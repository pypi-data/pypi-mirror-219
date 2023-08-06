from datetime import datetime, timedelta
from random import randint, choice, uniform
import pytest
from powerbot_backtesting import ApiExporter, SqlExporter
from powerbot_backtesting.utils import init_client
from powerbot_backtesting.utils.constants import PRODUCTS
from tests.config import config
from tests.helpers import do_cleanup


@pytest.fixture
def random_params_api():
    time_from = datetime.today().replace(hour=randint(0, 23), minute=0, second=0, microsecond=0) - timedelta(days=1)
    time_till = time_from + timedelta(hours=1)
    contract_time = choice(["hourly", "quarter-hourly"])
    product = list(PRODUCTS[contract_time])

    rndm_params = {"client": init_client(config['CLIENT_DATA']['API_KEY'], config['CLIENT_DATA']['HOST']),
                   "api_exporter": ApiExporter(api_key=config['CLIENT_DATA']['API_KEY'],
                                               host=config['CLIENT_DATA']['HOST']),
                   "product": product,
                   "time_from": time_from,
                   "time_till": time_till,
                   "contract_time": contract_time,
                   "delivery_area": config['CONTRACT_DATA']['DELIVERY_AREA'],
                   "portfolio": config['CONTRACT_DATA']['PORTFOLIO'],
                   "previous_days": randint(1, 5),
                   "timesteps": choice([5, 10, 15]),
                   "time_units": "minutes",
                   "desired_depth": randint(5, 15),
                   "min_depth": round(uniform(0.1, 0.3), 2)}
    yield rndm_params
    try:
        do_cleanup()
    except:  # noqa: E722
        pass


def random_params_history():
    # day_from = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=30)
    # time_from = datetime.today().replace(hour=randint(0, 23), minute=0, second=0, microsecond=0) - timedelta(days=30)
    day_from = config['CONTRACT_DATA']['TIME_FROM'].replace(hour=0)
    time_from = day_from.replace(hour=randint(0, 23), minute=0, second=0, microsecond=0)
    time_till = time_from + timedelta(hours=1)
    contract_time = choice(["hourly", "quarter-hourly"])
    product = list(PRODUCTS[contract_time])

    rndm_params = {"history_key": config['CLIENT_DATA']['HISTORY_KEY'],
                   "api_key": config['CLIENT_DATA']['API_KEY'],
                   "product": product,
                   "time_from": time_from,
                   "time_till": time_till,
                   "day_from": day_from,
                   "contract_time": contract_time,
                   "previous_days": randint(1, 5),
                   "timesteps": choice([5, 10, 15]),
                   "time_units": "minutes",
                   "desired_depth": randint(5, 15),
                   "min_depth": round(uniform(0.1, 0.3), 2)}

    return rndm_params


@pytest.fixture
def random_params_history_no_cleanup():
    yield random_params_history()


@pytest.fixture
def random_params_history_cleanup():
    yield random_params_history()
    try:
        do_cleanup()
    except WindowsError:
        pass


@pytest.fixture
def random_params_sql():
    rndm_params = {"sql_exporter": SqlExporter(db_type=config['SQL_DATA']['DB_TYPE'],
                                               user=config['SQL_DATA']['USER'],
                                               password=config['SQL_DATA']['PASSWORD'],
                                               host=config['SQL_DATA']['DB_HOST'],
                                               database=config['SQL_DATA']['DATABASE'],
                                               port=config['SQL_DATA']['PORT']),
                   "time_from": config['CONTRACT_DATA']['SQL_TIME_FROM'],
                   "time_till": config['CONTRACT_DATA']['SQL_TIME_TILL'],
                   "exchange": config['CONTRACT_DATA']['EXCHANGE'],
                   "contract_time": "hourly",
                   "delivery_area": config['CONTRACT_DATA']['DELIVERY_AREA'],
                   "previous_days": randint(1, 5),
                   "timesteps": choice([5, 10, 15]),
                   "time_units": "minutes",
                   "desired_depth": randint(5, 15),
                   "min_depth": round(uniform(0.1, 0.3), 2)}
    yield rndm_params
    try:
        do_cleanup()
    except WindowsError:
        pass
