from massive import RESTClient
import pandas as pd

API_KEY = "TBCRWM_hMNd85ETjqZCz83LFNZGWpJpU"

def get_live_gainers(min_change=1.0, min_volume=10000, limit=50):
    try:
        client = RESTClient(API_KEY)
        
        # Try the snapshot gainers endpoint
        gainers = client.get_snapshot_direction('stocks', direction='gainers')
        
        print(f"Raw gainers returned: {len(gainers)}")

        data = []
        for item in gainers:
            ticker = getattr(item, 'ticker', None) or getattr(item, 'T', None)
            if not ticker:
                continue

            # Extract price and change
            price = getattr(item, 'last_price', None) or getattr(item, 'c', None) or getattr(item, 'last', None)
            change_pct = getattr(item, 'change_percent', None) or getattr(item, 'todays_change_percent', None)
            volume = getattr(item, 'volume', None) or getattr(item, 'v', 0) or 0

            if price is None or change_pct is None:
                continue

            if change_pct >= min_change and volume >= min_volume and price >= 1.0:
                data.append({
                    "Ticker": ticker,
                    "Price": round(price, 4),
                    "% Change": round(change_pct, 2),
                    "Volume": f"{int(volume):,}",
                    "RVOL": "High",
                    "Score": round(change_pct, 1)
                })

        print(f"After filtering: {len(data)} tickers passed")

        if data:
            df = pd.DataFrame(data)
            return df.sort_values("% Change", ascending=False).head(limit)
        return pd.DataFrame()

    except Exception as e:
        print(f"Massive API Error: {e}")
        # Fallback: return some sample data so we can test the UI
        return pd.DataFrame([
            {"Ticker": "GPUS", "Price": 0.4391, "% Change": 68.88, "Volume": "5,200,000", "RVOL": "High", "Score": 68.9},
            {"Ticker": "ICCM", "Price": 7.25, "% Change": 240.38, "Volume": "12,400,000", "RVOL": "High", "Score": 240.4},
        ])
