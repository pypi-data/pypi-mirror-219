from ethrpc_accounts import Account  # noqa: E402,
import pkg_resources

from ethrpc.main import (
    AsyncWeb3,
    Ethrpc,
)
from ethrpc.providers.async_rpc import (  # noqa: E402
    AsyncHTTPProvider,
)
from ethrpc.providers.eth_tester import (  # noqa: E402
    EthereumTesterProvider,
)
from ethrpc.providers.ipc import (  # noqa: E402
    IPCProvider,
)
from ethrpc.providers.rpc import (  # noqa: E402
    HTTPProvider,
)
from ethrpc.providers.websocket import (  # noqa: E402
    WebsocketProvider,
)

__version__ = pkg_resources.get_distribution("ethrpc").version

__all__ = [
    "__version__",
    "AsyncWeb3",
    "Ethrpc",
    "HTTPProvider",
    "IPCProvider",
    "WebsocketProvider",
    "EthereumTesterProvider",
    "Account",
    "AsyncHTTPProvider",
]
