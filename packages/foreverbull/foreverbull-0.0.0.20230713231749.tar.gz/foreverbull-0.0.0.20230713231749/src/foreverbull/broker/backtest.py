import requests

from foreverbull import models

from .http import api_call


@api_call
def create(backtest: models.backtest.Backtest) -> requests.Request:
    return requests.Request(
        method="PUT",
        url="/api/v1/backtests",
        json=backtest.model_dump(),
    )


@api_call
def get(name: str) -> requests.Request:
    return requests.Request(
        method="GET",
        url=f"/api/v1/backtests/{name}",
    )


@api_call
def start(name: str) -> requests.Request:
    return requests.Request(
        method="PUT",
        url=f"/api/v1/backtests/{name}/start",
    )


@api_call
def get_execution(execution_id: str) -> requests.Request:
    return requests.Request(
        method="GET",
        url=f"/api/v1/backtests/executions/{execution_id}",
    )
