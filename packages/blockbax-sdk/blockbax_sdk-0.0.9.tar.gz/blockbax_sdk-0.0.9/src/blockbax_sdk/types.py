from typing_extensions import TypeAlias, Annotated, TypedDict
from typing import List, Optional, TypeVar, Union
import datetime
import enum
import uuid
from numbers import Number
from decimal import Decimal

import logging

logger = logging.getLogger(__name__)

# Generic types

AnyDate = Union[datetime.datetime, int, str]
AnyNumber = Union[int, float, Number, Decimal, str]

# Blockbax types

T = TypeVar("T")
BlockbaxType = Annotated[T, "BlockbaxType"]
BlockbaxId = Annotated[BlockbaxType[Union[str, uuid.UUID]], "BlockbaxId"]
BlockbaxExternalId = Annotated[BlockbaxType[str], "BlockbaxExternalId"]

# UUID' s
SubjectId = Annotated[BlockbaxId, "Subject"]
MetricId = Annotated[BlockbaxId, "Metric"]
PropertyTypeId = Annotated[BlockbaxId, "PropertyType"]
SubjectTypeId = Annotated[BlockbaxId, "SubjectType"]

# External ID' s
SubjectExternalId = Annotated[BlockbaxExternalId, "Subject"]
MetricExternalId = Annotated[BlockbaxExternalId, "Metric"]
PropertyTypeExternalId = Annotated[BlockbaxExternalId, "PropertyType"]

# Other ID
IngestionId = Annotated[BlockbaxType[str], "Ingestion"]
# Measurement data types


class BxType(str, enum.Enum):
    @classmethod
    def _missing_(cls, value: object):
        if isinstance(value, str):
            return _check_missing_is_upper_name(cls, value)
        return False


class MeasurementDataTypes(BxType):
    NUMBER = "number"
    LOCATION = "location"
    TEXT = "text"


# Property data types
class PropertyDataTypes(BxType):
    NUMBER = "number"
    LOCATION = "location"
    TEXT = "text"
    MAP_LAYER = "mapLayer"
    IMAGE = "image"
    AREA = "area"


# Primary location (Subject Type) types
class PrimaryLocationTypes(BxType):
    PROPERTY_TYPE = "PROPERTY_TYPE"
    METRIC = "METRIC"


# Metric types
class MetricTypes(BxType):
    INGESTED = "INGESTED"
    SIMULATED = "SIMULATED"
    CALCULATED = "CALCULATED"


class MetricMappingLevel(BxType):
    OWN = "OWN"
    CHILD = "CHILD"


# Check if given value is actually its lower counter part


def _check_missing_is_upper_name(cls, value: str):
    known_types = []
    for member in cls:
        known_types.append(member)
        if member.name == str(value).upper():
            return member
    error_unknown_type = f"'{value}' is not a known data type, known data types: {', '.join(known_types)}"
    raise ValueError(error_unknown_type)


class LocationLike(TypedDict, total=False):
    lat: AnyNumber
    lon: AnyNumber
    alt: Optional[AnyNumber]


class Location(TypedDict, total=False):
    lat: Decimal
    lon: Decimal
    alt: Optional[Decimal]


class MapLayerLike(TypedDict):
    imagePath: str
    leftBottom: LocationLike
    leftTop: LocationLike
    rightBottom: LocationLike
    rightTop: LocationLike


class MapLayer(TypedDict):
    imagePath: str
    leftBottom: Location
    leftTop: Location
    rightBottom: Location
    rightTop: Location


class Image(TypedDict):
    imagePath: str


class Polygon(TypedDict):
    outerRing: List[Location]


class Area(TypedDict):
    polygon: Polygon


class PolygonLike(TypedDict):
    outerRing: List[LocationLike]


class AreaLike(TypedDict):
    polygon: PolygonLike
