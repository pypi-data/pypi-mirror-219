from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
)

from eth_utils.toolz import (
    assoc,
)

from ethrpc.datastructures import (
    AttributeDict,
)
from ethrpc.types import (
    AsyncMiddlewareCoroutine,
    RPCEndpoint,
    RPCResponse,
)

if TYPE_CHECKING:
    from ethrpc import (  # noqa: F401
        AsyncWeb3,
        Ethrpc,
    )


def attrdict_middleware(
    make_request: Callable[[RPCEndpoint, Any], Any], _w3: "Ethrpc"
) -> Callable[[RPCEndpoint, Any], RPCResponse]:
    """
    Converts any result which is a dictionary into an `AttributeDict`.

    Note: Accessing `AttributeDict` properties via attribute
        (e.g. my_attribute_dict.property1) will not preserve typing.
    """

    def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
        response = make_request(method, params)

        if "result" in response:
            return assoc(
                response, "result", AttributeDict.recursive(response["result"])
            )
        else:
            return response

    return middleware


# --- async --- #


async def async_attrdict_middleware(
    make_request: Callable[[RPCEndpoint, Any], Any], _async_w3: "AsyncWeb3"
) -> AsyncMiddlewareCoroutine:
    """
    Converts any result which is a dictionary into an `AttributeDict`.

    Note: Accessing `AttributeDict` properties via attribute
        (e.g. my_attribute_dict.property1) will not preserve typing.
    """

    async def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
        response = await make_request(method, params)

        if "result" in response:
            return assoc(
                response, "result", AttributeDict.recursive(response["result"])
            )
        else:
            return response

    return middleware
