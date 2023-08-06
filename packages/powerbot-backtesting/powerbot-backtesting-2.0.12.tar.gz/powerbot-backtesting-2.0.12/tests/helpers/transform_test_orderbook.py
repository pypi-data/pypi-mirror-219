import pandas as pd


def transform_test_orderbook(orderbook: pd.DataFrame):
    """
    This function transforms the hard-coded, correct orderbook into the format required to compare it with the output
    orderbook of the get_orderbooks function.
    """

    orderbook.set_index(["delivery_start", "delivery_end", "time_step"], inplace=True,
                        drop=False)

    orderbook.index.names = ["delivery_start", "delivery_end", "timestep"]

    orderbook = orderbook.drop(["delivery_start", "delivery_end"], axis=1)

    orderbook["order_entry_time"] = orderbook.order_entry_time.astype(
        object)

    orderbook = orderbook.rename(columns={"type": "side"})

    orderbook_asks = orderbook[
        orderbook["side"] == "ask"].reset_index()
    orderbook_bids = orderbook[
        orderbook["side"] == "bid"].reset_index()
    min_sell_price = orderbook_asks.groupby(["delivery_start", "delivery_end", "timestep"])[
        "price"].min().reset_index()
    max_buy_price = orderbook_bids.groupby(["delivery_start", "delivery_end", "timestep"])[
        "price"].max().reset_index()
    idx_asks = orderbook_asks.groupby(["delivery_start", "delivery_end", "timestep"])[
        "price"].idxmin()
    idx_bids = orderbook_bids.groupby(["delivery_start", "delivery_end", "timestep"])[
        "price"].idxmax()

    min_sell_quant = orderbook_asks.loc[
        idx_asks, ["delivery_start", "delivery_end", "timestep", "quantity"]]
    min_sell_quant = min_sell_quant.rename(columns={"quantity": "best_ask_qty"})
    sell_agg = min_sell_quant.merge(min_sell_price)
    sell_agg = sell_agg.rename(columns={"price": "best_ask"})

    max_buy_quant = orderbook_bids.loc[
        idx_bids, ["delivery_start", "delivery_end", "timestep", "quantity"]]
    max_buy_quant = max_buy_quant.rename(columns={"quantity": "best_bid_qty"})
    buy_agg = max_buy_quant.merge(max_buy_price)
    buy_agg = buy_agg.rename(columns={"price": "best_bid"})
    data_agg = sell_agg.merge(buy_agg, on=["delivery_start", "delivery_end", "timestep"], how="outer")

    orderbook = orderbook.merge(data_agg, left_index=True,
                                right_on=["delivery_start",
                                          "delivery_end", "timestep"])

    orderbook.set_index(["delivery_start", "delivery_end", "timestep"], inplace=True)

    orderbook.loc[orderbook["side"] == "bid", "side"] = "BUY"
    orderbook.loc[orderbook["side"] == "ask", "side"] = "SELL"

    orderbook["side"] = orderbook["side"].astype("category")

    return orderbook
