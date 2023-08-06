from typing import List

from .measurement import Measurement
from ..types import IngestionId, SubjectExternalId, MetricExternalId

import dataclasses

import logging

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Ingestion:
    id: IngestionId
    measurements: List[Measurement] = dataclasses.field(default_factory=list)
    measurement_count: int = dataclasses.field(default=0)
    sorted: bool = dataclasses.field(default=False)

    def __eq__(self, other_ingestion: object) -> bool:
        if isinstance(other_ingestion, Ingestion):
            self.sort()
            other_ingestion.sort()
            return (
                self.id == other_ingestion.id
                and self.measurements == other_ingestion.measurements
            )

        return False

    def __post_init__(self):
        if not self.measurement_count:
            self.measurement_count = 0
        if not self.id:
            no_ids_given_error = f"Please provide a ingestion ID"
            raise ValueError(no_ids_given_error)
        self.sorted = False

    def sort(self):
        if not self.sorted:
            # If no timestmap is set it means that the measurement has to be send as soon
            # This is because the timestmap will be infered when it is received
            self.measurements.sort(key=lambda m: m.date if m.date is not None else 0)
            self.sorted = True

    def get_sorted_measurements(self) -> List[Measurement]:
        self.sort()
        return self.measurements

    def add_measurement(self, new_measurement: Measurement, sort: bool = False) -> None:
        if (
            len(self.measurements) > 0
            and new_measurement.get_data_type() != self.measurements[-1].get_data_type()
        ):
            inconsistent_use_of_data_type_error = f"Inconsistent use of data types, data type: {new_measurement.get_data_type()} does not equal data type of previous measurement added to this ingestion: {self.measurements[-1].get_data_type()}"
            raise ValueError(inconsistent_use_of_data_type_error)

        self.measurements.append(new_measurement)
        self.measurement_count += 1
        latest_measurement_date = self.measurements[-1].date
        if (
            latest_measurement_date is not None
            and new_measurement.date is not None
            and latest_measurement_date > new_measurement.date
        ):
            self.sorted = False

        if sort:
            self.sort()

    def clear(self):
        self.measurements.clear()
        self.measurement_count = 0

    def get_measurement_count(self):
        return len(self.measurements)
