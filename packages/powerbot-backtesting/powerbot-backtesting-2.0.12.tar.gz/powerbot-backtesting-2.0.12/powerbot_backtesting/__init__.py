# Version
from pbr.version import VersionInfo

__version__ = VersionInfo('powerbot_backtesting').version_string()

from powerbot_backtesting.models.backtesting_models import BacktestingAlgo, BatteryBacktestingAlgo  # noqa: F401
from powerbot_backtesting.models.exporter_models import ApiExporter, HistoryExporter, SqlExporter, init_client  # noqa: F401
