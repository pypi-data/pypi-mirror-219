from typing import Union, Optional, TypedDict
from numbers import Number
import decimal

from ..util import validation
from .. import types, errors

import abc
import dataclasses

import logging

logger = logging.getLogger(__name__)


class BaseMeasurementRequest(TypedDict):
    date: Optional[int]


class NumberMeasurementRequest(BaseMeasurementRequest):
    number: decimal.Decimal


class LocationMeasurementRequest(BaseMeasurementRequest):
    location: types.Location


class TextMeasurementRequest(BaseMeasurementRequest):
    text: str


MeasurementRequest = Union[
    NumberMeasurementRequest,
    LocationMeasurementRequest,
    TextMeasurementRequest,
]


# ignore because indirect relation with: https://github.com/python/mypy/issues/4717
# needs to be a dataclass to make let it work nicely with the specific measurement implementations
@dataclasses.dataclass  # type: ignore
class Measurement(abc.ABC):
    date: Optional[int] = dataclasses.field(default=None)

    @abc.abstractmethod
    def get_value(self) -> Union[int, str, types.Location, decimal.Decimal]:
        pass

    @classmethod
    @abc.abstractmethod
    def get_data_type(cls) -> str:
        pass

    @abc.abstractmethod
    def to_request(self) -> MeasurementRequest:
        ...


@dataclasses.dataclass
class NumberMeasurement(Measurement):
    number: decimal.Decimal = dataclasses.field(default_factory=decimal.Decimal)

    def get_value(self) -> decimal.Decimal:
        return self.number

    @classmethod
    def get_data_type(cls) -> str:
        return types.MeasurementDataTypes.NUMBER.value

    def to_request(self) -> NumberMeasurementRequest:
        return NumberMeasurementRequest(date=self.date, number=self.number)


@dataclasses.dataclass
class LocationMeasurement(Measurement):
    # ignore because: https://github.com/python/mypy/issues/5723
    location: types.Location = dataclasses.field(default_factory=types.Location)  # type: ignore

    def get_value(self) -> types.Location:
        return self.location

    @classmethod
    def get_data_type(cls) -> str:
        return types.MeasurementDataTypes.LOCATION.value

    def to_request(self) -> LocationMeasurementRequest:
        return LocationMeasurementRequest(date=self.date, location=self.location)


@dataclasses.dataclass
class TextMeasurement(Measurement):
    text: str = dataclasses.field(default_factory=str)

    def get_value(self) -> str:
        return self.text

    @classmethod
    def get_data_type(cls) -> str:
        return types.MeasurementDataTypes.TEXT.value

    def to_request(self) -> TextMeasurementRequest:
        return TextMeasurementRequest(date=self.date, text=self.text)


def new(
    date: Optional[types.AnyDate] = None,
    number: Optional[types.AnyNumber] = None,
    location: Optional[types.LocationLike] = None,
    text: Optional[str] = None,
    **kwargs,
) -> Optional[Measurement]:
    values: dict = {"number": number, "location": location, "text": text}

    if not validation.list_contains_single_value(list(values.values())):
        to_many_arguments_error = (
            f"Measurement takes exactly a single data type, values given: {values}"
        )
        raise errors.ValidationError(to_many_arguments_error)

    if number is not None:
        return NumberMeasurement(
            date=validation.check_date_and_convert_to_unix(date),
            number=validation.check_number_and_convert_to_decimal(number),
        )
    elif location is not None:
        return LocationMeasurement(
            date=validation.check_date_and_convert_to_unix(date),
            location=validation.check_location_and_convert(location),
        )
    elif text is not None:
        return TextMeasurement(
            date=validation.check_date_and_convert_to_unix(date),
            text=validation.check_text(text),
        )
    else:
        return None


def from_dict(kwargs: dict) -> Optional[Measurement]:
    return new(**kwargs)
