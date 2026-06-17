from massive import RESTClient
import pandas as pd

API_KEY = "TBCRWM_hMNd85ETjqZCz83LFNZGWpJpU"

def get_live_gainers(min_change=0.5, min_volume=10000, limit=30):
    """
    Pure live scanner with heavy debug output.
    """
    try:
        client = RESTClient(API_KEY)
        print("[DEBUG] Client created successfully")

        # Try the standard gainers method
        gainers = client.get_gainers_and_losers(
            market="stocks", 
            direction="gainers",
            include_pre_post_market=True
        )
        
        print(f"[DEBUG] get_gainers_and_losers returned {len(gainers)} items")

        data = []
        for item in gainers:
            ticker = getattr(item, 'ticker', None)
            if not ticker:
                continue

            day = getattr(item, 'day', None)
            if day:
                price = getattr(day, 'c', None)
                volume = getattr(day, 'v', 0)
            else:
                price = getattr(item, 'last_price', None) or getattr(item, 'c', None)
                volume = getattr(item, 'volume', 0) or getattr(item, 'v', 0)

            change_pct = getattr(item, 'todays_change_percent', None) or getattr(item, 'change_percent', None)

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

        print(f"[DEBUG] After filtering: {len(data)} tickers passed")

        if data:
            df = pd.DataFrame(data)
            return df.sort_values("% Change", ascending=False).head(limit)
        else:
            print("[DEBUG] No tickers passed filters")
            return pd.DataFrame()

    except Exception as e:
        print(f"[ERROR] Critical error: {str(e)}")
        return pd.DataFrame()
