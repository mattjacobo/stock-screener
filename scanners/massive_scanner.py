from massive import RESTClient
import pandas as pd

API_KEY = "TBCRWM_hMNd85ETjqZCz83LFNZGWpJpU"

def get_live_gainers(min_change=0.5, min_volume=10000, limit=50):
    """Returns data + debug info for visibility in the app."""
    debug_info = []
    try:
        client = RESTClient(API_KEY)
        debug_info.append("✅ Client initialized successfully")

        # Try snapshot for broader coverage
        snapshot = client.get_snapshot_all('stocks')
        debug_info.append(f"📡 Snapshot returned {len(snapshot)} items")

        data = []
        for item in snapshot[:300]:   # Process more items
            ticker = getattr(item, 'ticker', None) or getattr(item, 'T', None)
            if not ticker:
                continue

            price = getattr(item, 'last_price', None) or getattr(item, 'c', None) or getattr(item, 'last', None)
            change_pct = getattr(item, 'change_percent', None) or getattr(item, 'todays_change_percent', None)
            volume = getattr(item, 'volume', None) or getattr(item, 'v', 0) or 0

            if price is None or change_pct is None:
                continue

            try:
                price = float(price)
                change_pct = float(change_pct)
            except:
                continue

            if change_pct >= min_change and volume >= min_volume and price >= 0.5:
                data.append({
                    "Ticker": ticker,
                    "Price": round(price, 4),
                    "% Change": round(change_pct, 2),
                    "Volume": f"{int(volume):,}",
                    "RVOL": "High",
                    "Score": round(change_pct, 1)
                })

        debug_info.append(f"✅ After filtering: {len(data)} tickers passed filters")
        
        if data:
            df = pd.DataFrame(data)
            return df.sort_values("% Change", ascending=False).head(limit), debug_info
        else:
            debug_info.append("⚠️ No tickers passed filters")
            return pd.DataFrame(), debug_info

    except Exception as e:
        debug_info.append(f"❌ ERROR: {str(e)}")
        return pd.DataFrame(), debug_info
