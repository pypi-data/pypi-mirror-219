import decimal
from typing_extensions import TypeGuard
from typing import Any, Mapping, List, Optional, cast, Type, TypeVar

from . import convertions
from blockbax_sdk import types

import logging

logger = logging.getLogger(__name__)

T = TypeVar("T")


def validate_dict(
    type: Type[T], dict_to_check: Mapping[Any, Any], keys: list
) -> TypeGuard[T]:
    if not isinstance(dict_to_check, dict):
        raise ValueError(f"Dictionary `{dict_to_check}` is not a dict")
    missing_keys = []
    for key in keys:
        if key not in dict_to_check:
            missing_keys.append(key)
    if len(missing_keys) > 0:
        raise ValueError(
            f"Dictionary is not of type '{type.__name__}', received value: {dict_to_check} does not have keys: {missing_keys}"
        )
    return True


def check_date_and_convert_to_unix(d: Optional[types.AnyDate]) -> Optional[int]:
    """checks if the given date can be converted to a datetime object and returns the unix timestamp"""
    if d is None:
        return d
    return convertions.convert_any_date_to_unix_millis(d)


def check_text(v: str) -> str:
    """checks if value is instance of str, or Text type, if not raise error"""
    if not isinstance(v, str):
        value_not_text_error = f"Text value {v} is not a Text type"
        raise ValueError(value_not_text_error)
    return v


def check_number_and_convert_to_decimal(v: types.AnyNumber) -> decimal.Decimal:
    """Check if value can be converted into a Decimal.  returns a decimal"""
    return convertions.convert_number_to_decimal(v)


def check_latitude_and_convert_to_decimal(latitude: types.AnyNumber) -> decimal.Decimal:
    """Check if latitude can be converted into a Decimal and if within range: 90 < latitude < -90.  returns a decimal"""
    try:
        latitude = convertions.convert_number_to_decimal(latitude)
        if 90 < latitude < -90:
            raise ValueError(
                f"Latitude is not within correct range: 90 < {latitude} < -90 == {90 < latitude < -90}"
            )
        return latitude
    except (decimal.InvalidOperation, ValueError) as e:
        latitude_convertion_error = f"Could not convert: {latitude}, cause: {e}"
        raise ValueError(latitude_convertion_error)


def check_longitude_and_convert_to_decimal(
    longitude: types.AnyNumber,
) -> decimal.Decimal:
    """Check if longitude can be converted into a Decimal and if within range: 180 < longitude < -180.  returns a decimal"""
    try:
        longitude = convertions.convert_number_to_decimal(longitude)
        if 180 < longitude < -180:
            raise ValueError(
                f"Longitude is not within correct range: 180 < {longitude} < -180 == {180 < longitude < -180}"
            )
        return longitude
    except (decimal.InvalidOperation, ValueError) as e:
        longitude_convertion_error = f"Could not convert: {longitude}, cause: {e}"
        raise ValueError(longitude_convertion_error)


def check_altitude_and_convert_to_decimal(altitude: types.AnyNumber) -> decimal.Decimal:
    """Check if altitude can be converted into a Decimal.  returns a decimal"""
    try:
        altitude = convertions.convert_number_to_decimal(altitude)
        return altitude
    except (decimal.InvalidOperation, ValueError) as e:
        altitude_convertion_error = f"Could not convert: {altitude}, cause: {e}"
        raise ValueError(altitude_convertion_error)


def check_location_and_convert(location: types.LocationLike) -> types.Location:
    # check if lat and lon are numeric and if the l dict has lat and lon
    validate_dict(types.Location, location, ["lat", "lon"])

    if "lat" in location and "lon" in location:
        location["lat"] = check_latitude_and_convert_to_decimal(location["lat"])
        location["lon"] = check_longitude_and_convert_to_decimal(location["lon"])
    if "alt" in location:
        # altitude is optional
        alt = location.get("alt")
        if alt is not None:
            location["alt"] = check_altitude_and_convert_to_decimal(alt)
    return cast(types.Location, location)


def check_map_layer_and_convert(map_layer: types.MapLayerLike) -> types.MapLayer:
    validate_dict(
        types.MapLayer,
        map_layer,
        ["imagePath", "leftBottom", "leftTop", "rightBottom", "rightTop"],
    )

    if not isinstance(map_layer["imagePath"], str):
        raise ValueError("'imagePath' is not a 'str'")

    return {
        "imagePath": map_layer["imagePath"],
        "leftBottom": check_location_and_convert(map_layer["leftBottom"]),
        "leftTop": check_location_and_convert(map_layer["leftTop"]),
        "rightBottom": check_location_and_convert(map_layer["rightBottom"]),
        "rightTop": check_location_and_convert(map_layer["rightTop"]),
    }


def check_image(image: types.Image) -> types.Image:
    validate_dict(types.Image, image, ["imagePath"])

    if not isinstance(image["imagePath"], str):
        raise ValueError("'imagePath' is not a 'str'")

    return image


def list_contains_single_value(l: list) -> bool:
    summation = sum([value is not None for value in l])
    if summation > 1 or summation < 1:
        return False
    return True


def check_and_convert_outer_ring(
    outer_ring: List[types.LocationLike],
) -> List[types.Location]:
    return [check_location_and_convert(location) for location in outer_ring]


def check_and_convert_polygon(polygon: types.PolygonLike) -> types.Polygon:
    validate_dict(types.Polygon, polygon, ["outerRing"])

    return {
        "outerRing": check_and_convert_outer_ring(polygon["outerRing"]),
    }


def check_area_and_convert(area: types.AreaLike) -> types.Area:
    validate_dict(types.Area, area, ["polygon"])
    return {
        "polygon": check_and_convert_polygon(area["polygon"]),
    }
