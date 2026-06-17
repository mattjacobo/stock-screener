from massive import RESTClient
import pandas as pd

API_KEY = "TBCRWM_hMNd85ETjqZCz83LFNZGWpJpU"

def get_live_gainers(min_change=0.5, min_volume=10000, limit=50):
    try:
        client = RESTClient(API_KEY)
        
        # Correct method for gainers
        gainers = client.get_snapshot_direction('stocks', direction='gainers')
        
        print(f"Raw gainers returned: {len(gainers)}")

        data = []
        for item in gainers:
            ticker = getattr(item, 'ticker', None) or getattr(item, 'T', None)
            if not ticker:
                continue

            day = getattr(item, 'day', None) or item
            price = getattr(day, 'c', None) or getattr(day, 'last_price', None) or getattr(item, 'last', None)
            volume = getattr(day, 'v', None) or getattr(day, 'volume', 0) or 0

            change_pct = getattr(item, 'todays_change_percent', None) or getattr(item, 'change_percent', None)
            if change_pct is None or change_pct == 0:
                change_pct = getattr(item, 'change', None)
                if change_pct and price:
                    change_pct = change_pct / (price - change_pct) * 100 if (price - change_pct) > 0 else 0

            if change_pct is None:
                change_pct = 0

            if change_pct >= min_change and volume >= min_volume and price and price >= 1.0:
                data.append({
                    "Ticker": ticker,
                    "Price": round(price, 2),
                    "% Change": round(change_pct, 2),
                    "Volume": f"{int(volume):,}",
                    "RVOL": "High",
                    "Score": round(change_pct * 1.5, 1)
                })

        print(f"After filtering: {len(data)} tickers passed")

        if data:
            df = pd.DataFrame(data)
            return df.sort_values("% Change", ascending=False).head(limit)
        return pd.DataFrame()

    except Exception as e:
        print(f"Massive API Error: {e}")
        return pd.DataFrame()
