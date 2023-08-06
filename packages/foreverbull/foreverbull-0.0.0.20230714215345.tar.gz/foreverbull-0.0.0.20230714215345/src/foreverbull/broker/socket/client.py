from foreverbull.broker.socket.nanomsg import NanomsgContextSocket, NanomsgSocket
from foreverbull.models.service import Request, Response, SocketConfig


class ContextClient:
    def __init__(self, context_socket: NanomsgContextSocket):
        self._context_socket = context_socket

    def send(self, message: Response) -> None:
        self._context_socket.send(message.dump())

    def recv(self) -> Request:
        data = self._context_socket.recv()
        return Request.load(data)

    def close(self) -> None:
        self._context_socket.close()


class SocketClient:
    def __init__(self, config: SocketConfig) -> None:
        self.config = config
        self._socket = NanomsgSocket(config)

    def url(self) -> str:
        return self._socket.url()

    def send(self, message: Response) -> None:
        self._socket.send(message.dump())

    def recv(self) -> Request:
        data = self._socket.recv()
        return Request.load(data)

    def close(self) -> None:
        self._socket.close()

    def new_context(self) -> ContextClient:
        return ContextClient(NanomsgContextSocket(self._socket.new_context()))
