from __future__ import annotations

import logging

from prompt_library.__version__ import __version__


logging.getLogger("asyncio").setLevel(logging.DEBUG)
logging.getLogger("httpx").setLevel(logging.DEBUG)
logging.getLogger("faker").setLevel(logging.DEBUG)
logging.getLogger("sentry_sdk").setLevel(logging.WARNING)
