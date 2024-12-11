"""
This type stub file was generated by pyright.
"""

"""
This type stub file was generated by pyright.
"""
class MessageIdStore:
    """The MessageIdStore store MessageId and make sure that there is a 1-1 relation
    between msgid and symbol.
    """
    def __init__(self) -> None:
        ...

    def __len__(self) -> int:
        ...

    def __repr__(self) -> str:
        ...

    def get_symbol(self, msgid: str) -> str:
        ...

    def get_msgid(self, symbol: str) -> str:
        ...

    def register_message_definition(self, msgid: str, symbol: str, old_names: list[tuple[str, str]]) -> None:
        ...

    def add_msgid_and_symbol(self, msgid: str, symbol: str) -> None:
        """Add valid message id.

        There is a little duplication with add_legacy_msgid_and_symbol to avoid a function call,
        this is called a lot at initialization.
        """
        ...

    def add_legacy_msgid_and_symbol(self, msgid: str, symbol: str, new_msgid: str) -> None:
        """Add valid legacy message id.

        There is a little duplication with add_msgid_and_symbol to avoid a function call,
        this is called a lot at initialization.
        """
        ...

    def check_msgid_and_symbol(self, msgid: str, symbol: str) -> None:
        ...

    def get_active_msgids(self, msgid_or_symbol: str) -> list[str]:
        """Return msgids but the input can be a symbol.

        self.__active_msgids is used to implement a primitive cache for this function.
        """
        ...