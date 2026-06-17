import streamlit as st
import pandas as pd
from scanners.massive_scanner import get_live_gainers
import plotly.graph_objects as go

st.set_page_config(page_title="Stock Screener", layout="wide", initial_sidebar_state="expanded")

st.title("🚀 Stock Screener - Momentum Play Detector")
st.caption("Real-time Massive.io Scanner | Sykes / Touhey Style")

# Sidebar
with st.sidebar:
    st.header("Filters")
    gap_min = st.slider("Gap Min %", 0.0, 20.0, 3.0)
    min_volume = st.number_input("Min Volume", value=50000, step=10000)
    min_price = st.number_input("Min Price $", value=2.0)

    st.header("Risk")
    account_size = st.number_input("Account Size ($)", value=1000)
    risk_percent = st.slider("Risk % per Trade", 1.0, 10.0, 5.0)

# Main Layout
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Live Scanner")
    if st.button("🔄 Run Live Scan", type="primary", use_container_width=True):
        with st.spinner("Fetching real gainers from Massive..."):
            df = get_live_gainers(min_change=gap_min, min_volume=min_volume)

            if not df.empty:
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.success(f"Found {len(df)} plays")
            else:
                st.warning("No plays found. Try lowering the Gap Min %.")

with col2:
    st.subheader("Selected Ticker")
    ticker = st.text_input("Ticker", "GME").upper().strip()
    if st.button("Load Chart + Zones"):
        st.info(f"Chart + Supply/Demand Zones for {ticker} (in progress)")
        fig = go.Figure()
        fig.update_layout(title=f"{ticker} Daily Chart", height=500)
        st.plotly_chart(fig, use_container_width=True)

st.subheader("Alerts & Log")
st.info("Run a scan above to see opportunities.")

tab1, tab2 = st.tabs(["Watchlist", "Backtester"])
with tab1:
    st.write("Your saved plays will go here")
with tab2:
    st.write("Backtester coming soon")
