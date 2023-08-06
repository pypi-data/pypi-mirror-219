from ethrpc import (
    IPCProvider,
    Ethrpc,
)
from ethrpc.middleware import (
    geth_poa_middleware,
)
from ethrpc.providers.ipc import (
    get_dev_ipc_path,
)

w3 = Ethrpc(IPCProvider(get_dev_ipc_path()))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
