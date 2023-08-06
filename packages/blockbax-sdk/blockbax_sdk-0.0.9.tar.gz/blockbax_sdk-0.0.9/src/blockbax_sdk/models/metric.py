from typing import Optional
from ..util import convertions

import datetime
import dataclasses

import logging

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Metric:
    subject_type_id: str
    name: str
    id: str
    external_id: str
    data_type: str
    type: str
    created_date: datetime.datetime
    visible: bool = dataclasses.field(default=True)
    discrete: bool = dataclasses.field(default=False)
    mapping_level: Optional[str] = dataclasses.field(default=None)
    updated_date: Optional[datetime.datetime] = dataclasses.field(default=None)
    unit: Optional[str] = dataclasses.field(default=None)
    precision: Optional[str] = dataclasses.field(default=None)

    def __post_init__(self):
        if self.created_date:
            self.created_date = convertions.convert_any_date_to_datetime(
                self.created_date
            )
        if self.updated_date:
            self.updated_date = convertions.convert_any_date_to_datetime(
                self.updated_date
            )

    @classmethod
    def from_api_response(cls, api_response: dict):
        visible = api_response.get("visible")
        return cls(
            subject_type_id=api_response.get("subjectTypeId"),
            name=api_response.get("name"),
            id=api_response.get("id"),
            external_id=api_response.get("externalId"),
            type=api_response.get("type"),
            mapping_level=api_response.get("mappingLevel"),
            created_date=api_response.get("createdDate"),
            updated_date=api_response.get("updatedDate"),
            discrete=api_response.get("discrete"),
            data_type=api_response.get("dataType"),
            precision=api_response.get("precision") or "",
            unit=api_response.get("unit") or "",
            visible=visible if visible is not None else True,  # default if not present
        )
