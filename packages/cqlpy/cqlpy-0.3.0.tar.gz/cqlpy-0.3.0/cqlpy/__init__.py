"""
.. include:: ../README.md
"""

from importlib import metadata
from cqlpy._internal.context.context import Context
from cqlpy._internal.providers.local_valueset_provider import LocalValuesetProvider
from cqlpy._internal.providers.rosetta_valueset_provider import RosettaValuesetProvider
from cqlpy._internal.providers.valueset_provider import ValuesetProvider


__version__ = metadata.version("cqlpy")

__all__ = [
    "Context",
    "ValuesetProvider",
    "LocalValuesetProvider",
    "RosettaValuesetProvider",
]
