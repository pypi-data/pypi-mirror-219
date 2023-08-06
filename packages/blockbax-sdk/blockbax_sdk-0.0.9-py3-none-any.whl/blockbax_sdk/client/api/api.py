from typing import Any, Dict, Generator, List, Optional, cast

import logging


log = logging.getLogger(__name__)

import json
import math
import platform
import sys


import httpx
from tenacity import Retrying, TryAgain, RetryCallState
from tenacity.wait import wait_exponential
from tenacity.stop import stop_after_attempt

from blockbax_sdk import __version__
from . import api_utils
from ...models.series import SeriesRequest


class BlockbaxAuth(httpx.Auth):
    def __init__(self, token: str):
        self.token = token

    # Override
    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        request.headers["Authorization"] = f"ApiKey {self.token}"
        yield request


BASE_URL = "https://api.blockbax.com/"
DEFAULT_API_VERSION = "v1/"
PROJECTS_ENDPOINT = "projects/"


class BlockbaxHTTPSession(httpx.Client):
    user_agent: str = f"Blockbax Python SDK/{__version__} HTTPX/{httpx.__version__} Python/{sys.version} {platform.platform()}".replace(
        "\n", ""
    )
    retryer: Retrying
    tries: int = 3
    back_off_factor: int = 1
    status_force_list: List[int] = [
        httpx.codes.BAD_GATEWAY,
        httpx.codes.SERVICE_UNAVAILABLE,
        httpx.codes.GATEWAY_TIMEOUT,
    ]
    timeout_seconds: float = 10.0
    rate_limit_option: api_utils.RateLimitOption
    _sleep_buffer: int = 1

    def __init__(
        self,
        token: str,
        project_id: str,
        rate_limit_option: api_utils.RateLimitOption = api_utils.RateLimitOption.SLEEP,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.rate_limit_option = rate_limit_option
        self.retryer = Retrying(
            # Reraise the original error after the last attempt failed
            reraise=True,
            # Return the result of the last call attempt
            retry_error_callback=self.__retry_error_callback,
            # Exponential backoff
            wait=wait_exponential(multiplier=self.back_off_factor, min=1, max=10),
            # Stop retrying after the defined number of tries
            stop=stop_after_attempt(self.tries),
        )
        headers = httpx.Headers(
            {
                "Content-Type": "application/json",
                "User-Agent": self.user_agent,
            }
        )

        super(BlockbaxHTTPSession, self).__init__(
            trust_env=False,
            event_hooks={
                "request": [self.request_hook],
                "response": [self.response_hook],
            },
            headers=headers,
            auth=BlockbaxAuth(token),
            base_url=httpx.URL(
                f"{BASE_URL}{DEFAULT_API_VERSION}{PROJECTS_ENDPOINT}{project_id}"
            ),
            timeout=httpx.Timeout(self.timeout_seconds),
            *args,
            **kwargs,
        )

    # Overwrite
    def request(self, *args: Any, **kwargs: Any) -> httpx.Response:
        try:
            return self.retryer(
                super(BlockbaxHTTPSession, self).request, *args, **kwargs
            )

        except TryAgain:
            # Internally raised by the rate limit handler
            # If for some reason this failes after the amount of tries 'TryAgain' would be reraised
            raise RuntimeError(
                f"Unexpected error, retrying requests due to rate limiter failed after {self.tries} tries."
            )

    def __retry_error_callback(self, retry_state: RetryCallState) -> httpx.Response:
        retry_outcome = retry_state.outcome
        if retry_outcome is not None:
            return cast(httpx.Response, retry_outcome.result())
        raise RuntimeError(
            "Unexpected error, retry failed but the last outcome is 'None'. Expecting atleast one outcome with a response."
        )

    def request_hook(self, request: httpx.Request):
        """Request hook is called right before the request is made"""

    def response_hook(self, response: httpx.Response):
        """Response hook is called right after a request has been made"""

        # Immediately raise error if the access token is not unauthorized
        api_utils.raise_for_unauthorized_error(response)

        # Force a retry if the status code is in the 'status_force_list'
        if response.status_code in self.status_force_list:
            raise TryAgain

        # Handle rate limites retries
        api_utils.handle_rate_limiter(
            response, self.rate_limit_option, self._sleep_buffer
        )
        # Handles different HTTP error cases, either log errors or raises new Blockbax Errors
        client_error_codes = (
            [400, 402, 403] + list(range(405, 429)) + list(range(430, 500))
        )

        api_utils.raise_client_error(response, client_error_codes)
        server_error_codes = list(range(500, 600))
        api_utils.raise_server_error(response, server_error_codes)

        # Handles HTTP status codes that are not an error or not found
        api_utils.notify_partial_accepted(response)
        api_utils.notify_not_found(response)


class Api:
    # settings
    access_token: str
    project_id: str
    default_page_size: int = 200
    # endpoints
    property_types_endpoint: str = "propertyTypes"
    subject_types_endpoint: str = "subjectTypes"
    subjects_endpoint: str = "subjects"
    metrics_endpoint: str = "metrics"
    measurements_endpoint: str = "measurements"

    def __init__(
        self,
        access_token: str,
        project_id: str,
    ):
        self.access_token = access_token
        self.project_id = project_id

    def session(self) -> BlockbaxHTTPSession:
        return BlockbaxHTTPSession(self.access_token, self.project_id)

    def get_user_agent(self) -> str:
        return BlockbaxHTTPSession.user_agent

    # http requests
    def get(self, endpoint: str = "", params={}) -> Optional[dict]:
        """get a single instance from the API using ID"""
        params = {k: v for k, v in params.items() if v is not None}
        with self.session() as session:
            r = session.get(url=endpoint, params=params)
        return api_utils.parse_response(r)

    def search(
        self, endpoint: str = "", params: Optional[Dict[str, Any]] = None
    ) -> List[dict]:
        """search multiple instances from the API using automatic paging, returns a list of results"""
        # check params, if no size or page was given use default
        if not params:
            params = {}
        params = {k: v for k, v in params.items() if v is not None}
        params["size"] = self.default_page_size

        current_page_index = 0
        last_page_number = None
        results: List[dict] = []
        done = False
        # while the previous page is not equal to the last page index get the current page index

        with self.session() as session:
            while not done:
                params["page"] = current_page_index
                r = session.get(url=endpoint, params=params)
                response = api_utils.parse_response(r)
                if response is None:
                    return results
                result = cast(list, response.get("result"))
                results.extend(result if result is not None else [])
                if response.get("count") is None:
                    return results  # return because we do not know when to stop

                if last_page_number is None:
                    last_page_number = math.ceil(
                        response["count"] / params["size"]
                    )  # page index starts from 0
                current_page_index += 1

                if current_page_index >= last_page_number:
                    done = True
        return results

    def post(self, endpoint: str, data):
        with self.session() as session:
            r = session.post(
                url=endpoint,
                data=json.dumps(data, cls=api_utils.JSONEncoderWithDecimal),
            )
        return api_utils.parse_response(r)

    def put(self, endpoint: str, data):
        with self.session() as session:
            r = session.put(
                url=endpoint,
                data=json.dumps(data, cls=api_utils.JSONEncoderWithDecimal),
            )

        return api_utils.parse_response(r)

    def delete(self, endpoint: str):
        with self.session() as session:
            session.delete(endpoint)

    # project

    def get_project(self):
        return self.get()

    # property types

    def get_property_type(self, property_type_id: str):
        return self.get(endpoint=f"{self.property_types_endpoint}/{property_type_id}")

    def get_property_types(
        self, name: Optional[str] = None, external_id: Optional[str] = None
    ):
        params = {"name": name, "externalId": external_id}
        return self.search(self.property_types_endpoint, params=params)

    def create_property_type(
        self,
        name: str,
        external_id: str,
        data_type: str,
        predefined_values: bool = False,
        values: List[dict] = [],
    ):
        body = {
            "name": name,
            "externalId": external_id,
            "dataType": data_type,
            "predefinedValues": predefined_values,
            "values": values,
        }
        response = self.post(endpoint=self.property_types_endpoint, data=body)
        return response

    def update_property_type(
        self,
        property_type_id: str,
        name: str,
        external_id: str,
        data_type: str,
        predefined_values=False,
        values=[],
    ):
        body = {
            "name": name,
            "externalId": external_id,
            "dataType": data_type,
            "predefinedValues": predefined_values,
            "values": values,
        }
        response = self.put(
            endpoint=f"{self.property_types_endpoint}/{property_type_id}", data=body
        )
        return response

    def delete_property_type(self, property_type_id: str):
        self.delete(endpoint=f"{self.property_types_endpoint}/{property_type_id}")

    # subject types

    def get_subject_type(self, subject_type_id: str):
        return self.get(endpoint=f"{self.subject_types_endpoint}/{subject_type_id}")

    def get_subject_types(
        self, name: Optional[str] = None, property_type_ids: Optional[list] = None
    ):
        params = {"name": name, "propertyTypes": property_type_ids}
        return self.search(endpoint=f"{self.subject_types_endpoint}", params=params)

    def create_subject_type(
        self,
        name: str,
        parent_ids: Optional[List[str]] = None,
        primary_location: Optional[dict] = {},
        property_types: Optional[list] = [],
    ):
        body = {
            "name": name,
            "parentSubjectTypeIds": parent_ids,
            "primaryLocation": primary_location,
            "propertyTypes": property_types,
        }
        response = self.post(endpoint=self.subject_types_endpoint, data=body)
        return response

    def update_subject_type(
        self,
        subject_type_id: str,
        name: str,
        parent_ids: Optional[List[str]] = None,
        primary_location: Optional[dict] = {},
        property_types: Optional[list] = [],
    ):
        body = {
            "name": name,
            "parentSubjectTypeIds": parent_ids,
            "primaryLocation": primary_location,
            "propertyTypes": property_types,
        }
        response = self.put(
            endpoint=f"{self.subject_types_endpoint}/{subject_type_id}", data=body
        )
        return response

    def delete_subject_type(self, subject_type_id: str):
        self.delete(endpoint=f"{self.subject_types_endpoint}/{subject_type_id}")

    # subjects

    def get_subject(self, subject_id: str) -> Optional[dict]:
        return self.get(endpoint=f"{self.subjects_endpoint}/{subject_id}")

    def get_subjects(
        self,
        name: Optional[str] = None,
        subject_ids: Optional[List[str]] = None,
        subject_type_ids: Optional[list] = None,
        subject_ids_mode: Optional[str] = None,
        subject_external_id: Optional[str] = None,
        property_value_ids: Optional[str] = None,
    ) -> list:
        params = {
            "name": name,
            "subjectIds": subject_ids,
            "subjectTypeIds": subject_type_ids,
            "subjectIdsMode": subject_ids_mode,
            "externalId": subject_external_id,
            "propertyValueIds": property_value_ids,
        }
        return self.search(endpoint=self.subjects_endpoint, params=params)

    def create_subject(
        self,
        name: str,
        subject_type_id: str,
        external_id: str,
        ingestion_ids: list,
        parent_id: Optional[str] = None,
        properties: Optional[list] = None,
    ):
        body = {
            "name": name,
            "subjectTypeId": subject_type_id,
            "parentSubjectId": parent_id,
            "externalId": external_id,
            "ingestionIds": ingestion_ids,
            "properties": properties,
        }
        response = self.post(endpoint=self.subjects_endpoint, data=body)
        return response

    def update_subject(
        self,
        subject_id: str,
        name: str,
        subject_type_id: str,
        external_id: str,
        ingestion_ids: list,
        parent_id: Optional[str] = None,
        properties: Optional[list] = None,
    ):
        body = {
            "name": name,
            "subjectTypeId": subject_type_id,
            "parentSubjectId": parent_id,
            "externalId": external_id,
            "ingestionIds": ingestion_ids,
            "properties": properties,
        }

        response = self.put(
            endpoint=f"{self.subjects_endpoint}/{subject_id}", data=body
        )

        return response

    def delete_subject(self, subject_id: str):
        self.delete(endpoint=f"{self.subjects_endpoint}/{subject_id}")

    # metrics

    def get_metric(self, metric_id: str) -> Optional[dict]:
        return self.get(endpoint=f"{self.metrics_endpoint}/{metric_id}")

    def get_metrics(
        self,
        name: Optional[str] = None,
        subject_type_ids: Optional[List[str]] = None,
        metric_external_id: Optional[str] = None,
    ) -> List[dict]:
        params = {
            "name": name,
            "subjectTypeIds": subject_type_ids,
            "externalId": metric_external_id,
        }
        return self.search(endpoint=self.metrics_endpoint, params=params)

    def create_metric(
        self,
        name: str,
        data_type: str,
        external_id: str,
        type_: str,
        subject_type_id: str,
        mapping_level: Optional[str] = None,
        discrete: Optional[bool] = None,
        unit: Optional[str] = None,
        precision: Optional[int] = None,
        visible: Optional[bool] = None,
    ):
        body = {
            "name": name,
            "externalId": external_id,
            "subjectTypeId": subject_type_id,
            "dataType": data_type,
            "unit": unit,
            "precision": precision,
            "visible": visible,
            "type": type_,
            "discrete": discrete,
            "mappingLevel": mapping_level,
        }
        response = self.post(endpoint=self.metrics_endpoint, data=body)
        return response

    def update_metric(
        self,
        metric_id: str,
        name: str,
        data_type: str,
        external_id: str,
        type_: str,
        discrete: bool,
        subject_type_id: str,
        mapping_level: Optional[str] = None,
        unit: Optional[str] = None,
        precision: Optional[int] = None,
        visible: Optional[bool] = None,
    ):
        body = {
            "name": name,
            "externalId": external_id,
            "subjectTypeId": subject_type_id,
            "dataType": data_type,
            "unit": unit,
            "precision": precision,
            "visible": visible,
            "type": type_,
            "discrete": discrete,
            "mappingLevel": mapping_level,
        }
        response = self.put(endpoint=f"{self.metrics_endpoint}/{metric_id}", data=body)
        return response

    def delete_metric(self, metric_id: str):
        self.delete(endpoint=f"{self.metrics_endpoint}/{metric_id}")

    # measurements

    def get_measurements(
        self,
        subject_ids: Optional[str] = None,
        metric_ids: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        size: Optional[int] = None,
        order: Optional[str] = "asc",
    ) -> Optional[dict]:
        params = {
            "subjectIds": subject_ids,
            "metricIds": metric_ids,
            "fromDate": from_date,
            "toDate": to_date,
            "size": size,
            "order": order,
        }
        return self.get(endpoint=self.measurements_endpoint, params=params)

    def send_measurements(self, series: SeriesRequest):
        response = self.post(endpoint=self.measurements_endpoint, data=series)
        return response
