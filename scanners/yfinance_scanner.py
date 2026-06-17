import yfinance as yf
import pandas as pd

def get_live_gainers(min_change=1.0, min_volume=10000, limit=30):
    """
    yFinance based scanner - free and reliable for now.
    """
    try:
        # Common volatile/low-float watchlist
        watchlist = ['GME', 'AMC', 'SPCE', 'PLUG', 'SOFI', 'BBBY', 'BB', 'NOK', 'EXPR', 'WISH', 
                    'CLOV', 'SNDL', 'TLRY', 'CRBP', 'SAVA', 'ATER', 'MULN', 'FFIE', 'KOSS', 'NAKD',
                    'SMCI', 'MSTR', 'COIN', 'RIOT', 'MARA', 'HUT', 'CLSK', 'WULF', 'NVDA', 'TSLA']

        data = []
        for ticker in watchlist:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="5d")
                info = stock.info

                if len(hist) < 2:
                    continue

                prev_close = hist['Close'].iloc[-2]
                current = hist['Close'].iloc[-1]
                volume = hist['Volume'].iloc[-1]
                avg_vol = hist['Volume'].mean()

                change_pct = ((current - prev_close) / prev_close) * 100
                rvol = volume / avg_vol if avg_vol > 0 else 1.0

                if change_pct >= min_change and volume >= min_volume:
                    data.append({
                        "Ticker": ticker,
                        "Price": round(current, 4),
                        "% Change": round(change_pct, 2),
                        "Volume": f"{int(volume):,}",
                        "RVOL": round(rvol, 2),
                        "Score": round(change_pct * 1.5, 1)
                    })
            except:
                continue

        if data:
            df = pd.DataFrame(data)
            return df.sort_values("% Change", ascending=False).head(limit)
        return pd.DataFrame()

    except Exception as e:
        print(f"yFinance Error: {e}")
        return pd.DataFrame()
