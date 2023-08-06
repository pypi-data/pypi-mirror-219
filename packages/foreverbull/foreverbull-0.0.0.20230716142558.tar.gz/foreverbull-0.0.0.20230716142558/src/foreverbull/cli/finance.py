from datetime import datetime, timezone
from typing import List

import typer
from typing_extensions import Annotated

from foreverbull import broker

finance = typer.Typer()

asset = typer.Typer()
finance.add_typer(asset, name="asset")

ohlc = typer.Typer()
finance.add_typer(ohlc, name="ohlc")


symbols_argument = Annotated[List[str], typer.Argument(help="symbols to add")]
from_time_option = Annotated[datetime, typer.Option(help="start time")]
to_time_option = Annotated[datetime, typer.Option(help="end time")]


@asset.command()
def add(symbols: symbols_argument):
    broker.finance.add_assets(symbols)


@ohlc.command()
def download(start: from_time_option, end: to_time_option, symbols: symbols_argument = None):
    if not symbols:
        symbols = [asset["symbol"] for asset in broker.finance.get_assets()]
    broker.finance.download_ohlc(symbols, start.replace(tzinfo=timezone.utc), end.replace(tzinfo=timezone.utc))
