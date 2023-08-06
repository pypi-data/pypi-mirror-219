from datetime import datetime, timezone
from typing import List, Optional

import pandas as pd
from pydantic import field_serializer

from foreverbull.models.service import Database, SocketConfig

from .base import Base
from .service import Parameter


class Backtest(Base):
    name: str
    created_at: Optional[datetime] = None
    socket: Optional[SocketConfig] = None
    backtest_service: str
    worker_service: Optional[str] = None
    calendar: str = "XNYS"
    start_time: datetime
    end_time: datetime
    benchmark: str
    symbols: List[str]
    stage: Optional[str] = None
    error: Optional[str] = None

    @field_serializer("start_time")
    def start_time_iso(self, start_time: datetime, _info):
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
        return start_time.isoformat()

    @field_serializer("end_time")
    def end_time_iso(self, end_time: datetime, _info):
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=timezone.utc)
        return end_time.isoformat()


class Execution(Base):
    id: Optional[str] = None
    calendar: str = "XNYS"
    backtest_service: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    benchmark: Optional[str] = None
    symbols: Optional[List[str]] = None
    capital_base: int = 100000
    database: Optional[Database] = None
    parameters: Optional[List[Parameter]] = []
    socket: Optional[SocketConfig] = None


class IngestConfig(Base):
    calendar: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    symbols: List[str] = []


class Period(Base):
    period: datetime = None
    shorts_count: Optional[int] = None
    pnl: Optional[int] = None
    long_value: Optional[int] = None
    short_value: Optional[int] = None
    long_exposure: Optional[int] = None
    starting_exposure: Optional[int] = None
    short_exposure: Optional[int] = None
    capital_used: Optional[int] = None
    gross_leverage: Optional[int] = None
    net_leverage: Optional[int] = None
    ending_exposure: Optional[int] = None
    starting_value: Optional[int] = None
    ending_value: Optional[int] = None
    starting_cash: Optional[int] = None
    ending_cash: Optional[int] = None
    returns: Optional[int] = None
    portfolio_value: Optional[int] = None
    longs_count: Optional[int] = None
    algo_volatility: Optional[int] = None
    sharpe: Optional[int] = None
    alpha: Optional[int] = None
    beta: Optional[int] = None
    sortino: Optional[int] = None
    max_drawdown: Optional[int] = None
    max_leverage: Optional[int] = None
    excess_return: Optional[int] = None
    treasury_period_return: Optional[int] = None
    benchmark_period_return: Optional[int] = None
    benchmark_volatility: Optional[int] = None
    algorithm_period_return: Optional[int] = None

    @classmethod
    def from_backtest(cls, period):
        return Period(
            period=period["period_open"].to_pydatetime().replace(tzinfo=timezone.utc),
            shorts_count=int(period["shorts_count"] * 100),
            pnl=int(period["pnl"] * 100),
            long_value=int(period["long_value"] * 100),
            short_value=int(period["short_value"] * 100),
            long_exposure=int(period["long_exposure"] * 100),
            starting_exposure=int(period["starting_exposure"] * 100),
            short_exposure=int(period["short_exposure"] * 100),
            capital_used=int(period["capital_used"] * 100),
            gross_leverage=int(period["gross_leverage"] * 100),
            net_leverage=int(period["net_leverage"] * 100),
            ending_exposure=int(period["ending_exposure"] * 100),
            starting_value=int(period["starting_value"] * 100),
            ending_value=int(period["ending_value"] * 100),
            starting_cash=int(period["starting_cash"] * 100),
            ending_cash=int(period["ending_cash"] * 100),
            returns=int(period["returns"] * 100),
            portfolio_value=int(period["portfolio_value"] * 100),
            longs_count=int(period["longs_count"] * 100),
            algo_volatility=None if pd.isnull(period["algo_volatility"]) else int(period["algo_volatility"] * 100),
            sharpe=None if pd.isnull(period["sharpe"]) else int(period["sharpe"] * 100),
            alpha=None if period["alpha"] is None or pd.isnull(period["alpha"]) else int(period["alpha"] * 100),
            beta=None if period["beta"] is None or pd.isnull(period["beta"]) else int(period["beta"] * 100),
            sortino=None if pd.isnull(period["sortino"]) else int(period["sortino"] * 100),
            max_drawdown=None if pd.isnull(period["max_drawdown"]) else int(period["max_drawdown"] * 100),
            max_leverage=None if pd.isnull(period["max_leverage"]) else int(period["max_leverage"] * 100),
            excess_return=None if pd.isnull(period["excess_return"]) else int(period["excess_return"] * 100),
            treasury_period_return=None
            if pd.isnull(period["treasury_period_return"])
            else int(period["treasury_period_return"] * 100),
            benchmark_period_return=None
            if pd.isnull(period["benchmark_period_return"])
            else int(period["benchmark_period_return"] * 100),
            benchmark_volatility=None
            if pd.isnull(period["benchmark_volatility"])
            else int(period["benchmark_volatility"] * 100),
            algorithm_period_return=None
            if pd.isnull(period["algorithm_period_return"])
            else int(period["algorithm_period_return"] * 100),
        )


class Result(Base):
    periods: List[Period]
