from massive import RESTClient
import pandas as pd

API_KEY = "TBCRWM_hMNd85ETjqZCz83LFNZGWpJpU"

def get_live_gainers(min_change=1.0, min_volume=10000, limit=50):
    """
    Fetches real gainers from Massive.io and applies basic filters.
    """
    try:
        client = RESTClient(API_KEY)
        
        # Using snapshot for broader market coverage
        gainers = client.get_snapshot_direction('stocks', direction='gainers')
        
        print(f"[DEBUG] Raw gainers returned: {len(gainers)}")

        data = []
        for item in gainers:
            # Extract ticker
            ticker = getattr(item, 'ticker', None) or getattr(item, 'T', None)
            if not ticker:
                continue

            # Extract price and change
            price = getattr(item, 'last_price', None) or getattr(item, 'c', None) or getattr(item, 'last', None)
            change_pct = getattr(item, 'change_percent', None) or getattr(item, 'todays_change_percent', None)
            volume = getattr(item, 'volume', None) or getattr(item, 'v', 0) or 0

            if price is None or change_pct is None:
                continue

            if change_pct >= min_change and volume >= min_volume and price >= 0.5:
                data.append({
                    "Ticker": ticker,
                    "Price": round(float(price), 4),
                    "% Change": round(float(change_pct), 2),
                    "Volume": f"{int(volume):,}",
                    "RVOL": "High",
                    "Score": round(float(change_pct), 1)
                })

        print(f"[DEBUG] After filtering: {len(data)} tickers passed")

        if data:
            df = pd.DataFrame(data)
            return df.sort_values("% Change", ascending=False).head(limit)
        else:
            print("[DEBUG] No tickers passed filters")
            return pd.DataFrame()

    except Exception as e:
        print(f"[ERROR] Massive API Error: {e}")
        return pd.DataFrame()
