"""
This type stub file was generated by pyright.
"""

from typing import Dict

def src_or_src_doc(html_content: str) -> Dict[str, str]:
    """
    Depending if virtual files are supported,
    return the appropriate src or srcdoc attribute for an iframe.

    While `src:text/html;base64` is supported in most modern browsers,
    it does not allow us to resize the iframe to fit the content.

    So, we use `srcdoc` when not running a server (e.g. an html export).
    """
    ...
