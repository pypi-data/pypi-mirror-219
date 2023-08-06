import socket
from datetime import datetime
from typing import List

import typer
from rich.console import Console
from typing_extensions import Annotated

from foreverbull import broker, models

name = Annotated[str, typer.Option(help="strategy to run")]
broker_url_option = Annotated[str, typer.Option(help="broker to use")]
file_name_argument = Annotated[str, typer.Argument(help="file name")]
local_host_option = Annotated[str, typer.Option(help="local host")]
local_port_option = Annotated[str, typer.Option(help="local port")]

name_argument = Annotated[str, typer.Argument(help="name of the backtest")]
backtest_service_option = Annotated[str, typer.Option(help="backtest service to use")]
start_option = Annotated[datetime, typer.Option(help="start time of the backtest")]
end_option = Annotated[datetime, typer.Option(help="end time of the backtest")]
symbol_option = Annotated[
    List[str], typer.Option(help="symbol to use, require multiple --symbol entries for multiple values")
]
benchmark_option = Annotated[str, typer.Option(help="benchmark to use")]

try:
    local_hostname = socket.gethostbyname(socket.gethostname())
except socket.gaierror:
    local_hostname = socket.gethostbyname("localhost")

backtest = typer.Typer()

std = Console()
std_err = Console(stderr=True)


@backtest.command()
def list():
    pass


@backtest.command()
def create(
    name: name_argument,
    backtest_service: backtest_service_option,
    start: start_option,
    end: end_option,
    symbol: symbol_option,
    benchmark: benchmark_option,
):
    backtest = models.backtest.Backtest(
        name=name,
        backtest_service=backtest_service,
        start_time=start,
        end_time=end,
        symbols=symbol,
        benchmark=benchmark,
    )
    backtest = broker.backtest.create(backtest)
    std.print(backtest)


@backtest.command()
def ingest(backtest_name: name_argument):
    return broker.backtest.ingest(backtest_name)


@backtest.command()
def get(backtest_name: name_argument):
    std.print(broker.backtest.get(backtest_name))
