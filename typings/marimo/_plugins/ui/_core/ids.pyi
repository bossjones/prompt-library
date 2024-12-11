"""
This type stub file was generated by pyright.
"""

class NoIDProviderException(Exception):
    ...


class IDProvider:
    """Provide IDs for UIElements

    Can be used to provide IDs that are stable across sessions.
    """
    def __init__(self, prefix: str) -> None:
        """Initialize an ID provider

        `prefix` should be unique across cells
        """
        ...

    def take_id(self) -> str:
        """Get an ID"""
        ...