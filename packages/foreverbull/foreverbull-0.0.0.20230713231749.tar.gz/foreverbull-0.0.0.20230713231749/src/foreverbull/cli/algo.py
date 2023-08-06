import importlib
import os
import signal
import socket

import typer
from rich.console import Console
from typing_extensions import Annotated

from foreverbull import Foreverbull, broker

strategy_option = Annotated[str, typer.Option(help="strategy to run")]
broker_url_option = Annotated[str, typer.Option(help="broker to use")]
file_name_argument = Annotated[str, typer.Argument(help="file name")]
local_host_option = Annotated[str, typer.Option(help="local host")]
local_port_option = Annotated[str, typer.Option(help="local port")]

local_hostname = socket.gethostbyname(socket.gethostname())


algo = typer.Typer()

std = Console()
std_err = Console(stderr=True)


def import_algo(file_name: str):
    try:
        importlib.import_module(file_name.replace("/", ".").split(".py")[0])
    except Exception as e:
        std_err.log(f"Could not import {file_name}: {e}")
        exit(1)


@algo.command()
def start(
    file_name: file_name_argument,
):
    std.log("importing :", file_name)
    import_algo(file_name)
    fb = Foreverbull()
    fb.setup()
    fb.start()
    signal.signal(signal.SIGINT, lambda x, y: fb.stop())

    try:
        broker.service.update_instance(os.environ.get("SERVICE_NAME"), socket.gethostname(), fb.socket_config, True)
        std.log("Running")
        signal.pause()
        broker.service.update_instance(os.environ.get("SERVICE_NAME"), socket.gethostname(), fb.socket_config, False)
        std.log("Exiting")
    except Exception as e:
        std_err.log("error during run of backtest: ", repr(e))
        return
    finally:
        fb.stop()
