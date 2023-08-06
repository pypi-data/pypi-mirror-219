import pandas as pd
import numpy as np


def generate_hardcoded_input_orderbook():

    dates = pd.Series(pd.to_datetime(["2020-12-28 05:06:25.791000+00:00", "2020-12-31 14:00:00.479000+00:00",
                                      "2021-01-01 09:29:20.682000+00:00", "2021-01-01 09:29:21.008000+00:00",
                                      "2021-01-01 09:29:21.010000+00:00", "2021-01-01 09:29:21.015000+00:00",
                                      "2021-01-01 09:29:21.059000+00:00", "2021-01-01 09:31:32.840000+00:00",
                                      "2021-01-01 09:31:52.180000+00:00", "2021-01-01 09:31:52.180000+00:00"]))

    contract_id = pd.Series(["12049007", "12049007", "12049007", "12049007", "12049007", "120490022", "120490022",
                             "120490022", "120490022", "120490022"])

    delivery_area = pd.Series(["10YAT-APG------L"] * 10)

    delta = pd.Series([True, True, False, True, True, True, True, True, True, True])

    revision_no = pd.Series(np.arange(2, 12))

    asks = pd.Series([np.nan, np.nan,
                      [{"order_id": 1234, "price": 91, "quantity": 0.5, "contract_id": "12049007",
                        "delivery_area": "10YAT-APG------L",
                        "order_entry_time": pd.to_datetime("2021-01-01 09:29:20.682000+00:00")},
                       {"order_id": 1235, "price": 90, "quantity": 0.7, "contract_id": "12049007",
                        "delivery_area": "10YAT-APG------L",
                        "order_entry_time": pd.to_datetime("2021-01-01 09:29:20.682000+00:00")}],
                      np.nan,
                      [{"order_id": 1235, "price": 93, "quantity": 2, "contract_id": "12049007",
                        "delivery_area": "10YAT-APG------L",
                        "order_entry_time": pd.to_datetime("2021-01-01 09:29:20.682000+00:00")},
                       {"order_id": 1234, "price": 93, "quantity": 0.0, "contract_id": "12049007",
                        "delivery_area": "10YAT-APG------L",
                        "order_entry_time": pd.to_datetime("2021-01-01 09:29:20.682000+00:00")}],
                      np.nan,
                      [{"order_id": 1236, "price": -70, "quantity": 5, "contract_id": "12049022",
                        "delivery_area": "10YAT-APG------L",
                        "order_entry_time": pd.to_datetime("2021-01-01 09:29:21.059000+00:00")},
                       {"order_id": 1237, "price": 100, "quantity": 1, "contract_id": "12049022",
                        "delivery_area": "10YAT-APG------L",
                        "order_entry_time": pd.to_datetime("2021-01-01 09:29:21.059000+00:00")}],
                      [{"order_id": 1236, "price": 91, "quantity": 0.5, "contract_id": "12049022",
                        "delivery_area": "10YAT-APG------L",
                        "order_entry_time": pd.to_datetime("2021-01-01 09:29:21.059000+00:00")}],
                      [{"order_id": 1238, "price": -60, "quantity": 0.7, "contract_id": "12049022",
                        "delivery_area": "10YAT-APG------L",
                        "order_entry_time": pd.to_datetime("2021-01-01 09:31:52.180000+00:00")}],
                      [{"order_id": 1239, "price": -80, "quantity": 0.7, "contract_id": "12049022",
                        "delivery_area": "10YAT-APG------L",
                        "order_entry_time": pd.to_datetime("2021-01-01 09:31:52.180000+00:00")}]
                      ]
                     )

    bids = pd.Series([np.nan,
                      [{"order_id": 1123, "price": 89, "quantity": 0.5, "contract_id": "12049007",
                        "delivery_area": "10YAT-APG------L",
                        "order_entry_time": pd.to_datetime("2020-12-31 14:00:00.479000+00:00")},
                       {"order_id": 1124, "price": 90, "quantity": 0.7, "contract_id": "12049007",
                        "delivery_area": "10YAT-APG------L",
                        "order_entry_time": pd.to_datetime("2020-12-31 14:00:00.479000+00:00")}],
                      np.nan,
                      [{"order_id": 1123, "price": 89, "quantity": 2, "contract_id": "12049007",
                        "delivery_area": "10YAT-APG------L",
                        "order_entry_time": pd.to_datetime("2020-12-31 14:00:00.479000+00:00")},
                       {"order_id": 1124, "price": 90, "quantity": 0.0, "contract_id": "12049007",
                        "delivery_area": "10YAT-APG------L",
                        "order_entry_time": pd.to_datetime("2020-12-31 14:00:00.479000+00:00")}],
                      np.nan,
                      [{"order_id": 1123, "price": 89, "quantity": 0.0, "contract_id": "12049007",
                        "delivery_area": "10YAT-APG------L",
                        "order_entry_time": pd.to_datetime("2020-12-31 14:00:00.479000+00:00")},
                       {"order_id": 1127, "price": 80, "quantity": 1, "contract_id": "12049022",
                        "delivery_area": "10YAT-APG------L",
                        "order_entry_time": pd.to_datetime("2021-01-01 09:29:21.015000+00:00")}],
                      [{"order_id": 1127, "price": 80, "quantity": 0.0, "contract_id": "12049022",
                        "delivery_area": "10YAT-APG------L",
                        "order_entry_time": pd.to_datetime("2021-01-01 09:29:21.015000+00:00")}],
                      np.nan,
                      [{"order_id": 1130, "price": 80, "quantity": 0.0, "contract_id": "12049022",
                        "delivery_area": "10YAT-APG------L",
                        "order_entry_time": pd.to_datetime("2021-01-01 09:31:52.180000+00:00")}],
                      np.nan]
                     )

    best_bid = pd.Series([np.nan, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    best_ask = pd.Series([np.nan, np.nan, 0, 0, 0, 0, 0, 0, 0, 0])

    order_data_df = pd.concat([dates, contract_id, delivery_area, delta, revision_no, best_bid, best_ask, asks, bids],
                              keys=["as_of", "contract_id", "delivery_area", "delta", "revision_no", "best_bid",
                                    "best_ask", "asks", "bids"], axis=1)
    return order_data_df
