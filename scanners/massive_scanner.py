from massive import RESTClient
import pandas as pd

API_KEY = "TBCRWM_hMNd85ETjqZCz83LFNZGWpJpU"

def get_live_gainers(min_change=2.0, min_volume=50000, limit=40):
    try:
        client = RESTClient(API_KEY)
        gainers = client.get_gainers_and_losers(
            market="stocks",
            direction="gainers",
            include_pre_post_market=True
        )

        print(f"Raw gainers returned: {len(gainers)}")

        data = []
        for item in gainers:
            day = getattr(item, 'day', None)
            if not day or not getattr(day, 'c', None):
                continue

            ticker = item.ticker
            price = day.c
            volume = getattr(day, 'v', 0) or 0

            change_pct = getattr(item, 'todays_change_percent', None)
            if change_pct is None or change_pct == 0:
                abs_change = getattr(item, 'todays_change', None)
                if abs_change is not None and price > 0:
                    prev = price - abs_change
                    if prev > 0:
                        change_pct = (abs_change / prev) * 100

            if change_pct is None or change_pct == 0:
                open_p = getattr(day, 'o', None)
                if open_p and open_p > 0:
                    change_pct = ((price - open_p) / open_p) * 100
                else:
                    change_pct = 0

            if change_pct >= min_change and volume >= min_volume:
                data.append({
                    "Ticker": ticker,
                    "Price": round(price, 2),
                    "% Change": round(change_pct, 2),
                    "Volume": f"{volume:,}",
                    "RVOL": "High",
                    "Score": round(change_pct * 1.5, 1)
                })

        if data:
            df = pd.DataFrame(data)
            return df.sort_values("% Change", ascending=False).head(limit)
        return pd.DataFrame()

    except Exception as e:
        print(f"Massive Error: {e}")
        return pd.DataFrame()
