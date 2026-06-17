import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Import all scanners
from scanners.massive_scanner import get_live_gainers as massive_scanner
from scanners.yfinance_scanner import get_live_gainers as yfinance_scanner
from scanners.finviz_scanner import get_live_gainers as finviz_scanner

st.set_page_config(page_title="Stock Screener", layout="wide")

st.title("🚀 Stock Screener - Momentum Play Detector")
st.caption("Modular Multi-Source Scanner | Finding ANY stock in the market")

# =============================================
# SIDEBAR
# =============================================
with st.sidebar:
    st.header("Scanner Source")
    scanner_choice = st.radio(
        "Choose Data Source",
        ["Finviz (Best Free Market Scan)", "yFinance (Reliable)", "Massive.io (Paid)"],
        index=0
    )
    
    st.header("Filters")
    gap_min = st.slider("Gap Min %", 0.0, 30.0, 2.0)
    min_volume = st.number_input("Min Volume", value=20000, step=10000)
    min_price = st.number_input("Min Price $", value=0.5, step=0.1)

    st.header("Risk Management")
    account_size = st.number_input("Account Size ($)", value=1000)
    risk_percent = st.slider("Risk % per Trade", 1.0, 10.0, 5.0)

# =============================================
# MAIN LAYOUT
# =============================================
col_table, col_details = st.columns([3.5, 2.2])

with col_table:
    st.subheader("📊 Live Momentum Scanner")
    st.caption(f"Using: **{scanner_choice}** | Auto-discovers plays across the market")

    if st.button("🔄 Run Live Scan", type="primary", use_container_width=True):
        with st.spinner(f"Scanning market with {scanner_choice}..."):
            if "Finviz" in scanner_choice:
                df = finviz_scanner(min_change=gap_min, min_volume=min_volume)
            elif "yFinance" in scanner_choice:
                df = yfinance_scanner(min_change=gap_min, min_volume=min_volume)
            else:
                df = massive_scanner(min_change=gap_min, min_volume=min_volume)
            
            if not df.empty:
                df_display = df.copy()
                df_display["Price"] = df_display["Price"].apply(lambda x: f"${x:.3f}")
                df_display["% Change"] = df_display["% Change"].apply(lambda x: f"+{x:.2f}%")
                
                st.dataframe(df_display, use_container_width=True, hide_index=True, height=650)
                st.success(f"✅ Found {len(df)} plays matching your criteria")
            else:
                st.warning("No plays found. Try lowering Gap Min % or Min Volume.")

with col_details:
    st.subheader("Selected Ticker Analysis")
    ticker = st.text_input("Ticker Symbol", value="").upper().strip()
    
    if st.button("Load Chart + Zones", use_container_width=True) and ticker:
        st.info(f"📈 Loading {ticker} with Supply/Demand Zones...")
        fig = go.Figure()
        fig.update_layout(title=f"{ticker} - Daily Chart", height=480, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

st.divider()
st.info("💡 Finviz currently gives the broadest free market coverage. Upgrade Massive for real-time power.")
