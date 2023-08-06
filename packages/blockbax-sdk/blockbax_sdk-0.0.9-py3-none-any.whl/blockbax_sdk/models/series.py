from typing import List, TypedDict

from blockbax_sdk import errors
from ..types import IngestionId
from . import measurement

import dataclasses
import datetime

import logging

logger = logging.getLogger(__name__)


class IngestionRequest(TypedDict, total=False):
    ingestionId: IngestionId
    measurements: List[measurement.MeasurementRequest]


class SeriesRequest(TypedDict, total=False):
    series: List[IngestionRequest]


@dataclasses.dataclass
class Series:
    subject_id: str
    metric_id: str
    measurements: List[measurement.Measurement] = dataclasses.field(
        default_factory=list
    )

    def __iter__(self):
        return iter(self.measurements)

    @classmethod
    def from_api_response(cls, api_response):
        # Because we are constructing a new list there is no need to copy
        measurements = []
        for measurement_response in api_response.get("measurements"):
            try:
                measurements.append(measurement.from_dict(measurement_response))
            except errors.ValidationError:
                pass

        return cls(
            subject_id=api_response.get("subjectId"),
            metric_id=api_response.get("metricId"),
            measurements=measurements,
        )

    @property
    def latest_date(self) -> datetime.datetime:
        latest_date = 0
        for measurement in self.measurements:
            if measurement.date is not None:
                latest_date = (
                    measurement.date if measurement.date > latest_date else latest_date
                )
        return datetime.datetime.fromtimestamp(latest_date / 1000.0)
