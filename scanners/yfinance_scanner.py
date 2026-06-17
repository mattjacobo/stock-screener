import yfinance as yf
import pandas as pd

def get_live_gainers(min_change=1.0, min_volume=10000, limit=50):
    """
    Strong yFinance scanner with expanded universe.
    """
    watchlist = [
        'GME','AMC','SPCE','PLUG','SOFI','BBBY','BB','NOK','EXPR','WISH','CLOV','SNDL','TLRY',
        'CRBP','SAVA','ATER','MULN','FFIE','KOSS','NAKD','IDEX','XELA','HOLO','SIRI','SMCI',
        'MSTR','COIN','RIOT','MARA','HUT','CLSK','WULF','NVDA','TSLA','AMD','AAPL','META',
        'GOOGL','AMZN','MSFT','NFLX','PYPL','SQ','ROKU','UPST','CVNA','RBLX','U','HOOD',
        'RIVN','LCID','NKLA','WKHS','BLNK','FCEL','BE','RUN','ENPH','SEDG'
    ]

    data = []
    for ticker in watchlist:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")
            if len(hist) < 2:
                continue

            prev_close = hist['Close'].iloc[-2]
            current = hist['Close'].iloc[-1]
            volume = int(hist['Volume'].iloc[-1])

            change_pct = ((current - prev_close) / prev_close) * 100 if prev_close > 0 else 0

            if change_pct >= min_change and volume >= min_volume:
                data.append({
                    "Ticker": ticker,
                    "Price": round(current, 4),
                    "% Change": round(change_pct, 2),
                    "Volume": f"{volume:,}",
                    "RVOL": "N/A",
                    "Score": round(change_pct, 1)
                })
        except:
            continue

    if data:
        df = pd.DataFrame(data)
        return df.sort_values("% Change", ascending=False).head(limit)
    return pd.DataFrame()
