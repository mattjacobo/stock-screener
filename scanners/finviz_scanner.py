from finvizfinance.screener import Screener
import pandas as pd

def get_live_gainers(min_change=1.0, min_volume=10000, limit=50):
    """
    Finviz-based scanner - scans the entire market with filters.
    """
    try:
        # Define filters similar to your criteria
        filters = {
            'Change': f'+{min_change}%',   # Gap / % Change
            'Volume': f'+{min_volume}',    # Minimum volume
            'Price': 'Over $0.5'           # Avoid pennies if wanted
        }

        screener = Screener()
        screener.set_filter(filters_dict=filters)

        df = screener.screener_view()
        
        if not df.empty:
            df = df.rename(columns={
                'Ticker': 'Ticker',
                'Price': 'Price',
                'Change': '% Change',
                'Volume': 'Volume'
            })
            
            # Clean and format
            df['% Change'] = pd.to_numeric(df['% Change'].astype(str).str.replace('%', ''), errors='coerce')
            df = df[df['% Change'] >= min_change].head(limit)
            
            df = df[['Ticker', 'Price', '% Change', 'Volume']]
            df['RVOL'] = 'N/A'
            df['Score'] = df['% Change']
            
            return df
        
        return pd.DataFrame()

    except Exception as e:
        print(f"Finviz Error: {e}")
        return pd.DataFrame()
