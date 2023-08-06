import enum
import socket
from typing import Any, List, Optional

import pydantic
import pynng

from .base import Base


class Parameter(Base):
    key: str
    default: Optional[str] = None
    value: Optional[str] = None
    type: str


class Info(Base):
    type: str
    version: str
    parameters: List[Parameter]
    routes: List[str]


class Database(Base):
    user: str
    password: str
    netloc: str
    port: int
    dbname: str


class SocketType(str, enum.Enum):
    REQUESTER = "REQUESTER"
    REPLIER = "REPLIER"
    PUBLISHER = "PUBLISHER"
    SUBSCRIBER = "SUBSCRIBER"

    def get_socket(self):
        if self == SocketType.REQUESTER:
            return pynng.Req0
        elif self == SocketType.REPLIER:
            return pynng.Rep0
        elif self == SocketType.PUBLISHER:
            return pynng.Pub0
        elif self == SocketType.SUBSCRIBER:
            return pynng.Sub0
        else:
            raise Exception("Unknown socket type: {}".format(self))


class SocketConfig(Base):
    socket_type: SocketType = SocketType.REPLIER
    host: str = socket.gethostbyname(socket.gethostname())
    port: int = 0
    listen: bool = True
    recv_timeout: int = 500
    send_timeout: int = 500


class Request(Base):
    task: str
    data: Optional[Any] = None
    error: Optional[str] = None

    @pydantic.field_validator("data")
    def validate_data(cls, v):
        if v is None:
            return v
        if type(v) is dict:
            return v
        return v.model_dump()


class Response(Base):
    task: str
    error: Optional[str] = None
    data: Optional[Any] = None

    @pydantic.field_validator("data")
    def validate_data(cls, v):
        if v is None:
            return v
        if type(v) is dict:
            return v
        return v.model_dump()
