from datetime import datetime, timedelta, timezone
from pathlib import Path
from random import randint

import numpy as np
import pandas as pd
import pytest

from powerbot_backtesting import SqlExporter
from powerbot_backtesting.utils.constants import DATE_YMD_TIME_HM_ALT, DATE_YMD_TIME_HMS
from tests.helpers import random_params_sql  # noqa


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_sql")])
def test_sql_exporter_create_sql_engine(rndm_params):
    exporter = rndm_params["sql_exporter"]

    # Check if class was initialized correctly
    assert isinstance(exporter, SqlExporter)

    # Check if SQL engine was created correctly
    assert exporter.engine


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_sql")])
def test_sql_exporter_get_contracts(rndm_params):
    exporter = rndm_params["sql_exporter"]

    # Load Contracts as Dataframe
    contracts_df = exporter.get_contracts(delivery_start=rndm_params["time_from"],
                                          delivery_end=rndm_params["time_till"])

    # Check if return value is in correct type
    assert isinstance(contracts_df, pd.DataFrame)

    # Load Contracts as List
    contracts_list = exporter.get_contracts(delivery_start=rndm_params["time_from"],
                                            delivery_end=rndm_params["time_till"],
                                            as_dataframe=False)

    # Check if return value is in correct type
    assert isinstance(contracts_list, list)


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_sql")])
def test_sql_exporter_get_contract_ids(rndm_params):
    exporter = rndm_params["sql_exporter"]

    # Load Contract IDs from SQL
    sql_contracts_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                                  time_till=rndm_params["time_till"],
                                                  delivery_area=rndm_params["delivery_area"],
                                                  contract_time="all",
                                                  exchange=rndm_params["exchange"])
    # Check if return value is not empty
    assert sql_contracts_ids

    # Check if return value is in correct type
    assert isinstance(sql_contracts_ids, dict)
    assert all(isinstance(i, list) for i in sql_contracts_ids.values())

    t_from = rndm_params["time_from"]
    t_till = rndm_params["time_till"]
    d_area = rndm_params["delivery_area"]
    ex = rndm_params["exchange"]

    raw = exporter.send_raw_sql(
        f"SELECT contract_id FROM contracts WHERE delivery_start >= '{t_from}' "
        f"AND delivery_end <= '{t_till}' AND delivery_areas LIKE '%{d_area}%' "
        "AND product IN ('XBID_Hour_Power', 'Intraday_Hour_Power', 'GB_Hour_Power', 'P60MIN', 'Hourly_BSP', 'Hour_Power_Local_OTC',"
        " 'Hour_Power_Local', 'XBID_Quarter_Hour_Power', 'Intraday_Quarter_Hour_Power', 'GB_Quarter_Hour_Power', 'P15MIN', 'Quarterly_BSP', "
        "'Quarter_Hour_Power_Local', 'XBID_Half_Hour_Power', 'Intraday_Half_Hour_Power', 'GB_Half_Hour_Power', 'P30MIN', 'Continuous_Power_Peak', "
        "'Continuous_Power_Base') "
        f"AND exchange = '{ex}'")
    # Deflate
    raw = [x for i in raw for x in i]

    # Check if there is no data loss during format transformation
    assert all(i in raw for v in sql_contracts_ids.values() for i in v)


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_sql")])
def test_sql_exporter_get_public_trades(rndm_params):
    exporter = rndm_params["sql_exporter"]

    # Load Contract IDs
    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"],
                                             delivery_area=rndm_params["delivery_area"],
                                             contract_time=rndm_params["contract_time"],
                                             exchange=rndm_params["exchange"])
    # Check if return value is not empty
    assert contract_ids

    # Load Trades from SQL
    sql_trades = exporter.get_public_trades(contract_id=contract_ids,
                                            delivery_area=[rndm_params["delivery_area"]],
                                            as_dataframe=True,
                                            caching=True,
                                            use_cached_data=False)

    # Check if return value is in correct type
    assert isinstance(sql_trades, dict)
    assert all(isinstance(i, pd.DataFrame) for i in sql_trades.values())

    # Load from cache
    cache_trades = exporter.get_public_trades(contract_id=contract_ids,
                                              delivery_area=[rndm_params["delivery_area"]],
                                              as_dataframe=True,
                                              use_cached_data=True)

    assert all(i in cache_trades for i in sql_trades)


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_sql")])
def test_sql_exporter_get_contract_history(rndm_params):
    exporter = rndm_params["sql_exporter"]

    # Load Contract IDs
    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"],
                                             delivery_area=rndm_params["delivery_area"],
                                             contract_time=rndm_params["contract_time"],
                                             exchange=rndm_params["exchange"])
    # Check if return value is not empty
    assert contract_ids

    # Load Contract History from SQL
    sql_contract_history = exporter.get_contract_history(contract_id=contract_ids,
                                                         delivery_area=[rndm_params["delivery_area"]],
                                                         as_dataframe=True,
                                                         caching=True)

    # Check if return value is in correct type
    assert isinstance(sql_contract_history, dict)
    assert all(isinstance(i, pd.DataFrame) for i in sql_contract_history.values())

    # Load from cache
    cache_contract_history = exporter.get_contract_history(contract_id=contract_ids,
                                                           delivery_area=[rndm_params["delivery_area"]],
                                                           as_dataframe=True,
                                                           use_cached_data=True,
                                                           caching=False)

    assert all(i in cache_contract_history for i in sql_contract_history)


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_sql")])
def test_sql_exporter_get_own_trades(rndm_params):
    exporter = rndm_params["sql_exporter"]

    # Load Contract IDs
    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"],
                                             delivery_area=rndm_params["delivery_area"],
                                             contract_time=rndm_params["contract_time"],
                                             exchange="epex")
    # Check if return value is not empty
    assert contract_ids

    # Load Trades from SQL
    sql_own_trades = exporter.get_own_trades(contract_id=contract_ids,
                                             delivery_area=[rndm_params["delivery_area"]],
                                             as_dataframe=True)

    # Check if return value is in correct type
    assert isinstance(sql_own_trades, pd.DataFrame)


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_sql")])
def test_sql_exporter_get_internal_trades(rndm_params):
    exporter = rndm_params["sql_exporter"]

    # Load Contract IDs
    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"],
                                             delivery_area=rndm_params["delivery_area"],
                                             contract_time=rndm_params["contract_time"],
                                             exchange="epex")
    # Check if return value is not empty
    assert contract_ids

    # Load Trades from SQL
    sql_internal_trades = exporter.get_internal_trades(contract_id=contract_ids,
                                                       delivery_area=[rndm_params["delivery_area"]],
                                                       as_dataframe=True)

    # Check if return value is in correct type
    assert isinstance(sql_internal_trades, pd.DataFrame)


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_sql")])
def test_sql_exporter_get_signals(rndm_params):
    exporter = rndm_params["sql_exporter"]

    # Load Trades from SQL
    sql_signals = exporter.get_signals(time_from=rndm_params["time_from"],
                                       time_till=rndm_params["time_till"],
                                       delivery_areas=[rndm_params["delivery_area"]],
                                       as_dataframe=True)

    # Check if return value is in correct type
    assert isinstance(sql_signals, pd.DataFrame)


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_sql")])
def test_sql_exporter_send_raw_sql(rndm_params):
    exporter = rndm_params["sql_exporter"]

    # Load Contract IDs from SQL
    contracts_df = exporter.get_contracts(delivery_start=rndm_params["time_from"],
                                          delivery_end=rndm_params["time_till"],
                                          as_dataframe=False)

    t_from = rndm_params["time_from"]
    t_till = rndm_params["time_till"]

    raw = exporter.send_raw_sql(f"SELECT * FROM contracts WHERE delivery_start = '{t_from}' AND delivery_end = '{t_till}'")

    # Check if return values match
    assert all(i in raw for i in contracts_df)


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_sql")])
def test_sql_exporter_get_orders(rndm_params):
    exporter = rndm_params["sql_exporter"]

    # Load Contract IDs
    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"],
                                             delivery_area=rndm_params["delivery_area"],
                                             contract_time=rndm_params["contract_time"],
                                             exchange=rndm_params["exchange"])
    # Check if return value is not empty
    assert contract_ids

    # Load Contract History from SQL
    sql_contract_history = exporter.get_contract_history(contract_id=contract_ids,
                                                         delivery_area=[rndm_params["delivery_area"]],
                                                         as_dataframe=True,
                                                         use_cached_data=False,
                                                         caching=False)
    # Extract order data from history
    orders = exporter.get_orders(sql_contract_history)

    # Check if orders are in the right format
    assert isinstance(orders, dict)

    # Check if all DataFrames have been transformed
    assert len(sql_contract_history) == len(orders)

    # Check for data loss in all individual collections
    for k, v in sql_contract_history.items():
        history_asks = len([x for i in v.loc[v.asks != 0].asks.tolist() for x in i])
        history_bids = len([x for i in v.loc[v.bids != 0].bids.tolist() for x in i])

        assert len(orders[k]) == history_asks + history_bids


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_sql")])
def test_sql_exporter_get_ohlc_data(rndm_params):
    exporter = rndm_params["sql_exporter"]

    # Load Contract IDs
    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"],
                                             delivery_area=rndm_params["delivery_area"],
                                             contract_time=rndm_params["contract_time"],
                                             exchange=rndm_params["exchange"])
    # Check if return value is not empty
    assert contract_ids

    # Load Trades from SQL
    sql_trades = exporter.get_public_trades(contract_id=contract_ids,
                                            delivery_area=[rndm_params["delivery_area"]],
                                            as_dataframe=True)

    # Process OHLC data
    processed_ohlc = exporter.get_ohlc_data(
        trade_data=sql_trades,
        delivery_area=rndm_params["delivery_area"],
        timesteps=rndm_params["timesteps"],
        time_unit=rndm_params["time_units"],
        use_cached_data=False,
        caching=True)

    # Load OHLC data from cache
    cached_ohlc = exporter.get_ohlc_data(
        trade_data=sql_trades,
        delivery_area=rndm_params["delivery_area"],
        timesteps=rndm_params["timesteps"],
        time_unit=rndm_params["time_units"],
        use_cached_data=True,
        caching=False)

    # Check if ohlc data is in the right format
    assert isinstance(processed_ohlc, dict)
    assert isinstance(cached_ohlc, dict)

    # Check for same length of processed data
    assert len(sql_trades) == len(processed_ohlc) == len(cached_ohlc)

    # Check if processed and cached ohlc data are the same
    assert all(v.compare(cached_ohlc[k]).empty for k, v in processed_ohlc.items())

    # One file generation
    exporter.get_ohlc_data(trade_data=sql_trades,
                           delivery_area=rndm_params["delivery_area"],
                           timesteps=rndm_params["timesteps"],
                           time_unit=rndm_params["time_units"],
                           one_file=True)

    # Check if file was created
    cache_path = Path("__pb_cache__").joinpath(f"prod\\{rndm_params['exchange']}_{rndm_params['delivery_area']}\\"
                                               f"{rndm_params['time_from'].strftime('%Y-%m')}\\"
                                               f"{rndm_params['time_from'].strftime('%m-%d')}\\processed")

    if len(contract_ids) == 1:
        assert cache_path.joinpath(
            f"all_ohlc_{rndm_params['time_from'].strftime(DATE_YMD_TIME_HM_ALT)}_{rndm_params['timesteps']}"
            f"{rndm_params['time_units'][0]}.json.gz").exists()
    else:
        assert cache_path.joinpath(
            f"all_ohlc_{rndm_params['time_from'].strftime(DATE_YMD_TIME_HM_ALT)} - {rndm_params['time_till'].strftime(DATE_YMD_TIME_HM_ALT)}_"
            f"{rndm_params['timesteps']}{rndm_params['time_units'][0]}.json.gz").exists()


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_sql")])
def test_sql_exporter_get_orderbooks(rndm_params):
    exporter = rndm_params["sql_exporter"]

    # Load Contract IDs
    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"],
                                             delivery_area=rndm_params["delivery_area"],
                                             contract_time=rndm_params["contract_time"],
                                             exchange=rndm_params["exchange"])
    # Check if return value is not empty
    assert contract_ids

    # Load Contract History from SQL
    sql_contract_history = exporter.get_contract_history(contract_id=contract_ids,
                                                         delivery_area=[rndm_params["delivery_area"]],
                                                         as_dataframe=True)

    # Process orderbook
    processed_orderbooks = exporter.get_orderbooks(contract_hist_data=sql_contract_history,
                                                   delivery_area=rndm_params["delivery_area"],
                                                   timesteps=rndm_params["timesteps"],
                                                   time_unit=rndm_params["time_units"],
                                                   caching=True)

    # Load orderbooks from cache
    cached_orderbooks = exporter.get_orderbooks(contract_hist_data=sql_contract_history,
                                                delivery_area=rndm_params["delivery_area"],
                                                timesteps=rndm_params["timesteps"],
                                                time_unit=rndm_params["time_units"],
                                                caching=False)

    # Check if order books are in the right format
    assert isinstance(processed_orderbooks, dict)
    assert isinstance(cached_orderbooks, dict)

    # Check for same length of processed data
    assert len(sql_contract_history) == len(processed_orderbooks) == len(cached_orderbooks)

    # Check if processed and cached order books are the same
    for k, v in processed_orderbooks.items():
        for kx, x in v.items():
            assert x.compare(cached_orderbooks[k][kx]).empty

    # Process orderbooks in shortest interval
    exporter.get_orderbooks(contract_hist_data=sql_contract_history,
                            delivery_area=rndm_params["delivery_area"],
                            shortest_interval=True,
                            use_cached_data=False,
                            caching=True)

    # Process orerbooks at timestamp
    timestamp = [rndm_params["time_from"] - timedelta(hours=randint(2, 5)) for _ in range(len(contract_ids))]

    timestamp_orderbooks = exporter.get_orderbooks(contract_hist_data=sql_contract_history,
                                                   delivery_area=rndm_params["delivery_area"],
                                                   timestamp=timestamp,
                                                   use_cached_data=False,
                                                   caching=False)

    # Check for same length of processed data
    assert len(sql_contract_history) == len(timestamp_orderbooks)

    # Check if there is only one or less single order book per time period
    assert all(len(v) <= 1 for k, v in timestamp_orderbooks.items())

    # Check if correct times provided by timestamps have been used
    assert all([[*v][0] == timestamp[nr].replace(tzinfo=timezone.utc) for nr, (k, v) in enumerate(timestamp_orderbooks.items()) if [*v]])

    # Process orerbooks starting from timestamp
    timestamp = [rndm_params["time_from"] - timedelta(hours=randint(2, 5)) for _ in range(len(contract_ids))]

    from_timestamp_orderbooks = exporter.get_orderbooks(contract_hist_data=sql_contract_history,
                                                        delivery_area=rndm_params["delivery_area"],
                                                        timestamp=timestamp,
                                                        timesteps=rndm_params["timesteps"],
                                                        time_unit=rndm_params["time_units"],
                                                        use_cached_data=False,
                                                        caching=False)

    # Check for same length of processed data
    assert len(sql_contract_history) == len(from_timestamp_orderbooks)

    # Check if correct times provided by timestamps have been used
    assert all([[*v][0] == timestamp[nr].replace(tzinfo=timezone.utc) for nr, (k, v) in enumerate(from_timestamp_orderbooks.items()) if [*v]])

    # JSON-file generation
    exporter.get_orderbooks(contract_hist_data=sql_contract_history,
                            delivery_area=rndm_params["delivery_area"],
                            timestamp=timestamp,
                            timesteps=rndm_params["timesteps"],
                            time_unit=rndm_params["time_units"],
                            as_json=True)

    # Check if file was created
    cache_path = Path("__pb_cache__").joinpath(
        f"prod\\{rndm_params['exchange']}_{rndm_params['delivery_area']}\\{rndm_params['time_from'].strftime('%Y-%m')}\\"
        f"{rndm_params['time_from'].strftime('%m-%d')}\\processed")

    if len(contract_ids) == 1:
        assert cache_path.joinpath(f"orderbook_{rndm_params['time_from'].strftime(DATE_YMD_TIME_HM_ALT)}_"
                                   f"{rndm_params['timesteps']}{rndm_params['time_units'][0]}.json.gz").exists()
    else:
        assert cache_path.joinpath(f"orderbook_{rndm_params['time_from'].strftime(DATE_YMD_TIME_HM_ALT)} - "
                                   f"{rndm_params['time_till'].strftime(DATE_YMD_TIME_HM_ALT)}_{rndm_params['timesteps']}"
                                   f"{rndm_params['time_units'][0]}.json.gz").exists()

    # Assert shortest interval was saved
    assert cache_path.joinpath(
        f"{rndm_params['time_from'].strftime(DATE_YMD_TIME_HM_ALT)} - "
        f"{rndm_params['time_till'].strftime(DATE_YMD_TIME_HM_ALT)}_orderbook_shortest.p").exists()


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_sql")])
def test_sql_exporter_vwap_by_depth(rndm_params):
    exporter = rndm_params["sql_exporter"]

    # Load Contract IDs
    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"],
                                             delivery_area=rndm_params["delivery_area"],
                                             contract_time=rndm_params["contract_time"],
                                             exchange=rndm_params["exchange"])
    # Check if return value is not empty
    assert contract_ids

    # Load Contract History from SQL
    sql_contract_history = exporter.get_contract_history(contract_id=contract_ids,
                                                         delivery_area=[rndm_params["delivery_area"]],
                                                         as_dataframe=True)
    # Extract order data
    orders = exporter.get_orders(contract_hist_data=sql_contract_history)

    # Load Trades from SQL
    sql_trades = exporter.get_public_trades(contract_id=contract_ids,
                                            delivery_area=[rndm_params["delivery_area"]],
                                            as_dataframe=True)

    # Calculate VWAPS for object collections
    order_vwaps = exporter.vwap_by_depth(objects=orders, desired_depth=rndm_params["desired_depth"],
                                         min_depth=rndm_params["min_depth"])
    trade_vwaps = exporter.vwap_by_depth(objects=sql_trades, desired_depth=rndm_params["desired_depth"],
                                         min_depth=rndm_params["min_depth"])

    # Check if there is a VWAP for every key
    assert all(k in [*orders] for k in [*order_vwaps])
    assert all(k in [*sql_trades] for k in [*trade_vwaps])

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
                         [pytest.lazy_fixture("random_params_sql")])
def test_sql_exporter_vwap_by_timeperiod(rndm_params):
    exporter = rndm_params["sql_exporter"]

    # Load Contract IDs
    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"],
                                             delivery_area=rndm_params["delivery_area"],
                                             contract_time=rndm_params["contract_time"],
                                             exchange=rndm_params["exchange"])
    # Check if return value is not empty
    assert contract_ids

    # Load Contract History from SQL
    sql_contract_history = exporter.get_contract_history(contract_id=contract_ids,
                                                         delivery_area=[rndm_params["delivery_area"]],
                                                         as_dataframe=True)
    # Extract order data
    orders = exporter.get_orders(contract_hist_data=sql_contract_history)

    # Load Trades from SQL
    sql_trades = exporter.get_public_trades(contract_id=contract_ids,
                                            delivery_area=[rndm_params["delivery_area"]],
                                            as_dataframe=True)

    timestamp = (rndm_params["time_from"] - timedelta(hours=3)).strftime(DATE_YMD_TIME_HMS)

    # Calculate VWAPS for object collections
    for spec in ["0T-60T-30T", "60T-30T-15T", "60T-60T-0T"]:
        exporter.vwap_by_timeperiod(objects=orders[[*orders][0]], timestamp=timestamp, time_spec=spec)
        exporter.vwap_by_timeperiod(objects=sql_trades[[*sql_trades][0]], timestamp=timestamp, time_spec=spec)

    # Mock input data to prove output is correct
    timestamp_mock = (rndm_params["time_from"] - timedelta(hours=2)).strftime(DATE_YMD_TIME_HMS)
    for test in [180, 240]:
        mock = pd.DataFrame({"price": np.repeat(20, test),
                             "quantity": np.repeat(1, test),
                             "exec_time": pd.date_range(start=timestamp, periods=test, freq="T")})
        mock.exec_time = pd.to_datetime(mock.exec_time, utc=True)

        assert exporter.vwap_by_timeperiod(objects=mock, timestamp=timestamp_mock) == 20


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_sql")])
def test_sql_exporter_calc_rolling_vwap(rndm_params):
    exporter = rndm_params["sql_exporter"]

    # Load Contract IDs
    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"],
                                             delivery_area=rndm_params["delivery_area"],
                                             contract_time=rndm_params["contract_time"],
                                             exchange=rndm_params["exchange"])
    # Check if return value is not empty
    assert contract_ids

    # Load Trades from SQL
    sql_trades = exporter.get_public_trades(contract_id=contract_ids,
                                            delivery_area=[rndm_params["delivery_area"]],
                                            as_dataframe=True)

    trade_vwaps = exporter.calc_rolling_vwap(trades=sql_trades)

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
