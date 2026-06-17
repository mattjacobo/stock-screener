from massive import RESTClient
import pandas as pd

API_KEY = "TBCRWM_hMNd85ETjqZCz83LFNZGWpJpU"

def get_live_gainers(min_change=0.5, min_volume=10000, limit=50):
    """
    Pure live data from Massive. No fallback.
    Debug prints will help us identify the bottleneck.
    """
    try:
        client = RESTClient(API_KEY)
        
        print("[DEBUG] Attempting to fetch gainers...")

        # Try snapshot first (broader market coverage)
        try:
            gainers = client.get_snapshot_direction('stocks', direction='gainers')
            print(f"[DEBUG] Snapshot method succeeded - Raw items: {len(gainers)}")
        except Exception as e1:
            print(f"[DEBUG] Snapshot method failed: {e1}")
            # Fallback to gainers endpoint
            gainers = client.get_gainers_and_losers(market="stocks", direction="gainers", include_pre_post_market=True)
            print(f"[DEBUG] Gainers endpoint returned: {len(gainers)} items")

        data = []
        processed = 0

        for item in gainers[:200]:  # Limit processing for speed
            processed += 1
            ticker = getattr(item, 'ticker', None) or getattr(item, 'T', None) or getattr(item, 'symbol', None)
            if not ticker:
                continue

            price = getattr(item, 'last_price', None) or getattr(item, 'c', None) or getattr(item, 'last', None) or getattr(item, 'price', None)
            change_pct = getattr(item, 'change_percent', None) or getattr(item, 'todays_change_percent', None) or getattr(item, 'change', None)
            volume = getattr(item, 'volume', None) or getattr(item, 'v', None) or 0

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

        print(f"[DEBUG] Processed {processed} items | After filtering: {len(data)} tickers passed")

        if data:
            df = pd.DataFrame(data)
            return df.sort_values("% Change", ascending=False).head(limit)
        else:
            print("[DEBUG] No tickers passed the filters")
            return pd.DataFrame()

    except Exception as e:
        print(f"[ERROR] Critical Massive API Error: {e}")
        return pd.DataFrame()
