"""
This type stub file was generated by pyright.
"""

from astroid.manager import AstroidManager

"""Astroid hooks for understanding ``boto3.ServiceRequest()``."""
BOTO_SERVICE_FACTORY_QUALIFIED_NAME = ...
def service_request_transform(node):
    """Transform ServiceResource to look like dynamic classes."""
    ...

def register(manager: AstroidManager) -> None:
    ...