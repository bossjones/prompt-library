"""
This type stub file was generated by pyright.
"""

from typing import List, Optional
from marimo._ast.app import _AppConfig
from marimo._ast.cell import CellConfig, CellId_t
from marimo._config.config import MarimoConfig, PartialMarimoConfig
from marimo._messaging.cell_output import CellOutput
from marimo._server.model import SessionMode
from marimo._server.tokens import SkewProtectionToken

def home_page_template(html: str, base_url: str, user_config: MarimoConfig, config_overrides: PartialMarimoConfig, server_token: SkewProtectionToken) -> str:
    ...

def notebook_page_template(html: str, base_url: str, user_config: MarimoConfig, config_overrides: PartialMarimoConfig, server_token: SkewProtectionToken, app_config: _AppConfig, filename: Optional[str], mode: SessionMode) -> str:
    ...

def static_notebook_template(html: str, user_config: MarimoConfig, config_overrides: PartialMarimoConfig, server_token: SkewProtectionToken, app_config: _AppConfig, filepath: Optional[str], code: str, code_hash: str, cell_ids: list[str], cell_names: list[str], cell_codes: list[str], cell_configs: list[CellConfig], cell_outputs: dict[CellId_t, CellOutput], cell_console_outputs: dict[CellId_t, List[CellOutput]], files: dict[str, str], asset_url: Optional[str] = ...) -> str:
    ...
