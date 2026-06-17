import streamlit as st
import pandas as pd
from scanners.massive_scanner import get_live_gainers
import plotly.graph_objects as go

st.set_page_config(page_title="Stock Screener", layout="wide", initial_sidebar_state="expanded")

st.title("🚀 Stock Screener - Momentum Play Detector")
st.caption("Real-time Massive.io | Auto Discovery | Sykes/Touhey Style")

# Sidebar Filters (IBKR Style)
with st.sidebar:
    st.header("🔍 Strategy Filters")
    
    gap_min = st.slider("Gap Min %", 0.0, 30.0, 4.0)
    min_volume = st.number_input("Min Volume", value=50000, step=25000)
    min_price = st.number_input("Min Price $", value=1.0, step=0.5)
    max_float_m = st.number_input("Max Float (M)", value=300, step=50)

    st.header("Risk Management")
    account_size = st.number_input("Account Size ($)", value=1000)
    risk_percent = st.slider("Risk % per Trade", 1.0, 10.0, 5.0)

    st.divider()
    if st.button("💾 Save Filters", use_container_width=True):
        st.success("Filters saved (demo)")

# Main Layout
col_table, col_details = st.columns([3.5, 2.2])

with col_table:
    st.subheader("📊 Live Momentum Scanner")
    st.caption("Auto-discovers plays based on your filters — no manual input needed")

    if st.button("🔄 Run Live Scan", type="primary", use_container_width=True):
        with st.spinner("Scanning market with Massive.io..."):
            df = get_live_gainers(min_change=gap_min, min_volume=min_volume)

            if not df.empty:
                # Color coding
                def highlight_change(val):
                    if val > 0:
                        return 'background-color: #0e4a2e; color: white'
                    return 'background-color: #4a1d1d; color: white'
                
                styled = df.style.applymap(highlight_change, subset=['% Change'])
                
                st.dataframe(styled, use_container_width=True, hide_index=True, height=650)
                st.success(f"✅ Found {len(df)} plays matching your criteria")
            else:
                st.warning("No plays found. Try lowering Gap Min % or Volume.")

with col_details:
    st.subheader("Selected Ticker Analysis")
    
    # Auto-update when row is clicked (Streamlit limitation - we'll improve this)
    ticker = st.text_input("Or enter manually", value="").upper().strip()
    
    if st.button("Load Chart + Zones", use_container_width=True):
        if ticker:
            st.info(f"📈 Loading {ticker} with Supply/Demand Zones...")
            fig = go.Figure()
            fig.update_layout(title=f"{ticker} - Daily Chart", height=480, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

# Bottom Alerts
st.divider()
st.subheader("🛎️ Alerts & Log")
st.info("Run scans above to generate alerts. Real-time alerts coming soon.")

st.caption("💡 Pro Tip: Refresh the page or click Run Live Scan often during market hours.")
