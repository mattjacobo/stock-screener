from tradingview_screener import Screener
import pandas as pd

def get_live_gainers(min_change=1.0, min_volume=10000, limit=50):
    """
    TradingView-based scanner - scans the entire market.
    """
    try:
        screener = Screener()
        
        # Basic filters for momentum plays
        df = screener \
            .filter("change", ">=", min_change) \
            .filter("volume", ">=", min_volume) \
            .filter("price", ">=", 0.5) \
            .sort("change", "desc") \
            .get(limit)

        if not df.empty:
            df = df.rename(columns={
                "symbol": "Ticker",
                "price": "Price",
                "change": "% Change",
                "volume": "Volume"
            })
            df = df[["Ticker", "Price", "% Change", "Volume"]]
            df["RVOL"] = "N/A"
            df["Score"] = df["% Change"]
            return df.head(limit)
        return pd.DataFrame()

    except Exception as e:
        print(f"TradingView Error: {e}")
        return pd.DataFrame()
