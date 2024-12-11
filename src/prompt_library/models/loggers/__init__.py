"""prompt_library.models.loggers"""

# pyright: reportAssignmentType=false
# pyright: strictParameterNoneValue=false
# pylint: disable=no-name-in-module

# SOURCE: https://blog.bartab.fr/fastapi-logging-on-the-fly/
from __future__ import annotations

from typing import Any, ForwardRef, List, Optional

from pydantic import BaseModel, Field


LoggerModel = ForwardRef("LoggerModel")


class LoggerPatch(BaseModel):
    name: str
    level: str


class LoggerModel(BaseModel):
    name: str
    level: int | None
    # children: Optional[List["LoggerModel"]] = None
    # fixes: https://github.com/samuelcolvin/pydantic/issues/545
    children: list[Any] | None = None
    # children: ListLoggerModel = None


LoggerModel.update_forward_refs()
