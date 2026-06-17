from tradingview_screener import Query
import pandas as pd

def get_live_gainers(min_change=0.5, min_volume=5000, limit=50):
    """
    TradingView Scanner - Full market scan.
    """
    try:
        query = (Query()
                 .select('symbol', 'close', 'change', 'volume', 'market_cap_basic')
                 .where('change', '>=', min_change)
                 .where('volume', '>=', min_volume)
                 .where('close', '>=', 0.5)
                 .sort('change', 'desc')
                 .limit(limit))

        df = query.get_scanner_data()

        if not df.empty:
            df = df.rename(columns={
                "symbol": "Ticker",
                "close": "Price",
                "change": "% Change",
                "volume": "Volume"
            })
            df = df[["Ticker", "Price", "% Change", "Volume"]].copy()
            df["RVOL"] = "N/A"
            df["Score"] = df["% Change"].round(1)
            return df.head(limit)
        
        return pd.DataFrame()

    except Exception as e:
        print(f"TradingView Scanner Error: {e}")
        return pd.DataFrame()
