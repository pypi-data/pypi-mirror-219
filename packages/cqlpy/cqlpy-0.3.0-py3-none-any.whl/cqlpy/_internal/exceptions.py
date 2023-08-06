class CqlPyError(Exception):
    ...


class CqlPyValueError(CqlPyError, ValueError):
    ...


class CqlPyTypeError(CqlPyError, TypeError):
    ...


class CqlPyKeyError(CqlPyError, KeyError):
    ...


class CqlParseError(CqlPyValueError):
    ...


class ValuesetProviderError(CqlPyError):
    ...


class ValuesetReadError(CqlPyError):
    ...


class ValuesetInterpretationError(ValuesetReadError):
    ...
