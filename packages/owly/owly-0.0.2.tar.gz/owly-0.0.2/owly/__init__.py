"""Set of utilities related to ontologies and their management."""
__version__ = "0.0.2"
__version_info__ = tuple((int(num) if num.isdigit() else num for num in __version__.replace("-", ".", 1).split(".")))

from owly.endpoint import Endpoint, QueryResult

__all__ = [
    "Endpoint",
    "QueryResult",
    "__version__",
    "__version_info__",
]
