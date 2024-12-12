"""
This type stub file was generated by pyright.
"""

import httpx
from typing import Dict, List, Optional

"""
This type stub file was generated by pyright.
"""
MIME_TYPE_FIXES = ...
def mimetype_from_string(content) -> Optional[str]:
    ...

def mimetype_from_path(path) -> Optional[str]:
    ...

def dicts_to_table_string(headings: List[str], dicts: List[Dict[str, str]]) -> List[str]:
    ...

def remove_dict_none_values(d):
    """
    Recursively remove keys with value of None or value of a dict that is all values of None
    """
    ...

class _LogResponse(httpx.Response):
    def iter_bytes(self, *args, **kwargs):
        ...
    


class _LogTransport(httpx.BaseTransport):
    def __init__(self, transport: httpx.BaseTransport) -> None:
        ...
    
    def handle_request(self, request: httpx.Request) -> httpx.Response:
        ...
    


def logging_client() -> httpx.Client:
    ...

def simplify_usage_dict(d):
    ...

def token_usage_string(input_tokens, output_tokens, token_details) -> str:
    ...

