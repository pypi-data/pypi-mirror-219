import pandas as pd

from powerbot_backtesting import HistoryExporter
from tests.helpers.transform_test_orderbook import transform_test_orderbook
from tests.helpers.generate_hardcoded_input_orderbook import generate_hardcoded_input_orderbook
from itertools import chain


def test_get_orderbooks_seq_shortest():
    """
    This test validates the output of the get_orderbooks function based on a hard-coded contract history.
    Format-wise, the hard-coded contract history resembles a contract history, that would commonly occur.
    Specifically, this test assumes the shortest_interval parameter of the get_orderbooks function to be set to True as
    well as the concurrent parameter set to False and validates the function output against a hard-coded,
    correct orderbook.
    """

    order_data_df = generate_hardcoded_input_orderbook()

    key = (pd.to_datetime("2021-01-01 12:15:00.000000+00:00"), pd.to_datetime("2021-01-01 12:30:00.000000+00:00"))

    order_data = {key: order_data_df}

    exchange = "epex"
    delivery_area = "10YAT-APG------L"

    exporter = HistoryExporter(exchange=exchange, delivery_area=delivery_area)

    orders_df_shortest_interval = exporter.get_orderbooks(contract_hist_data=order_data,
                                                          concurrent=False,
                                                          shortest_interval=True,
                                                          use_cached_data=False,
                                                          caching=False)

    orders_df_corr_shortest_interval = pd.DataFrame(
        {"order_id": ["1123", "1124", "1234", "1235", "1123", "1234", "1235", "1123", "1235", "1235", "1127", "1235",
                      "1236", "1237", "1235", "1236", "1237", "1235", "1236", "1237", "1238", "1239"],
         "price": [89.0, 90.0, 91.0, 90.0, 89.0, 91.0, 90.0, 89.0, 90.0, 90.0, 80.0, 90.0, -70, 100.0, 90.0, -70.0, 100.0, 90, -70.0, 100.0, -60.0,
                   -80.0],
         "quantity": [0.5, 0.7, 0.5, 0.7, 2, 0.5, 0.7, 2, 2, 2, 1, 2, 5, 1, 2, 0.5, 1, 2, 0.5, 1, 0.7, 0.7],
         "contract_id": ["12049007", "12049007", "12049007", "12049007", "12049007", "12049007", "12049007", "12049007",
                         "12049007", "12049007", "12049022", "12049007", "12049022", "12049022", "12049007", "12049022",
                         "12049022", "12049007", "12049022", "12049022", "12049022", "12049022"],
         "order_entry_time": [pd.to_datetime("2020-12-31 14:00:00.479000+00:00"),
                              pd.to_datetime("2020-12-31 14:00:00.479000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                              pd.to_datetime("2020-12-31 14:00:00.479000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                              pd.to_datetime("2020-12-31 14:00:00.479000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:21.015000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:21.059000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:21.059000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:21.059000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:21.059000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:21.059000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:21.059000+00:00"),
                              pd.to_datetime("2021-01-01 09:31:52.180000+00:00"),
                              pd.to_datetime("2021-01-01 09:31:52.180000+00:00")],
         "type": ["bid", "bid", "ask", "ask", "bid", "ask", "ask", "bid", "ask", "ask", "bid", "ask", "ask", "ask",
                  "ask", "ask", "ask", "ask", "ask", "ask", "ask", "ask"],
         "time_step": [pd.to_datetime("2020-12-31 14:00:00.479000+00:00"),
                       pd.to_datetime("2020-12-31 14:00:00.479000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:21.008000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:21.008000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:21.008000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:21.010000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:21.010000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:21.015000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:21.015000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:21.059000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:21.059000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:21.059000+00:00"),
                       pd.to_datetime("2021-01-01 09:31:32.840000+00:00"),
                       pd.to_datetime("2021-01-01 09:31:32.840000+00:00"),
                       pd.to_datetime("2021-01-01 09:31:32.840000+00:00"),
                       pd.to_datetime("2021-01-01 09:31:52.180000+00:00"),
                       pd.to_datetime("2021-01-01 09:31:52.180000+00:00"),
                       pd.to_datetime("2021-01-01 09:31:52.180000+00:00"),
                       pd.to_datetime("2021-01-01 09:31:52.180000+00:00"),
                       pd.to_datetime("2021-01-01 09:31:52.180000+00:00")]
         })

    orders_df_corr_shortest_interval["delivery_start"] = pd.to_datetime("2021-01-01 12:15:00.000000+00:00")
    orders_df_corr_shortest_interval["delivery_end"] = pd.to_datetime("2021-01-01 12:30:00.000000+00:00")

    orders_df_corr_shortest_interval_transformed = transform_test_orderbook(orders_df_corr_shortest_interval)

    pd.testing.assert_frame_equal(orders_df_shortest_interval, orders_df_corr_shortest_interval_transformed)


def test_get_orderbooks_seq_15m():
    """
       This test validates the output of the get_orderbooks function based on a hard-coded contract history.
       Format-wise, the hard-coded contract history resembles a contract history, that would commonly occur.
       Specifically, this test assumes the shortest_interval parameter of the get_orderbooks function to be set to False,
       assumes time steps of a 15-minute frequency as well as the concurrent parameter set to False and validates the
       function output against a hard-coded, correct orderbook.
       """

    order_data_df = generate_hardcoded_input_orderbook()

    key = (pd.to_datetime("2021-01-01 12:15:00.000000+00:00"), pd.to_datetime("2021-01-01 12:30:00.000000+00:00"))

    order_data = {key: order_data_df}

    exchange = "epex"
    delivery_area = "10YAT-APG------L"

    exporter = HistoryExporter(exchange=exchange, delivery_area=delivery_area)

    orders_df_15m = exporter.get_orderbooks(contract_hist_data=order_data,
                                            concurrent=False,
                                            shortest_interval=False,
                                            use_cached_data=False,
                                            caching=False)

    time_range = pd.date_range(start="2020-12-31 14:15:00+00:00", end="2021-01-01 09:15:00+00:00", freq="15T")

    orders_df_corr_15m = pd.DataFrame(
        {"order_id": list(chain(*[["1123", "1124"] * 77, ["1235"], ["1236"], ["1237"], ["1235"], ["1236"], ["1237"],
                                  ["1238"], ["1239"]])),
         "price": list(chain(*[[89.0, 90.0] * 77, [90.0], [-70.0], [100.0], [90.0], [-70.0], [100.0], [-60.0], [-80.0]])),
         "quantity": list(chain(*[[0.5, 0.7] * 77, [2], [5], [1], [2], [0.5], [1], [0.7], [0.7]])),
         "contract_id": list(
             chain(*[["12049007", "12049007"] * 77, ["12049007"], ["12049022"], ["12049022"], ["12049007"],
                     ["12049022"], ["12049022"], ["12049022"], ["12049022"]])),
         "order_entry_time": list(chain(*[[pd.to_datetime("2020-12-31 14:00:00.479000+00:00"),
                                           pd.to_datetime("2020-12-31 14:00:00.479000+00:00")] * 77,
                                          [pd.to_datetime("2021-01-01 09:29:20.682000+00:00")],
                                          [pd.to_datetime("2021-01-01 09:29:21.059000+00:00")],
                                          [pd.to_datetime("2021-01-01 09:29:21.059000+00:00")],
                                          [pd.to_datetime("2021-01-01 09:29:20.682000+00:00")],
                                          [pd.to_datetime("2021-01-01 09:29:21.059000+00:00")],
                                          [pd.to_datetime("2021-01-01 09:29:21.059000+00:00")],
                                          [pd.to_datetime("2021-01-01 09:31:52.180000+00:00")],
                                          [pd.to_datetime("2021-01-01 09:31:52.180000+00:00")]])),
         "type": list(chain(*[["bid", "bid"] * 77, ["ask"], ["ask"], ["ask"], ["ask"], ["ask"], ["ask"], ["ask"], ["ask"]])),
         "time_step": list(chain(*[time_range.repeat(2), [pd.to_datetime("2021-01-01 09:30:00+00:00")] * 3,
                                   [pd.to_datetime("2021-01-01 09:45:00+00:00")] * 5]))
         })

    orders_df_corr_15m["delivery_start"] = pd.to_datetime("2021-01-01 12:15:00.000000+00:00")
    orders_df_corr_15m["delivery_end"] = pd.to_datetime("2021-01-01 12:30:00.000000+00:00")

    orders_df_corr_15m_transformed = transform_test_orderbook(orders_df_corr_15m)

    pd.testing.assert_frame_equal(orders_df_15m, orders_df_corr_15m_transformed)


def test_get_orderbooks_par_shortest():
    """
       This test validates the output of the get_orderbooks function based on a hard-coded contract history.
       Format-wise, the hard-coded contract history resembles a contract history, that would commonly occur.
       Specifically, this test assumes the shortest_interval parameter of the get_orderbooks function to be set to True as
       well as the concurrent parameter set to True and validates the function output against a hard-coded,
       correct orderbook.
       """

    order_data_df = generate_hardcoded_input_orderbook()

    key1 = (pd.to_datetime("2021-01-01 12:15:00.000000+00:00"), pd.to_datetime("2021-01-01 12:30:00.000000+00:00"))
    key2 = (pd.to_datetime("2021-01-01 12:30:00.000000+00:00"), pd.to_datetime("2021-01-01 12:45:00.000000+00:00"))

    order_data = {key1: order_data_df, key2: order_data_df}

    exchange = "epex"
    delivery_area = "10YAT-APG------L"

    exporter = HistoryExporter(exchange=exchange, delivery_area=delivery_area)

    orders_df_shortest_interval = exporter.get_orderbooks(contract_hist_data=order_data,
                                                          concurrent=True,
                                                          shortest_interval=True,
                                                          use_cached_data=False,
                                                          caching=False)

    orders_df_corr_shortest_interval = pd.DataFrame(
        {"order_id": ["1123", "1124", "1234", "1235", "1123", "1234", "1235", "1123", "1235", "1235", "1127", "1235",
                      "1236", "1237", "1235", "1236", "1237", "1235", "1236", "1237", "1238", "1239"],
         "price": [89.0, 90.0, 91.0, 90.0, 89.0, 91.0, 90.0, 89.0, 90.0, 90.0, 80.0, 90.0, -70, 100.0, 90.0, -70.0, 100.0, 90, -70.0, 100.0, -60.0,
                   -80.0],
         "quantity": [0.5, 0.7, 0.5, 0.7, 2, 0.5, 0.7, 2, 2, 2, 1, 2, 5, 1, 2, 0.5, 1, 2, 0.5, 1, 0.7, 0.7],
         "contract_id": ["12049007", "12049007", "12049007", "12049007", "12049007", "12049007", "12049007", "12049007",
                         "12049007", "12049007", "12049022", "12049007", "12049022", "12049022", "12049007", "12049022",
                         "12049022", "12049007", "12049022", "12049022", "12049022", "12049022"],
         "order_entry_time": [pd.to_datetime("2020-12-31 14:00:00.479000+00:00"),
                              pd.to_datetime("2020-12-31 14:00:00.479000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                              pd.to_datetime("2020-12-31 14:00:00.479000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                              pd.to_datetime("2020-12-31 14:00:00.479000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:21.015000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:21.059000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:21.059000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:21.059000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:21.059000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:21.059000+00:00"),
                              pd.to_datetime("2021-01-01 09:29:21.059000+00:00"),
                              pd.to_datetime("2021-01-01 09:31:52.180000+00:00"),
                              pd.to_datetime("2021-01-01 09:31:52.180000+00:00")],
         "type": ["bid", "bid", "ask", "ask", "bid", "ask", "ask", "bid", "ask", "ask", "bid", "ask", "ask", "ask",
                  "ask", "ask", "ask", "ask", "ask", "ask", "ask", "ask"],
         "time_step": [pd.to_datetime("2020-12-31 14:00:00.479000+00:00"),
                       pd.to_datetime("2020-12-31 14:00:00.479000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:20.682000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:21.008000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:21.008000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:21.008000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:21.010000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:21.010000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:21.015000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:21.015000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:21.059000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:21.059000+00:00"),
                       pd.to_datetime("2021-01-01 09:29:21.059000+00:00"),
                       pd.to_datetime("2021-01-01 09:31:32.840000+00:00"),
                       pd.to_datetime("2021-01-01 09:31:32.840000+00:00"),
                       pd.to_datetime("2021-01-01 09:31:32.840000+00:00"),
                       pd.to_datetime("2021-01-01 09:31:52.180000+00:00"),
                       pd.to_datetime("2021-01-01 09:31:52.180000+00:00"),
                       pd.to_datetime("2021-01-01 09:31:52.180000+00:00"),
                       pd.to_datetime("2021-01-01 09:31:52.180000+00:00"),
                       pd.to_datetime("2021-01-01 09:31:52.180000+00:00")]
         })

    orders_df_corr_shortest_interval["delivery_start"] = pd.to_datetime("2021-01-01 12:15:00.000000+00:00")
    orders_df_corr_shortest_interval["delivery_end"] = pd.to_datetime("2021-01-01 12:30:00.000000+00:00")

    orders_df_corr_shortest_interval2 = orders_df_corr_shortest_interval.copy()

    orders_df_corr_shortest_interval2["delivery_start"] = pd.to_datetime("2021-01-01 12:30:00.000000+00:00")
    orders_df_corr_shortest_interval2["delivery_end"] = pd.to_datetime("2021-01-01 12:45:00.000000+00:00")

    orders_df_corr_shortest_interval_combined = pd.concat([orders_df_corr_shortest_interval,
                                                           orders_df_corr_shortest_interval2], axis=0)

    orders_df_corr_shortest_interval_transformed = transform_test_orderbook(orders_df_corr_shortest_interval_combined)

    pd.testing.assert_frame_equal(orders_df_shortest_interval, orders_df_corr_shortest_interval_transformed)


def test_get_orderbooks_par_15m():
    """
       This test validates the output of the get_orderbooks function based on a hard-coded contract history.
       Format-wise, the hard-coded contract history resembles a contract history, that would commonly occur.
       Specifically, this test assumes the shortest_interval parameter of the get_orderbooks function to be set to False,
       assumes time steps of a 15-minute frequency as well as the concurrent parameter set to True and validates the
       function output against a hard-coded, correct orderbook.
       """

    order_data_df = generate_hardcoded_input_orderbook()

    key1 = (pd.to_datetime("2021-01-01 12:15:00.000000+00:00"), pd.to_datetime("2021-01-01 12:30:00.000000+00:00"))
    key2 = (pd.to_datetime("2021-01-01 12:30:00.000000+00:00"), pd.to_datetime("2021-01-01 12:45:00.000000+00:00"))

    order_data = {key1: order_data_df, key2: order_data_df}

    exchange = "epex"
    delivery_area = "10YAT-APG------L"

    exporter = HistoryExporter(exchange=exchange, delivery_area=delivery_area)

    orders_df_15m = exporter.get_orderbooks(contract_hist_data=order_data,
                                            concurrent=True,
                                            shortest_interval=False,
                                            use_cached_data=False,
                                            caching=False)

    time_range = pd.date_range(start="2020-12-31 14:15:00+00:00", end="2021-01-01 09:15:00+00:00", freq="15T")

    orders_df_corr_15m = pd.DataFrame(
        {"order_id": list(chain(*[["1123", "1124"] * 77, ["1235"], ["1236"], ["1237"], ["1235"], ["1236"], ["1237"],
                                  ["1238"], ["1239"]])),
         "price": list(
             chain(*[[89.0, 90.0] * 77, [90.0], [-70.0], [100.0], [90.0], [-70.0], [100.0], [-60.0], [-80.0]])),
         "quantity": list(chain(*[[0.5, 0.7] * 77, [2], [5], [1], [2], [0.5], [1], [0.7], [0.7]])),
         "contract_id": list(
             chain(*[["12049007", "12049007"] * 77, ["12049007"], ["12049022"], ["12049022"], ["12049007"],
                     ["12049022"], ["12049022"], ["12049022"], ["12049022"]])),
         "order_entry_time": list(chain(*[[pd.to_datetime("2020-12-31 14:00:00.479000+00:00"),
                                           pd.to_datetime("2020-12-31 14:00:00.479000+00:00")] * 77,
                                          [pd.to_datetime("2021-01-01 09:29:20.682000+00:00")],
                                          [pd.to_datetime("2021-01-01 09:29:21.059000+00:00")],
                                          [pd.to_datetime("2021-01-01 09:29:21.059000+00:00")],
                                          [pd.to_datetime("2021-01-01 09:29:20.682000+00:00")],
                                          [pd.to_datetime("2021-01-01 09:29:21.059000+00:00")],
                                          [pd.to_datetime("2021-01-01 09:29:21.059000+00:00")],
                                          [pd.to_datetime("2021-01-01 09:31:52.180000+00:00")],
                                          [pd.to_datetime("2021-01-01 09:31:52.180000+00:00")]])),
         "type": list(
             chain(*[["bid", "bid"] * 77, ["ask"], ["ask"], ["ask"], ["ask"], ["ask"], ["ask"], ["ask"], ["ask"]])),
         "time_step": list(chain(*[time_range.repeat(2), [pd.to_datetime("2021-01-01 09:30:00+00:00")] * 3,
                                   [pd.to_datetime("2021-01-01 09:45:00+00:00")] * 5]))
         })

    orders_df_corr_15m["delivery_start"] = pd.to_datetime("2021-01-01 12:15:00.000000+00:00")
    orders_df_corr_15m["delivery_end"] = pd.to_datetime("2021-01-01 12:30:00.000000+00:00")

    orders_df_corr_15m2 = orders_df_corr_15m.copy()

    orders_df_corr_15m2["delivery_start"] = pd.to_datetime("2021-01-01 12:30:00.000000+00:00")
    orders_df_corr_15m2["delivery_end"] = pd.to_datetime("2021-01-01 12:45:00.000000+00:00")

    orders_df_corr_15m_combined = pd.concat([orders_df_corr_15m,
                                             orders_df_corr_15m2], axis=0)

    orders_df_corr_15m_transformed = transform_test_orderbook(orders_df_corr_15m_combined)

    pd.testing.assert_frame_equal(orders_df_15m, orders_df_corr_15m_transformed)


def test_bid_over_ask_in_generated_orderbook_15min():
    """
       This test validates the output of the 15min-interval-based get_orderbooks function against bid-over-ask errors.
       The expected outcome, is that there are no bids-over-asks.
    """

    order_data_df = generate_hardcoded_input_orderbook()

    key1 = (pd.to_datetime("2021-01-01 12:15:00.000000+00:00"), pd.to_datetime("2021-01-01 12:30:00.000000+00:00"))
    key2 = (pd.to_datetime("2021-01-01 12:30:00.000000+00:00"), pd.to_datetime("2021-01-01 12:45:00.000000+00:00"))

    order_data = {key1: order_data_df, key2: order_data_df}

    exchange = "epex"
    delivery_area = "10YAT-APG------L"

    exporter = HistoryExporter(exchange=exchange, delivery_area=delivery_area)

    orders_df_15m = exporter.get_orderbooks(contract_hist_data=order_data,
                                            concurrent=True,
                                            shortest_interval=False,
                                            use_cached_data=False,
                                            caching=False)

    assert sum(orders_df_15m["best_bid"] > orders_df_15m["best_ask"]) == 0


def test_bid_over_ask_in_generated_orderbook_shortest_interval():
    """
       This test validates the output of the shortest-interval-based get_orderbooks function against bid-over-ask errors.
       The expected outcome, is that there are no bids-over-asks.
    """

    order_data_df = generate_hardcoded_input_orderbook()

    key1 = (pd.to_datetime("2021-01-01 12:15:00.000000+00:00"), pd.to_datetime("2021-01-01 12:30:00.000000+00:00"))
    key2 = (pd.to_datetime("2021-01-01 12:30:00.000000+00:00"), pd.to_datetime("2021-01-01 12:45:00.000000+00:00"))

    order_data = {key1: order_data_df, key2: order_data_df}

    exchange = "epex"
    delivery_area = "10YAT-APG------L"

    exporter = HistoryExporter(exchange=exchange, delivery_area=delivery_area)

    orders_df_shortest_interval = exporter.get_orderbooks(contract_hist_data=order_data,
                                                          concurrent=True,
                                                          shortest_interval=True,
                                                          use_cached_data=False,
                                                          caching=False)

    assert sum(orders_df_shortest_interval["best_bid"] > orders_df_shortest_interval["best_ask"]) == 0
