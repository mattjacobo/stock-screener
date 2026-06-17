import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

# Import scanners
from scanners.massive_scanner import get_live_gainers as massive_scanner
from scanners.yfinance_scanner import get_live_gainers as yfinance_scanner

st.set_page_config(page_title="Stock Screener", layout="wide")

st.title("🚀 Stock Screener - Momentum Play Detector")
st.caption("Multi-Source Scanner + Interactive Charts")

# Session state
if 'selected_ticker' not in st.session_state:
    st.session_state.selected_ticker = None
if 'chart_timeframe' not in st.session_state:
    st.session_state.chart_timeframe = "1d"

# =============================================
# SIDEBAR
# =============================================
with st.sidebar:
    st.header("Scanner Source")
    scanner_choice = st.radio(
        "Choose Data Source",
        ["yFinance (Reliable)", "Massive.io (Paid)"],
        index=0
    )
    
    st.header("Filters")
    gap_min = st.slider("Gap Min %", 0.0, 30.0, 1.0)
    min_volume = st.number_input("Min Volume", value=10000, step=5000)

    st.header("Risk Management")
    account_size = st.number_input("Account Size ($)", value=1000)
    risk_percent = st.slider("Risk % per Trade", 1.0, 10.0, 5.0)

# =============================================
# MAIN LAYOUT
# =============================================
col_table, col_details = st.columns([3.5, 2.2])

with col_table:
    st.subheader("📊 Live Momentum Scanner")
    
    if st.button("🔄 Run Live Scan", type="primary", use_container_width=True):
        with st.spinner(f"Scanning with {scanner_choice}..."):
            if "yFinance" in scanner_choice:
                df = yfinance_scanner(min_change=gap_min, min_volume=min_volume)
            else:
                df = massive_scanner(min_change=gap_min, min_volume=min_volume)
            
            if not df.empty:
                df_display = df.copy()
                df_display["Price"] = df_display["Price"].apply(lambda x: f"${x:.3f}")
                df_display["% Change"] = df_display["% Change"].apply(lambda x: f"+{x:.2f}%")
                
                # Clickable table
                event = st.dataframe(
                    df_display, 
                    use_container_width=True, 
                    hide_index=True, 
                    height=650,
                    on_select="rerun",
                    selection_mode="single-row"
                )
                
                if event and len(event.selection["rows"]) > 0:
                    selected_idx = event.selection["rows"][0]
                    st.session_state.selected_ticker = df_display.iloc[selected_idx]["Ticker"]
            else:
                st.warning("No plays found. Try lowering filters.")

with col_details:
    st.subheader("Selected Ticker Analysis")
    
    display_ticker = st.text_input("Ticker Symbol", value=st.session_state.selected_ticker or "").upper().strip()
    
    # Timeframe buttons
    if display_ticker:
        st.write("**Timeframe**")
        cols = st.columns(6)
        timeframes = ["1m", "5m", "15m", "1h", "4h", "1d"]
        for i, tf in enumerate(timeframes):
            if cols[i].button(tf, use_container_width=True):
                st.session_state.chart_timeframe = tf

    if display_ticker:
        st.success(f"📈 **{display_ticker}** - {st.session_state.chart_timeframe.upper()}")
        
        with st.spinner("Loading chart..."):
            try:
                stock = yf.Ticker(display_ticker)
                hist = stock.history(period="60d", interval=st.session_state.chart_timeframe)
                
                if not hist.empty:
                    fig = go.Figure(data=[go.Candlestick(
                        x=hist.index,
                        open=hist['Open'],
                        high=hist['High'],
                        low=hist['Low'],
                        close=hist['Close'],
                        name=display_ticker
                    )])
                    
                    fig.update_layout(
                        title=f"{display_ticker} - {st.session_state.chart_timeframe.upper()} Chart",
                        height=550,
                        template="plotly_dark",
                        xaxis_rangeslider_visible=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("No data for this timeframe.")
            except Exception as e:
                st.error(f"Could not load chart: {e}")

st.divider()
st.info("💡 Click any row in the scanner table to auto-load its chart.")
