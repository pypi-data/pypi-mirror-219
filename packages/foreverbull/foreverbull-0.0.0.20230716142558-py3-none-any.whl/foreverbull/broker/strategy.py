import requests

from .http import api_call


@api_call
def create(name: str, worker: str, backtest: str, backtest_config: dict) -> requests.Request:
    return requests.Request(
        method="PUT",
        url="/api/v1/strategies",
        json={"name": name, "backtest": backtest, "worker": worker, "backtest_config": backtest_config},
    )


@api_call
def get(name: str) -> requests.Request:
    return requests.Request(
        method="GET",
        url=f"/api/v1/strategies/{name}",
    )
