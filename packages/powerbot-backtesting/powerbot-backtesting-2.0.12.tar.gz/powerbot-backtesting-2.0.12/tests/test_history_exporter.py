import gzip
import numpy as np
import pandas as pd
import pytest

from datetime import datetime, timezone, timedelta
from pathlib import Path
from powerbot_backtesting import HistoryExporter, ApiExporter
from powerbot_backtesting.models import HistoryApiClient
from helpers import random_params_history_cleanup, random_params_history_no_cleanup  # noqa
from config import config


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_history_no_cleanup")])
def test_history_exporter_init(rndm_params):
    exporter = HistoryExporter(exchange="epex", delivery_area="10YDE-RWENET---I")

    assert isinstance(exporter.client, HistoryApiClient)


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_history_no_cleanup")])
def test_history_exporter_get_historic_data(rndm_params):
    exporter = HistoryExporter(exchange="epex", delivery_area="10YDE-RWENET---I")

    base_path = Path(f"__pb_cache__/history/{exporter.exchange}_{exporter.delivery_area}/{rndm_params['day_from'].strftime('%Y-%m')}")  # noqa: W605
    exchange = "epex"
    delivery_area = "10YDE-RWENET---I"

    # Processing files for both, epex and nordpool -> other exchanges behave like one or the other
    prod_path = Path(
        f"__pb_cache__/prod/{exchange}_{delivery_area}/{rndm_params['day_from'].strftime('%Y-%m')}/"
        f"{rndm_params['day_from'].strftime('%m-%d')}/raw")  # noqa: W605

    exporter = HistoryExporter(exchange=exchange, delivery_area=delivery_area)

    # Process extracted files, while keeping zip file
    transformed_data = exporter.get_historic_data(api_key=rndm_params["history_key"],
                                                  day_from=rndm_params["day_from"],
                                                  extract_files=True,
                                                  process_data=True,
                                                  keep_zip_files=True)

    # Check if directory contains all files as return value
    assert all(i in transformed_data for i in prod_path.iterdir() if i.is_file())

    # Process extracted files, while deleting zip file
    exporter.get_historic_data(api_key=rndm_params["history_key"],
                               day_from=rndm_params["day_from"],
                               extract_files=True,
                               process_data=True,
                               keep_zip_files=False)

    # Check if zip file doesn't exist anymore
    assert not base_path.joinpath(f"{rndm_params['day_from'].strftime('%m-%d')}_public_data.zip").exists()


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_history_no_cleanup")])
def test_history_exporter_get_contracts(rndm_params):
    exchange = "epex"
    delivery_area = "10YDE-RWENET---I"

    exporter = HistoryExporter(exchange=exchange, delivery_area=delivery_area)

    contracts = exporter.get_contracts(time_from=rndm_params["time_from"],
                                       time_till=rndm_params["time_till"],
                                       contract_time="all",
                                       products=rndm_params["product"])

    # Check if output is returned
    assert contracts

    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"],
                                             contract_time="all",
                                             products=rndm_params["product"])

    # Check if output is returned
    assert contract_ids

    # Check if output is right type
    assert isinstance(contracts, list)
    assert all(isinstance(i, dict) for i in contracts)

    # Get contract file to rebuild index
    year_month = rndm_params["day_from"].strftime("%Y-%m")
    day_month = rndm_params["day_from"].strftime("%m-%d")
    file_path = Path(f"./__pb_cache__/prod/{exporter.exchange}_{exporter.delivery_area}/{year_month}/{day_month}/raw")  # noqa: W605

    index = next((i for i in file_path.iterdir() if i.is_file() and "contract" in i.name))
    index = pd.read_json(gzip.open(index))
    index['delivery_start'] = pd.to_datetime(index['delivery_start'])
    index['delivery_end'] = pd.to_datetime(index['delivery_end'])
    index = index.astype({"contract_id": "str"})
    if exchange == "epex":
        index = index.loc[index.undrlng_contracts.isna()]
    else:
        index = index.loc[index.productType != "CUSTOM_BLOCK"]

    # Check if contract ID is in index
    assert all(i["contract_id"] in index.contract_id.to_list() for i in contracts)

    # Check if the same input parameters lead to same contract IDs
    c_ids = index.loc[
        (index._product.isin(rndm_params["product"])) & (index.delivery_start >= str(rndm_params["time_from"].replace(tzinfo=timezone.utc)))
        & (index.delivery_end <= str(rndm_params["time_till"].replace(tzinfo=timezone.utc)))].contract_id.tolist()

    assert c_ids == [i["contract_id"] for i in contracts]


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_history_no_cleanup")])
def test_history_exporter_get_contract_ids(rndm_params):
    exchange = "epex"
    delivery_area = "10YDE-RWENET---I"

    exporter = HistoryExporter(exchange=exchange, delivery_area=delivery_area)

    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"],
                                             contract_time="all",
                                             products=rndm_params["product"])

    # Check if output is returned
    assert contract_ids

    # Check if output is right type
    assert isinstance(contract_ids, dict)

    # Get contract file to rebuild index
    year_month = rndm_params["day_from"].strftime("%Y-%m")
    day_month = rndm_params["day_from"].strftime("%m-%d")
    file_path = Path(f"./__pb_cache__/prod/{exporter.exchange}_{exporter.delivery_area}/{year_month}/{day_month}/raw")  # noqa: W605

    index = next((i for i in file_path.iterdir() if i.is_file() and "contract" in i.name))
    index = pd.read_json(gzip.open(index))
    index['delivery_start'] = pd.to_datetime(index['delivery_start'])
    index['delivery_end'] = pd.to_datetime(index['delivery_end'])
    index = index.astype({"contract_id": "str"})
    if exchange == "epex":
        index = index.loc[index.undrlng_contracts.isna()]
    else:
        index = index.loc[index.productType != "CUSTOM_BLOCK"]

    # Check if contract ID is in index
    assert not index.loc[index.contract_id.isin([i for v in contract_ids.values() for i in v])].empty

    # Check if the same input parameters lead to same contract IDs
    c_ids = index.loc[
        (index._product.isin(rndm_params["product"])) & (index.delivery_start >= str(rndm_params["time_from"].replace(tzinfo=timezone.utc)))
        & (index.delivery_end <= str(rndm_params["time_till"].replace(tzinfo=timezone.utc)))].contract_id.tolist()
    assert c_ids == [i for v in contract_ids.values() for i in v]


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_history_no_cleanup")])
def test_history_exporter_get_public_trades(rndm_params):
    exchange = "epex"
    delivery_area = "10YDE-RWENET---I"

    exporter = HistoryExporter(exchange=exchange, delivery_area=delivery_area)

    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"],
                                             contract_time="all",
                                             products=rndm_params["product"])

    assert contract_ids

    # Load Trades from API and cache locally
    api_trades = exporter.get_public_trades(
        contract_ids=contract_ids,
        contract_time=rndm_params["contract_time"])

    # Check if trades are in the right format
    assert isinstance(api_trades, dict)

    # Check if only trades for the right contracts have been loaded
    # Local contracts might have no trades!
    assert all(len(v.contract_id.unique()) <= len(contract_ids[k]) for k, v in api_trades.items())
    assert all(c in contract_ids[k] for k, v in api_trades.items() for c in v.contract_id.unique())

    # Check VWAP
    vwap_trades = exporter.get_public_trades(contract_ids=contract_ids,
                                             contract_time=rndm_params["contract_time"],
                                             add_vwap=True)

    vwap_columns = ['time_diff', 'cumulated_quantity', 'target_volume', 'vwap']

    # Check for added columns
    assert all(i in v.columns for k, v in vwap_trades.items() for i in vwap_columns)

    # Check for data type
    assert all(v.vwap.dtypes == "float" for v in vwap_trades.values())


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_history_no_cleanup")])
def test_history_exporter_get_contract_history(rndm_params):
    exchange = "epex"
    delivery_area = "10YDE-RWENET---I"

    exporter = HistoryExporter(exchange=exchange, delivery_area=delivery_area)

    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"],
                                             contract_time="all",
                                             products=rndm_params["product"])

    assert contract_ids

    # Load Histories from API and cache locally
    contract_history = exporter.get_contract_history(contract_ids=contract_ids)

    # Check if histories are in the right format
    assert isinstance(contract_history, dict)

    # Check if only histories for the right contracts have been loaded
    assert all(len(v.contract_id.unique()) == len(contract_ids[k]) for k, v in contract_history.items())
    assert all(c in contract_ids[k] for k, v in contract_history.items() for c in v.contract_id.unique())


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_history_no_cleanup")])
def test_history_exporter_get_orders(rndm_params):
    exchange = "epex"
    delivery_area = "10YDE-RWENET---I"

    exporter = HistoryExporter(exchange=exchange, delivery_area=delivery_area)

    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"],
                                             contract_time="all",
                                             products=rndm_params["product"])

    assert contract_ids

    # Load contract history
    contract_history = exporter.get_contract_history(contract_ids=contract_ids)

    # Extract order data from history
    orders = exporter.get_orders(contract_hist_data=contract_history)

    # Check if orders are in the right format
    assert isinstance(orders, dict)

    # Check if all DataFrames have been transformed
    assert len(contract_history) == len(orders)

    # Check for data loss in all individual collections
    for k, v in contract_history.items():
        history_asks = len([x for i in v.loc[v.asks != 0].asks.tolist() for x in i])
        history_bids = len([x for i in v.loc[v.bids != 0].bids.tolist() for x in i])

        assert len(orders[k]) == history_asks + history_bids

    # Check all orders
    all_orders = exporter.get_orders(contract_hist_data=contract_history,
                                     append_all=True)

    # Check if all orders have been appended
    assert len(all_orders) == sum([len(v) for v in orders.values()])


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_history_no_cleanup")])
def test_history_exporter_get_ohlc_data(rndm_params):
    exchange = "epex"
    delivery_area = "10YDE-RWENET---I"

    exporter = HistoryExporter(exchange=exchange, delivery_area=delivery_area)
    api_exporter = ApiExporter(api_key=config['CLIENT_DATA']['API_KEY'], host=config['CLIENT_DATA']['HOST'])

    contract_ids = api_exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                                 time_till=rndm_params["time_till"],
                                                 contract_time="all",
                                                 products=rndm_params["product"])

    # Load trades
    trade_data = exporter.get_public_trades(contract_ids=contract_ids,
                                            contract_time=rndm_params["contract_time"])

    # Process OHLC data
    processed_ohlc = exporter.get_ohlc_data(trade_data=trade_data,
                                            timesteps=rndm_params["timesteps"],
                                            time_unit=rndm_params["time_units"],
                                            use_cached_data=False,
                                            caching=True)

    # Load OHLC data from cache
    cached_ohlc = exporter.get_ohlc_data(trade_data=trade_data,
                                         timesteps=rndm_params["timesteps"],
                                         time_unit=rndm_params["time_units"],
                                         use_cached_data=True,
                                         caching=False)

    # Check if ohlc data is in the right format
    assert isinstance(processed_ohlc, dict)
    assert isinstance(cached_ohlc, dict)

    # Check for same length of processed data
    assert len(trade_data) == len(processed_ohlc) == len(cached_ohlc)

    # Check if processed and cached ohlc data are the same
    assert all(v.compare(cached_ohlc[k]).empty for k, v in processed_ohlc.items())

    # One file generation
    exporter.get_ohlc_data(trade_data=trade_data,
                           timesteps=rndm_params["timesteps"],
                           time_unit=rndm_params["time_units"])


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_history_no_cleanup")])
def test_history_exporter_vwap_by_depth(rndm_params):
    exchange = "epex"
    delivery_area = "10YDE-RWENET---I"
    exporter = HistoryExporter(exchange=exchange, delivery_area=delivery_area)
    api_exporter = ApiExporter(api_key=config['CLIENT_DATA']['API_KEY'], host=config['CLIENT_DATA']['HOST'])

    # Get contract IDs to load trades for
    contract_ids = api_exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                                 time_till=rndm_params["time_till"],
                                                 contract_time="all",
                                                 products=rndm_params["product"])

    assert contract_ids

    # Load contract history
    api_history = exporter.get_contract_history(contract_ids=contract_ids)

    # Extract order data
    orders = exporter.get_orders(contract_hist_data=api_history)

    # Load trade data
    trades = exporter.get_public_trades(contract_ids=contract_ids,
                                        contract_time=rndm_params["contract_time"])

    # Calculate VWAPS for object collections
    order_vwaps = exporter.vwap_by_depth(objects=orders, desired_depth=rndm_params["desired_depth"],
                                         min_depth=rndm_params["min_depth"])
    trade_vwaps = exporter.vwap_by_depth(objects=trades, desired_depth=rndm_params["desired_depth"],
                                         min_depth=rndm_params["min_depth"])

    # Check if there is a VWAP for every key
    assert all(k in [*orders] for k in [*order_vwaps])
    assert all(k in [*trades] for k in [*trade_vwaps])

    # Mock input data to prove output is correct
    mock_100_objects = {[*contract_ids][0]: pd.DataFrame({"price": np.repeat(20, 100), "quantity": np.repeat(1, 100)})}
    mock_5_objects = {[*contract_ids][0]: pd.DataFrame({"price": np.repeat(20, 5), "quantity": np.repeat(1, 5)})}

    # Check if VWAP is correctly calculated to be 20
    mock_vwap_100 = exporter.vwap_by_depth(objects=mock_100_objects, desired_depth=10, min_depth=0.5)
    assert all(v == 20.0 for v in mock_vwap_100.values())

    # Check if all VWAPs equal 0 because min_depth requirement is not satisfied
    mock_vwap_5 = exporter.vwap_by_depth(objects=mock_5_objects, desired_depth=10, min_depth=0.7)
    assert all(v == 0 for v in mock_vwap_5.values())


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_history_no_cleanup")])
def test_history_exporter_vwap_by_timeperiod(rndm_params):
    exchange = "epex"
    delivery_area = "10YDE-RWENET---I"

    exporter = HistoryExporter(exchange=exchange, delivery_area=delivery_area)
    api_exporter = ApiExporter(api_key=config['CLIENT_DATA']['API_KEY'], host=config['CLIENT_DATA']['HOST'])

    # Get contract IDs to load trades for
    contract_ids = api_exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                                 time_till=rndm_params["time_till"],
                                                 contract_time="all",
                                                 products=rndm_params["product"])

    assert contract_ids

    # Load contract history
    api_history = api_exporter.get_contract_history(contract_ids=contract_ids, delivery_area=delivery_area)

    # Extract order data
    orders = exporter.get_orders(contract_hist_data=api_history)

    # Load trade data
    trades = api_exporter.get_public_trades(contract_ids=contract_ids,
                                            contract_time=rndm_params["contract_time"],
                                            delivery_area=delivery_area)

    timestamp = pd.Timestamp((rndm_params["time_from"] - timedelta(hours=3)), tz="UTC")

    # Calculate VWAPS for object collections
    for spec in ["0T-60T-30T", "60T-30T-15T", "60T-60T-0T"]:
        exporter.vwap_by_timeperiod(objects=orders[[*orders][0]], timestamp=timestamp, time_spec=spec)
        exporter.vwap_by_timeperiod(objects=trades[[*trades][0]], timestamp=timestamp, time_spec=spec)

    # Mock input data to prove output is correct
    timestamp_mock = pd.Timestamp((rndm_params["time_from"] - timedelta(hours=2)), tz="UTC")
    for test in [180, 240]:
        mock = pd.DataFrame({"price": np.repeat(20, test),
                             "quantity": np.repeat(1, test),
                             "exec_time": pd.date_range(start=timestamp, periods=test, freq="T")})
        mock.exec_time = pd.to_datetime(mock.exec_time, utc=True)

        assert exporter.vwap_by_timeperiod(objects=mock, timestamp=timestamp_mock) == 20


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_history_cleanup")])
def test_history_exporter_calc_rolling_vwap(rndm_params):
    exchange = "epex"
    delivery_area = "10YDE-RWENET---I"
    exporter = HistoryExporter(exchange=exchange, delivery_area=delivery_area)
    api_exporter = ApiExporter(api_key=config['CLIENT_DATA']['API_KEY'], host=config['CLIENT_DATA']['HOST'])

    # Get contract IDs to load trades for
    contract_ids = api_exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                                 time_till=rndm_params["time_till"],
                                                 contract_time="all",
                                                 products=rndm_params["product"])

    assert contract_ids

    # Load trade data
    trades = exporter.get_public_trades(contract_ids=contract_ids,
                                        contract_time=rndm_params["contract_time"])

    trade_vwaps = exporter.calc_rolling_vwap(trades=trades)

    # Check if vwap column exists and holds data
    for v in trade_vwaps.values():
        assert "vwap_1h" in v.columns
        assert not v["vwap_1h"].isnull().values.any()

    # Mock input data to prove output is correct
    mock_dates = [datetime(2021, 1, 1, 10, 0, 0) + timedelta(minutes=i) for i in range(0, 100)]
    mock_100_objects = {[*contract_ids][0]: pd.DataFrame({"exec_time": mock_dates, "price": np.repeat(20, 100), "quantity": np.repeat(1, 100)})}

    # Check if VWAP is correctly calculated to be 20 for each item
    mock_vwap_100 = exporter.calc_rolling_vwap(trades=mock_100_objects)
    assert all(len(i.vwap_1h.unique()) == 1 and i.vwap_1h.unique()[0] == 20 for i in mock_vwap_100.values())
