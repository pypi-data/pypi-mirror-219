import can
import isotp
from _typeshed import Incomplete

class ListenableStack(isotp.CanStack):
    def rx_canbus(self): ...
    listener: Incomplete
    def __init__(self, bus, listener: can.Listener = ..., *args, **kwargs) -> None: ...

class Cantp:
    stack: Incomplete
    txid: Incomplete
    rxid: Incomplete
    logger: Incomplete
    bus: Incomplete
    def __init__(self, bus, txid, rxid, listener: Incomplete | None = ..., *args, **kwargs) -> None: ...
    def send_request(self, cmd, functional: bool = ..., timeout: int = ...): ...
    def poll_response(self, timeout: int = ...) -> bytearray: ...
