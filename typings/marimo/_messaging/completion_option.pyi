"""
This type stub file was generated by pyright.
"""

from dataclasses import dataclass
from typing import Optional

"""
This type stub file was generated by pyright.
"""
@dataclass
class CompletionOption:
    name: str
    type: str
    completion_info: Optional[str]
    def __post_init__(self) -> None:
        ...
    


