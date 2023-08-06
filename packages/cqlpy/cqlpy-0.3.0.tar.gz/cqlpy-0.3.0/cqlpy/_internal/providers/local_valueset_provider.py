import json
import re
from os import PathLike
from pathlib import Path
from typing import Optional

from typing import Any

from cqlpy._internal.providers.valueset_provider import ValuesetProvider
from cqlpy._internal.logger import get_logger

from cqlpy._internal.exceptions import (
    CqlPyKeyError,
    ValuesetInterpretationError,
    ValuesetReadError,
)

_DEFAULT_FILE_PATTERN = r".*?\.json|.*?\.ndjson"


class LocalValuesetProvider(ValuesetProvider):
    """
    A value set provider that loads value sets from a local directory or file.

    JSON and NDJSON files are supported.
    """

    def __init__(
        self, directory_or_file: PathLike, pattern: Optional[str] = None
    ) -> None:
        """
        Creates a new local value set provider.

        ## Parameters

        - `directory_or_file`: The directory or file to load value sets from. If a
            directory is provided, all files in the directory will be loaded. If a file is
            provided, only that file will be loaded.
        - `pattern`: A regular expression pattern to match files in the directory. Only
            files that match the pattern will be loaded. Defaults to .json and .ndjson
            files.
        """
        self.__directory = Path(directory_or_file)
        self.__pattern = pattern
        self.__valuesets: Optional[dict[str, dict[str, Any]]] = None
        self.__logger = get_logger().getChild(self.__class__.__name__)

    def __interpret_valueset(self, definition: str) -> list[tuple[str, dict[str, Any]]]:
        valuesets: list[tuple[str, dict[str, Any]]] = []
        try:
            valueset = json.loads(definition)
            valuesets.append((valueset["id"], valueset))
            return valuesets
        except json.JSONDecodeError as error:
            for line in definition.splitlines():
                try:
                    valueset = json.loads(line)
                    valuesets.append((valueset["id"], valueset))
                except Exception as error:
                    self.__logger.warning(
                        f"Failed to interpret value set definition: {error}"
                    )
                    raise ValuesetInterpretationError(
                        "Failed to interpret value set definition"
                    ) from error
            return valuesets
        except Exception as error:
            self.__logger.warning(f"Failed to interpret value set definition: {error}")
            raise ValuesetInterpretationError(
                "Failed to interpret value set definition"
            ) from error

    def __read_valueset(self, path: Path) -> list[tuple[str, dict[str, Any]]]:
        try:
            with open(path, "r") as handle:
                return self.__interpret_valueset(handle.read())
        except Exception as error:
            self.__logger.warning(f"Failed to read file {path}: {error}")
            raise ValuesetReadError(f"Failed to read file {path}") from error

    def __read_valuesets(self) -> dict[str, dict[str, Any]]:
        valuesets: dict[str, dict[str, Any]] = {}
        if self.__directory.is_file():
            self.__logger.debug(f"Reading value set from {self.__directory.name}")
            valueset_pairs = self.__read_valueset(self.__directory)
            for valueset_id, valueset_description in valueset_pairs:
                valuesets[valueset_id] = valueset_description
            return valuesets

        pattern = self.__pattern or _DEFAULT_FILE_PATTERN
        for file in self.__directory.iterdir():
            if not file.is_file():
                continue
            if not re.search(pattern, file.name):
                continue
            self.__logger.debug(f"Reading value set from {file.name}")
            valueset_pairs = self.__read_valueset(file)
            for valueset_id, valueset_description in valueset_pairs:
                valuesets[valueset_id] = valueset_description
        return valuesets

    @property
    def valuesets(self) -> dict[str, dict[str, Any]]:
        """
        All currently-loaded value sets.

        ## Returns

        A dictionary of value set IDs to value set definitions.
        """
        if self.__valuesets is None:
            self.__valuesets = self.__read_valuesets()
        return self.__valuesets

    def get_valueset(self, name: str, scope: Optional[str]) -> dict[str, Any]:
        try:
            valueset = self.valuesets[name]
        except ValuesetReadError as error:
            raise CqlPyKeyError(f"Value set {name} not found") from error
        return valueset
