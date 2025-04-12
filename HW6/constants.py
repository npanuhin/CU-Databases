from typing import Any, Iterable


PAGE_SIZE = 4096

TYPE_FORMATS = {
    'bool': ('?', 1),
    'char': ('c', 1),
    'int': ('i', 4),
    'long': ('q', 8),
    'float': ('d', 8),
    'string': ('s', 0),
    'datetime': ('q', 8),
}

SCHEMA_TYPE = Iterable[dict[str, Any]]
RECORD_TYPE = list[Any]
