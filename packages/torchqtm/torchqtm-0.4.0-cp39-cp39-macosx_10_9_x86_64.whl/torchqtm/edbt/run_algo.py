import pandas as pd
import typing

import talib

from torchqtm.edbt.algorithm import TradingAlgorithm
from torchqtm.edbt.sim_params import SimulationParameters

from torchqtm.finance.account import Account
from torchqtm.finance.metrics.tracker import MetricsTracker
from torchqtm.utils.calendar_utils import get_calendar
from torchqtm.utils.datetime_utils import DateTimeManager
from torchqtm.types import DATA_FREQUENCIES
from torchqtm.data.data_portal import DataPortal
from torchqtm.assets import Equity
from torchqtm.finance.metrics.loader import DEFAULT_METRICS


# Design a time machine


class run_algo(object):
    def __init__(
            self,
            Algo: typing.Type[TradingAlgorithm],
            data_frequency: DATA_FREQUENCIES,
            capital_base: float,
            bundle: str,
            start: pd.Timestamp,
            end: pd.Timestamp,
            output,
            trading_calendar,
            metrics_set,
            local_namespace,
            environ,
            account_configs,
            benchmark_spec,
    ):

        if trading_calendar is None:
            trading_calendar = get_calendar("XSHG")
        datetime_manager = DateTimeManager(trading_calendar)

        # benchmark_symbol, benchmark_returns = benchmark_spec.resolve(start, end)
        benchmark_symbol, benchmark_returns = (0, 0)

        data_portal = DataPortal(
            data_frequency=data_frequency,
            trading_calendar=datetime_manager.trading_calendar,
            datetime_manager=datetime_manager,
            restrictions=None,
        )

        sim_params = SimulationParameters(
            start_session=start,
            end_session=end,
            trading_calendar=trading_calendar,
            capital_base=capital_base,
            data_frequency=data_frequency,
        )

        account = Account(
            datetime_manager=datetime_manager,
            trading_sessions=trading_calendar.sessions_in_range(start, end),
            capital_base=capital_base,
            data_frequency=data_frequency,
        )

        metrics_tracker = MetricsTracker(
            trading_calendar=trading_calendar,
            first_session=start,
            last_session=end,
            capital_base=capital_base,
            emission_rate=data_frequency,
            data_frequency=data_frequency,
            account=account,
            metrics=metrics_set,
        )

        algo = Algo(
            sim_params=sim_params,
            data_portal=data_portal,
            namespace=None,
            trading_calendar=datetime_manager.trading_calendar,
            datetime_manager=datetime_manager,
            benchmark_returns=benchmark_returns,
            account=account,
            metrics_tracker=metrics_tracker,
        )

        it = iter(algo.get_generator())
        while True:
            try:
                next(it)
            except StopIteration:
                break


class TestAlgo(TradingAlgorithm):
    def initialize(self):
        self.safe_set_attr("sym", Equity("000001.XSHE"))
        self.safe_set_attr("count", 0)

    def before_trading_start(self):
        pass

    def handle_data(self):
        for i in range(300):
            prices = self.history(self.sym, 'close', 21, "daily")

        short_avg = talib.SMA(prices, 5)
        long_avg = talib.SMA(prices, 20)

        current_position = self.account.get_position(self.sym)
        if short_avg[-1] - long_avg[-1] < 0 and short_avg[-2] - long_avg[-2] > 0 and current_position.amount > 0:
            self.order(self.sym, -100)

        if short_avg[-1] - long_avg[-1] > 0 and short_avg[-2] - long_avg[-2] < 0:
            for i in range(100):
                self.order(self.sym, 10)

    def analyze(self):
        print(self.account.ledger.cash)
        print(self.account.ledger.portfolio_value)


import sys


def print_progress(progress):
    '''
    progress 是一个介于0和1之间的浮点数，代表当前进度
    '''
    bar_length = 50  # 进度条的长度，你可以根据自己的需求进行修改
    assert 0 <= progress <= 1

    # 计算已完成部分和未完成部分的长度
    completed_length = int(bar_length * progress)
    uncompleted_length = bar_length - completed_length

    # 创建进度条字符串
    progress_bar = '[' + '#' * completed_length + '-' * uncompleted_length + ']'

    # 在同一行打印进度条和进度百分比
    sys.stdout.write("\r" + progress_bar + ' {:.2f}%'.format(progress * 100))
    sys.stdout.flush()


if __name__ == "__main__":
    Algo = TestAlgo
    data_frequency: DATA_FREQUENCIES = "daily"
    capital_base = 1e6
    bundle = "rqalpha"
    start = pd.Timestamp("20160101")
    end = pd.Timestamp("20220101")
    output = None
    trading_calendar = None
    metrics_set = DEFAULT_METRICS
    local_namespace = None
    environ = None
    account_configs = None
    benchmark_spec = None

    run_algo(
        Algo=Algo,
        data_frequency=data_frequency,
        capital_base=capital_base,
        bundle=bundle,
        start=start,
        end=end,
        output=output,
        trading_calendar=trading_calendar,
        metrics_set=metrics_set,
        local_namespace=local_namespace,
        environ=environ,
        account_configs=account_configs,
        benchmark_spec=benchmark_spec,
    )
