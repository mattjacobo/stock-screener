import streamlit as st
import pandas as pd
from scanners.massive_scanner import get_live_gainers
import plotly.graph_objects as go

st.set_page_config(page_title="Stock Screener", layout="wide", initial_sidebar_state="expanded")

st.title("🚀 Stock Screener - Momentum Play Detector")
st.caption("Real-time Massive.io | Auto Discovery | Sykes/Touhey Style")

# Sidebar Filters
with st.sidebar:
    st.header("🔍 Strategy Filters")
    
    gap_min = st.slider("Gap Min %", 0.0, 30.0, 2.0)
    min_volume = st.number_input("Min Volume", value=20000, step=10000)
    min_price = st.number_input("Min Price $", value=0.5, step=0.1)

    st.header("Risk Management")
    account_size = st.number_input("Account Size ($)", value=1000)
    risk_percent = st.slider("Risk % per Trade", 1.0, 10.0, 5.0)

# Main Area
col_table, col_details = st.columns([3.5, 2.2])

with col_table:
    st.subheader("📊 Live Momentum Scanner")
    st.caption("Automatically finds plays matching your filters")

    if st.button("🔄 Run Live Scan", type="primary", use_container_width=True):
        with st.spinner("Scanning market with Massive.io..."):
            df = get_live_gainers(min_change=gap_min, min_volume=min_volume)

            if not df.empty:
                # Fixed styling
                def highlight_change(row):
                    styles = [''] * len(row)
                    try:
                        idx = row.index.get_loc('% Change')
                        if row['% Change'] > 0:
                            styles[idx] = 'background-color: #0e4a2e; color: white'
                    except:
                        pass
                    return styles
                
                styled_df = df.style.apply(highlight_change, axis=1)
                
                st.dataframe(
                    styled_df,
                    use_container_width=True,
                    hide_index=True,
                    height=650
                )
                st.success(f"✅ Found {len(df)} plays")
            else:
                st.warning("No plays found. Try lowering Gap Min % or Min Volume.")

with col_details:
    st.subheader("Selected Ticker Analysis")
    ticker = st.text_input("Ticker (or click row above)", value="").upper().strip()
    
    if st.button("Load Chart + Zones", use_container_width=True) and ticker:
        st.info(f"📈 Loading analysis for **{ticker}**...")
        fig = go.Figure()
        fig.update_layout(title=f"{ticker} - Daily Chart with Supply/Demand Zones", height=480, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

# Bottom
st.divider()
st.subheader("🛎️ Alerts & Log")
st.info("Run scans to generate opportunities.")

st.caption("💡 Next: Real-time auto-refresh + clickable rows")
