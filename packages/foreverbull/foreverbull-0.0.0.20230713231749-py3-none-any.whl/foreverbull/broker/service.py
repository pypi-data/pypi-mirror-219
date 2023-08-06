import requests

from foreverbull.models.service import SocketConfig

from .http import api_call


@api_call
def create(name: str, image: str) -> requests.Request:
    return requests.Request(
        method="PUT",
        url="/api/v1/services",
        json={"name": name, "image": image},
    )


@api_call
def get(service: str) -> requests.Request:
    return requests.Request(
        method="GET",
        url=f"/api/v1/services/{service}",
    )


@api_call
def update_instance(service: str, container_id: str, socket: SocketConfig, online: bool) -> requests.Request:
    return requests.Request(
        method="PUT",
        url=f"/api/v1/services/{service}/instances/{container_id}",
        json={**socket.dict(), "online": online},
    )
