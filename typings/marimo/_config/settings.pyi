"""
This type stub file was generated by pyright.
"""

from dataclasses import dataclass

@dataclass
class GlobalSettings:
    DEVELOPMENT_MODE: bool = ...
    QUIET: bool = ...
    YES: bool = ...
    CHECK_STATUS_UPDATE: bool = ...
    TRACING: bool = ...
    PROFILE_DIR: str | None = ...
    LOG_LEVEL: int = ...
    MANAGE_SCRIPT_METADATA: bool = ...
    IN_SECURE_ENVIRONMENT: bool = ...


GLOBAL_SETTINGS = ...
