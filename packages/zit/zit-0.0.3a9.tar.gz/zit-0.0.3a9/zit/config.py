import logging
import os
from pathlib import Path

from rich.logging import RichHandler

ZITRC_FILE = Path(os.path.expanduser("~/.zitrc"))
REGISTRY_ENDPOINT = "https://www.api.zityspace.cn/formula-registry"
WS_PUBLISH_ENDPOINT = "wss://www.api.zityspace.cn/formula-registry/formula/publish"
WS_INSTALL_ENDPOINT = "wss://www.api.zityspace.cn/formula-registry/formula/install"
AUTH_PUBLIC_ENDPOINT = "https://www.api.zityspace.cn/auth/public"


logging.basicConfig(level="INFO", format="%(message)s", handlers=[RichHandler(rich_tracebacks=True)])
logger = logging.getLogger(__name__)
