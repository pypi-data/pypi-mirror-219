from typing import (
    Optional,
)

from ethrpc import (
    Ethrpc,
)
from ethrpc._utils.rpc_abi import (
    RPC,
)
from ethrpc.types import (
    TxParams,
    Wei,
)


def rpc_gas_price_strategy(
    w3: Ethrpc, transaction_params: Optional[TxParams] = None
) -> Wei:
    """
    A simple gas price strategy deriving it's value from the eth_gasPrice JSON-RPC call.
    """
    return w3.manager.request_blocking(RPC.eth_gasPrice, [])
