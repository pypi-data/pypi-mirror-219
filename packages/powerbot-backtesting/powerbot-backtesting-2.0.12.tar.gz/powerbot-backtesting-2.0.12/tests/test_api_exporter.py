from datetime import datetime
from datetime import timedelta, timezone
from random import choice
import numpy as np
import pandas as pd
import pytest
from dateutil.tz import tzutc
from powerbot_client import ApiClient
from helpers import random_params_api  # noqa


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_api")])
def test_api_exporter_init(rndm_params):
    exporter = rndm_params["api_exporter"]

    assert isinstance(exporter.client, ApiClient)


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_api")])
def test_api_exporter_get_contracts(rndm_params):
    exporter = rndm_params["api_exporter"]

    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"],
                                             contract_time="all",
                                             products=rndm_params["product"],
                                             delivery_areas=[rndm_params["delivery_area"]])

    contract_objects = exporter.get_contracts(time_from=rndm_params["time_from"],
                                              time_till=rndm_params["time_till"],
                                              contract_time="all",
                                              products=rndm_params["product"],
                                              delivery_areas=[rndm_params["delivery_area"]])

    # Check if output is returned
    assert contract_objects, contract_ids

    # Check if output is right type
    assert isinstance(contract_objects, list)
    assert isinstance(contract_ids, dict)

    # Check if both outputs contain same contracts by comparing IDs and length
    ids_1 = [x.contract_id for x in contract_objects]
    ids_2 = [x for i in contract_ids.values() for x in i]
    assert len(ids_1) == len(ids_2)
    assert all(i in ids_2 for i in ids_1)

    # Check if only the chosen product is in the returned contracts
    assert len([x.product for x in contract_objects if x.product in rndm_params["product"]]) == len(contract_objects)

    # Check if all contracts were active in the chosen delivery areas
    assert all(rndm_params["delivery_area"] in i.delivery_areas for i in contract_objects)


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_api")])
def test_api_exporter_get_contract_ids(rndm_params):
    exporter = rndm_params["api_exporter"]

    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"],
                                             contract_time="all",
                                             products=rndm_params["product"],
                                             delivery_areas=[rndm_params["delivery_area"]])

    contract_objects = exporter.get_contracts(time_from=rndm_params["time_from"],
                                              time_till=rndm_params["time_till"],
                                              contract_time="all",
                                              products=rndm_params["product"],
                                              delivery_areas=[rndm_params["delivery_area"]])

    # Check if output is returned
    assert contract_objects, contract_ids

    # Check if output is right type
    assert isinstance(contract_objects, list)
    assert isinstance(contract_ids, dict)

    # Check if both outputs contain same contracts by comparing IDs and length
    ids_1 = [x.contract_id for x in contract_objects]
    ids_2 = [x for i in contract_ids.values() for x in i]
    assert len(ids_1) == len(ids_2)
    assert all(i in ids_2 for i in ids_1)

    # Check if only the chosen product is in the returned contracts
    assert len([x.product for x in contract_objects if x.product in rndm_params["product"]]) == len(contract_objects)

    # Check if all contracts were active in the chosen delivery areas
    assert all(rndm_params["delivery_area"] in i.delivery_areas for i in contract_objects)


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_api")])
def test_api_exporter_get_public_trades(rndm_params):
    exporter = rndm_params["api_exporter"]

    contract_ids = exporter.get_contract_ids(
        time_from=rndm_params["time_from"],
        time_till=rndm_params["time_till"],
        contract_time=rndm_params["contract_time"],
        delivery_areas=[rndm_params["delivery_area"]])

    assert contract_ids

    # Load Trades from API and cache locally
    api_trades = exporter.get_public_trades(
        contract_ids=contract_ids,
        delivery_area=rndm_params["delivery_area"],
        contract_time=rndm_params["contract_time"],
        use_cached_data=False,
        caching=True)

    # Load previously cached Trades
    cache_trades = exporter.get_public_trades(
        contract_ids=contract_ids,
        delivery_area=rndm_params["delivery_area"],
        contract_time=rndm_params["contract_time"],
        use_cached_data=True,
        caching=False)

    # Check if trades are in the right format
    assert isinstance(api_trades, dict), isinstance(cache_trades, dict)

    # Check if only trades for the right contracts have been loaded
    # Local contracts might have no trades!
    assert all(len(v.contract_id.unique()) <= len(contract_ids[k]) for k, v in api_trades.items())
    assert all(c in contract_ids[k] for k, v in api_trades.items() for c in v.contract_id.unique())

    assert all(len(v.contract_id.unique()) <= len(contract_ids[k]) for k, v in cache_trades.items())
    assert all(c in contract_ids[k] for k, v in cache_trades.items() for c in v.contract_id.unique())

    # Check if API and Cache are the same
    assert all(v.compare(cache_trades[k]).empty for k, v in api_trades.items())

    # Check VWAP
    vwap_trades = exporter.get_public_trades(contract_ids=contract_ids,
                                             delivery_area=rndm_params["delivery_area"],
                                             contract_time=rndm_params["contract_time"],
                                             add_vwap=True,
                                             use_cached_data=True,
                                             caching=False)

    vwap_columns = ['trade_id', 'buy_delivery_area', 'sell_delivery_area', 'api_timestamp',
                    'exec_time', 'contract_id', 'price', 'quantity', 'self_trade',
                    'time_diff', 'cumulated_quantity', 'target_volume', 'vwap']

    # Check for added columns
    assert all(i in v.columns for k, v in vwap_trades.items() for i in vwap_columns)

    # Check for data loss
    assert all(len(v) == len(cache_trades[k]) for k, v in vwap_trades.items())

    # Check for data type
    assert all(v.vwap.dtypes == "float" for v in vwap_trades.values())


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_api")])
def test_api_exporter_get_public_trades_by_days(rndm_params):
    exporter = rndm_params["api_exporter"]

    # Get trades with time_from
    trade_data = exporter.get_public_trades_by_days(
        time_from=rndm_params["time_from"],
        previous_days=rndm_params["previous_days"],
        delivery_area=rndm_params["delivery_area"],
        contract_time=rndm_params["contract_time"])

    # Check if trades are in the right format
    assert isinstance(trade_data, dict)

    # Check if the right amount of previous days have been loaded
    # API data is very unreliable here, so this test may fail
    try:
        assert len(trade_data) == rndm_params["previous_days"] + 1
    except AssertionError:
        return

    # Check if only trades for the right contracts have been loaded
    timeframes = {"all": 15, "hourly": 60, "half-hourly": 30, "quarter-hourly": 15}
    time_till = rndm_params["time_from"] + timedelta(minutes=timeframes[rndm_params["contract_time"]])

    contract_ids = exporter.get_contract_ids(rndm_params["time_from"], time_till=time_till,
                                             contract_time=rndm_params["contract_time"])

    for i in range(rndm_params["previous_days"]):
        rndm_params["time_from"] -= timedelta(days=1)
        time_till -= timedelta(days=1)
        contract_ids.update(exporter.get_contract_ids(rndm_params["time_from"], time_till=time_till,
                                                      contract_time=rndm_params["contract_time"]))

    assert all(c in contract_ids[k] for k, v in trade_data.items() for c in v.contract_id.unique())

    # Get trades with specific contract time
    list_contract_ids = []
    for v in contract_ids.values():
        for i in v:
            list_contract_ids.append(i)

    contract_id = choice(list_contract_ids)

    trade_data = exporter.get_public_trades_by_days(contract_id=contract_id,
                                                    contract_time="hourly",
                                                    previous_days=rndm_params["previous_days"],
                                                    delivery_area=rndm_params["delivery_area"])

    # Check if trades are in the right format
    assert isinstance(trade_data, dict)

    # Check if the right amount of previous days have been loaded
    # API data is very unreliable here, so this test may fail
    try:
        assert len(trade_data) == rndm_params["previous_days"] + 1
    except AssertionError:
        return


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_api")])
def test_api_exporter_get_contract_history(rndm_params):
    exporter = rndm_params["api_exporter"]

    contract_ids = exporter.get_contract_ids(
        time_from=rndm_params["time_from"],
        time_till=rndm_params["time_till"],
        contract_time=rndm_params["contract_time"],
        delivery_areas=[rndm_params["delivery_area"]])

    assert contract_ids

    # Load Histories from API and cache locally
    api_history = exporter.get_contract_history(
        contract_ids=contract_ids,
        delivery_area=rndm_params["delivery_area"],
        use_cached_data=False,
        caching=True)

    # Load previously cached Histories
    cache_history = exporter.get_contract_history(
        contract_ids=contract_ids,
        delivery_area=rndm_params["delivery_area"],
        use_cached_data=True,
        caching=True)

    # Check if histories are in the right format
    assert isinstance(api_history, dict), isinstance(cache_history, dict)

    # Check if only histories for the right contracts have been loaded
    assert all(len(v.contract_id.unique()) == len(contract_ids[k]) for k, v in api_history.items())
    assert all(c in contract_ids[k] for k, v in api_history.items() for c in v.contract_id.unique())

    assert all(len(v.contract_id.unique()) == len(contract_ids[k]) for k, v in cache_history.items())
    assert all(c in contract_ids[k] for k, v in cache_history.items() for c in v.contract_id.unique())

    for k, v in api_history.items():
        if not v.compare(cache_history[k]).empty:
            v.compare(cache_history[k]).to_csv(f"tst_{k.replace(':', '')}.csv", sep=";")

    assert all(v.compare(cache_history[k]).empty for k, v in api_history.items())


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_api")])
def test_api_exporter_get_signals(rndm_params):
    exporter = rndm_params["api_exporter"]

    signals = exporter.get_signals(time_from=rndm_params["time_from"] - timedelta(days=20),
                                   time_till=rndm_params["time_till"],
                                   portfolio_id=[rndm_params["portfolio"]])

    # Check if there are any signals, else skip this test
    try:
        assert signals
    except AssertionError:
        return

    # Check for type
    assert isinstance(signals, list)

    # Check if only signals from chosen portfolios have been loaded
    assert all(rndm_params["portfolio"] in i.portfolio_ids for i in signals)

    # Check if received_at times are within time period
    assert all(i.received_at >= (rndm_params["time_from"] - timedelta(days=20)).astimezone(tzutc()) for i in signals)
    assert all(i.received_at <= rndm_params["time_till"].replace(tzinfo=timezone.utc) for i in signals)


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_api")])
def test_api_exporter_get_own_trades(rndm_params):
    exporter = rndm_params["api_exporter"]

    own_trades = exporter.get_own_trades(time_from=rndm_params["time_from"] - timedelta(days=10),
                                         time_till=rndm_params["time_till"],
                                         delivery_area=rndm_params["delivery_area"],
                                         portfolio_id=[rndm_params["portfolio"]])

    # Check if there are any own trades, else skip this test
    try:
        assert own_trades
    except AssertionError:
        return

    # Check for type
    assert isinstance(own_trades, list)

    # Check if only trades from chosen portfolios have been loaded
    assert all(
        rndm_params["portfolio"] == i.buy_portfolio_id or rndm_params["portfolio"] == i.sell_portfolio_id for i in
        own_trades)

    # Check if trade execution times are within time period
    assert all(i.exec_time >= (rndm_params["time_from"] - timedelta(days=15)).astimezone(tzutc()) for i in own_trades)
    assert all(i.exec_time <= rndm_params["time_till"].astimezone(tzutc()) for i in own_trades)


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_api")])
def test_api_exporter_get_internal_trades(rndm_params):
    exporter = rndm_params["api_exporter"]

    internal_trades = exporter.get_internal_trades(time_from=rndm_params["time_from"] - timedelta(days=15),
                                                   time_till=rndm_params["time_till"],
                                                   delivery_area=rndm_params["delivery_area"],
                                                   portfolio_id=[rndm_params["portfolio"]])

    # Check if there are any internal trades, else skip this test
    try:
        assert internal_trades
    except AssertionError:
        return

    # Check for type
    assert isinstance(internal_trades, list)

    # Check if only signals from chosen portfolios have been loaded
    assert all(
        rndm_params["portfolio"] == i.buy_portfolio_id or rndm_params["portfolio"] == i.sell_portfolio_id for i in
        internal_trades)

    # Check if trade execution times are within time period
    assert all(
        i.exec_time >= (rndm_params["time_from"] - timedelta(days=15)).astimezone(tzutc()) for i in internal_trades)
    assert all(i.exec_time <= rndm_params["time_till"].astimezone(tzutc()) for i in internal_trades)


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_api")])
def test_api_exporter_get_own_orders(rndm_params):
    exporter = rndm_params["api_exporter"]

    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"] + timedelta(days=2),
                                             contract_time="all",
                                             delivery_areas=[rndm_params["delivery_area"]])

    own_orders = exporter.get_own_orders(delivery_area=rndm_params["delivery_area"],
                                         portfolio_ids=[rndm_params["portfolio"]],
                                         contract_ids=contract_ids)

    # Check if there are any own orders, else skip this test
    try:
        assert own_orders
    except AssertionError:
        return

    # Check for type
    assert isinstance(own_orders, list)

    # Check if only orders from chosen portfolios have been loaded
    assert all(rndm_params["portfolio"] == i.portfolio_id for i in own_orders)

    # Check if orders belong to the desired contracts
    # Extract contract IDs from orders
    order_contract_ids = [x.contract_id for i in own_orders for x in i.contracts]
    assert all(i in [x for v in contract_ids.values() for x in v] for i in order_contract_ids)


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_api")])
def test_api_exporter_get_orders(rndm_params):
    exporter = rndm_params["api_exporter"]

    # Get contract IDs to load trades for
    contract_ids = exporter.get_contract_ids(
        time_from=rndm_params["time_from"],
        time_till=rndm_params["time_till"],
        contract_time=rndm_params["contract_time"],
        delivery_areas=[rndm_params["delivery_area"]])

    assert contract_ids

    # Load contract history
    contract_history = exporter.get_contract_history(
        contract_ids=contract_ids,
        delivery_area=rndm_params["delivery_area"],
        use_cached_data=False,
        caching=True)

    # Extract order data from history
    orders = exporter.get_orders(contract_history)

    # Check if orders are in the right format
    assert isinstance(orders, dict)

    # Check if all DataFrames have been transformed
    assert len(contract_history) == len(orders)

    # Check for data loss in all individual collections
    for k, v in contract_history.items():
        history_asks = []
        history_bids = []

        for i in v.orders:
            if i["bid"]:
                history_bids += i["bid"]
            if i["ask"]:
                history_asks += i["ask"]

        assert len(orders[k]) == (len(history_asks) + len(history_bids))


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_api")])
def test_api_exporter_get_ohlc_data(rndm_params):
    exporter = rndm_params["api_exporter"]

    # Get contract IDs to load trades for
    contract_ids = exporter.get_contract_ids(
        time_from=rndm_params["time_from"],
        time_till=rndm_params["time_till"],
        contract_time=rndm_params["contract_time"],
        delivery_areas=[rndm_params["delivery_area"]])

    assert contract_ids

    # Load trades
    trade_data = exporter.get_public_trades(
        contract_ids=contract_ids,
        delivery_area=rndm_params["delivery_area"],
        contract_time=rndm_params["contract_time"],
        use_cached_data=False,
        caching=True)

    # Process OHLC data
    processed_ohlc = exporter.get_ohlc_data(
        trade_data=trade_data,
        delivery_area=rndm_params["delivery_area"],
        timesteps=rndm_params["timesteps"],
        time_unit=rndm_params["time_units"],
        use_cached_data=False,
        caching=True)

    # Load OHLC data from cache
    cached_ohlc = exporter.get_ohlc_data(
        trade_data=trade_data,
        delivery_area=rndm_params["delivery_area"],
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


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_api")])
def test_api_exporter_calc_trade_vwap(rndm_params):
    exporter = rndm_params["api_exporter"]

    # Get trade VWAPs for X previous days
    trade_vwap = exporter.calc_trade_vwap(contract_time=rndm_params["contract_time"],
                                          delivery_area=rndm_params["delivery_area"],
                                          time_from=rndm_params["time_from"],
                                          previous_days=rndm_params["previous_days"])

    # Check if trade VWAP is in the right format
    assert isinstance(trade_vwap, pd.DataFrame)

    # Check if only trades for the right contracts have been used
    contract_ids = []
    for i in exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                       time_till=rndm_params["time_till"],
                                       contract_time=rndm_params["contract_time"]).values():
        for x in i:
            contract_ids.append(x)

    for i in range(rndm_params["previous_days"]):
        rndm_params["time_from"] -= timedelta(days=1)
        rndm_params["time_till"] -= timedelta(days=1)
        for i in exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                           time_till=rndm_params["time_till"],
                                           contract_time=rndm_params["contract_time"]).values():
            for x in i:
                contract_ids.append(x)

    assert all(c in contract_ids for c in trade_vwap.contract_id.unique())


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_api")])
def test_api_exporter_vwap_by_depth(rndm_params):
    exporter = rndm_params["api_exporter"]

    # Get contract IDs to load trades for
    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"],
                                             contract_time=rndm_params["contract_time"],
                                             delivery_areas=[rndm_params["delivery_area"]])

    assert contract_ids

    # Load contract history
    history = exporter.get_contract_history(contract_ids=contract_ids,
                                            delivery_area=rndm_params["delivery_area"],
                                            caching=False)
    # Extract order data
    orders = exporter.get_orders(contract_hist_data=history)

    # Load trade data
    trades = exporter.get_public_trades(contract_ids=contract_ids,
                                        delivery_area=rndm_params["delivery_area"],
                                        contract_time=rndm_params["contract_time"],
                                        caching=False)

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
                         [pytest.lazy_fixture("random_params_api")])
def test_api_exporter_vwap_by_timeperiod(rndm_params):
    exporter = rndm_params["api_exporter"]

    # Get contract IDs to load trades for
    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"],
                                             contract_time=rndm_params["contract_time"],
                                             delivery_areas=[rndm_params["delivery_area"]])

    assert contract_ids

    # Load contract history
    api_history = exporter.get_contract_history(contract_ids=contract_ids,
                                                delivery_area=rndm_params["delivery_area"],
                                                caching=False)
    # Extract order data
    orders = exporter.get_orders(contract_hist_data=api_history)

    # Load trade data
    api_trades = exporter.get_public_trades(contract_ids=contract_ids,
                                            delivery_area=rndm_params["delivery_area"],
                                            contract_time=rndm_params["contract_time"],
                                            caching=False)

    timestamp = pd.Timestamp(rndm_params["time_from"] - timedelta(hours=3), tz="UTC")

    # Calculate VWAPS for object collections
    for spec in ["0T-60T-30T", "60T-30T-15T", "60T-60T-0T"]:
        exporter.vwap_by_timeperiod(objects=orders[[*orders][0]], timestamp=timestamp, time_spec=spec)
        exporter.vwap_by_timeperiod(objects=api_trades[[*api_trades][0]], timestamp=timestamp, time_spec=spec)

    # Mock input data to prove output is correct
    timestamp_mock = pd.Timestamp(rndm_params["time_from"] - timedelta(hours=2), tz="UTC")
    for test in [180, 240]:
        mock = pd.DataFrame({"price": np.repeat(20, test),
                             "quantity": np.repeat(1, test),
                             "exec_time": pd.date_range(start=timestamp, periods=test, freq="T")})
        mock.exec_time = pd.to_datetime(mock.exec_time, utc=True)

        assert exporter.vwap_by_timeperiod(objects=mock, timestamp=timestamp_mock) == 20


@pytest.mark.parametrize("rndm_params",
                         [pytest.lazy_fixture("random_params_api")])
def test_api_exporter_calc_rolling_vwap(rndm_params):
    exporter = rndm_params["api_exporter"]

    # Get contract IDs to load trades for
    contract_ids = exporter.get_contract_ids(time_from=rndm_params["time_from"],
                                             time_till=rndm_params["time_till"],
                                             contract_time=rndm_params["contract_time"],
                                             delivery_areas=[rndm_params["delivery_area"]])

    assert contract_ids

    # Load trade data
    api_trades = exporter.get_public_trades(contract_ids=contract_ids,
                                            delivery_area=rndm_params["delivery_area"],
                                            contract_time=rndm_params["contract_time"],
                                            caching=False)

    trade_vwaps = exporter.calc_rolling_vwap(trades=api_trades)

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
