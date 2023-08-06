"""Blockbax Python SDK"""
import logging
from typing import cast

logging.getLogger(__name__).addHandler(logging.NullHandler())
try:
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore
try:
    __version__ = cast(str, version(__name__))
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

from .client import HttpClient
from . import models
from . import errors
from . import types

__all__ = [
    "HttpClient",
    "models",
    "errors",
    "types",
]
