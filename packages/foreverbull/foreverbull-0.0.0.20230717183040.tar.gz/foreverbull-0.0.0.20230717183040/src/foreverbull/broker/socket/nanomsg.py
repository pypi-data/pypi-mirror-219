from pynng import exceptions, nng

from foreverbull.models.service import SocketConfig

from .exceptions import SocketClosed, SocketTimeout


class NanomsgContextSocket:
    def __init__(self, context_socket: nng.Context):
        self._context_socket = context_socket

    def send(self, data: bytes) -> None:
        try:
            return self._context_socket.send(data)
        except exceptions.Closed as exc:
            raise SocketClosed(exc)

    def recv(self) -> bytes:
        try:
            return self._context_socket.recv()
        except exceptions.Timeout as exc:
            raise SocketTimeout(exc)
        except exceptions.Closed as exc:
            raise SocketClosed(exc)

    def close(self) -> None:
        return self._context_socket.close()


class NanomsgSocket:
    def __init__(self, config: SocketConfig):
        self._socket = None
        self._config = config
        if self._config.listen:
            self._socket = self._config.socket_type.get_socket()(
                listen=f"tcp://{self._config.host}:{self._config.port}"
            )
        else:
            self._socket = self._config.socket_type.get_socket()(dial=f"tcp://{self._config.host}:{self._config.port}")
        self._socket.recv_timeout = self._config.recv_timeout
        self._socket.send_timeout = self._config.send_timeout
        if self._config.listen and self._config.port == 0:
            # Pretty hacky way to find the port that OS randomly assigns when it's orginally set as 0
            self._config.port = int(self._socket.listeners[0].url.split(":")[-1])

    def url(self) -> str:
        if self._config.listen:
            return self._socket.listeners[0].url
        return self._socket.dialers[0].url

    def send(self, data: bytes) -> None:
        try:
            return self._socket.send(data)
        except exceptions.Closed as exc:
            raise SocketClosed(exc)

    def recv(self) -> bytes:
        try:
            return self._socket.recv()
        except exceptions.Timeout as exc:
            raise SocketTimeout(exc)
        except exceptions.Closed as exc:
            raise SocketClosed(exc)

    def close(self) -> None:
        return self._socket.close()

    def new_context(self) -> NanomsgContextSocket:
        return NanomsgContextSocket(self._socket.new_context())
