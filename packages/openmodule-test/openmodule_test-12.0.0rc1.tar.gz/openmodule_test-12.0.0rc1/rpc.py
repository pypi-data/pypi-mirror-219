import random
import string
import threading
import time
from functools import partial
from typing import Dict, Tuple, Any, Callable, Type, Optional

from pydantic.main import BaseModel

from openmodule.models.base import OpenModuleModel
from openmodule.models.rpc import RPCErrorResult, RPCServerError
from openmodule.rpc import RPCClient
from openmodule_test.zeromq import ZMQTestMixin


class _EmptyModel(BaseModel):
    pass


class RPCServerTestMixin(ZMQTestMixin):
    def wait_for_rpc_response(self, channel: str, type: str, request: BaseModel, response_type: Type[OpenModuleModel]):
        """
        waits until a rpc server is responding to the channel/type
        """
        for x in range(self.zmq_client.startup_check_iterations):
            try:
                self.rpc(channel, type, request, response_type, timeout=0.1)
                return
            except TimeoutError:
                pass

            time.sleep(self.zmq_client.startup_check_delay)

        assert False, "error during startup and connect"

    def wait_for_rpc_server(self, server):
        message_received = False

        def handler(_, __):
            nonlocal message_received
            message_received = True

        """
        waits until a rpc server is responding on the last channel we registered
        this assumes that the subscription we issue is the last and if it is connected, 
        all previous subscriptions will also be connected
        """
        assert server.handlers, "you need to register the handlers beforehand"
        random_channel = "_test" + "".join(random.choices(string.ascii_letters, k=10))

        server.register_handler(random_channel, "ping", _EmptyModel, _EmptyModel, handler, register_schema=False)

        for x in range(self.zmq_client.startup_check_iterations):
            self.rpc_no_response(random_channel, "ping", {})
            time.sleep(self.zmq_client.startup_check_delay)
            if message_received:
                break

        assert message_received, "error during startup and connect"


class MockRPCEntry(RPCClient.RPCEntry):
    def __init__(self, timeout, callback):
        super().__init__(timeout)
        self.callback = callback

    def _run_callback(self):
        try:
            res = self.callback()
            self.response = {"status": "ok", **(res if isinstance(res, dict) else res.dict())}
        except Exception:
            self.response = RPCErrorResult(status=RPCServerError.handler_error).dict()
        self.ready.set()

    def result(self, response_type: Type[OpenModuleModel], timeout=None):
        thread = threading.Thread(target=self._run_callback, daemon=True)
        thread.start()
        return super().result(response_type, timeout)


class MockRPCClient:
    def __init__(self, callbacks: Optional[Dict[Tuple[str, str], Callable[[OpenModuleModel, Any], Any]]] = None,
                 responses: Optional[Dict[Tuple[str, str], Any]] = None, default_timeout=1.0):
        self.callbacks = callbacks or {}
        self.responses = responses or {}
        self.last_request = {}
        self.default_timeout = default_timeout

    def rpc_non_blocking(self, channel: str, type: str, request: [Dict, BaseModel], timeout: float = None) \
            -> RPCClient.RPCEntry:
        self.last_request[(channel, type)] = request
        if timeout is None:
            timeout = self.default_timeout
        if (channel, type) in self.callbacks:
            entry = MockRPCEntry(timeout, partial(self.callbacks[(channel, type)], request, None))
        else:
            entry = RPCClient.RPCEntry(timeout)
            if (channel, type) in self.responses:
                res = self.responses.get((channel, type)).dict()
                entry.response = {"status": "ok", **(res if isinstance(res, dict) else res.dict())}
        return entry

    def rpc(self, channel: str, type: str, request: [Dict, BaseModel], response_type: Type[OpenModuleModel],
            timeout: float = None) -> OpenModuleModel:
        entry = self.rpc_non_blocking(channel, type, request, timeout)
        return entry.result(response_type, timeout=timeout)
