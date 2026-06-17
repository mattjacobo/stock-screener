import streamlit as st
import pandas as pd
from scanners.massive_scanner import get_live_gainers
import plotly.graph_objects as go

st.set_page_config(page_title="Stock Screener", layout="wide", initial_sidebar_state="expanded")

st.title("🚀 Stock Screener - Momentum Play Detector")
st.caption("Real-time | Massive.io | Professional Scanner")

# ==================== SIDEBAR (IBKR Style) ====================
with st.sidebar:
    st.header("🔍 Filters")
    
    st.subheader("Price Action")
    gap_min = st.slider("Gap % (Min)", 0.0, 30.0, 4.0)
    min_price = st.number_input("Min Price $", value=1.0, step=0.5)
    min_volume = st.number_input("Min Volume", value=100000, step=50000)
    
    st.subheader("Universe")
    max_float = st.number_input("Max Float (M)", value=300, step=50)
    
    st.subheader("Risk Management")
    account_size = st.number_input("Account Size ($)", value=1000)
    risk_percent = st.slider("Max Risk % per Trade", 1.0, 10.0, 5.0)
    
    st.divider()
    st.button("💾 Save Current Filters", use_container_width=True)

# ==================== MAIN AREA ====================
col_table, col_details = st.columns([3.5, 2])

with col_table:
    st.subheader("Live Momentum Scanner")
    
    if st.button("🔄 Run Live Scan", type="primary", use_container_width=True):
        with st.spinner("Scanning market with Massive.io..."):
            df = get_live_gainers(min_change=gap_min, min_volume=min_volume)
            
            if not df.empty:
                # Color coding for % Change
                def color_change(val):
                    color = 'background-color: #0e4a2e' if val > 0 else 'background-color: #4a1d1d'
                    return color
                
                styled_df = df.style.applymap(color_change, subset=['% Change'])
                
                st.dataframe(
                    styled_df,
                    use_container_width=True,
                    hide_index=True,
                    height=600
                )
                st.success(f"Found {len(df)} momentum plays")
            else:
                st.warning("No plays found matching your filters. Try lowering Gap Min %.")

with col_details:
    st.subheader("Selected Ticker")
    ticker_input = st.text_input("Enter Ticker", value="GME").upper().strip()
    
    if st.button("Load Analysis", use_container_width=True):
        st.info(f"📊 Loading full analysis for **{ticker_input}**...")
        # Placeholder for real chart
        fig = go.Figure()
        fig.update_layout(
            title=f"{ticker_input} - Daily Chart with Supply/Demand Zones",
            height=450,
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("**Suggested Risk Setup**")
        st.write(f"Account: ${account_size} | Risk: {risk_percent}% → Position Size: ~${int(account_size * risk_percent/100)}")

# Bottom section
st.divider()
st.subheader("🛎️ Alerts & Recent Activity")
st.info("No alerts yet — run a scan to populate.")

st.caption("💡 Tip: Click 'Run Live Scan' regularly. We're building toward full IBKR-level power.")
