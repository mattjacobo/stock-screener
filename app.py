import streamlit as st
import pandas as pd
from scanners.massive_scanner import get_live_gainers
import plotly.graph_objects as go

st.set_page_config(page_title="Stock Screener", layout="wide")

st.title("🚀 Stock Screener - Momentum Play Detector")
st.caption("Real-time Massive.io | Auto Discovery")

with st.sidebar:
    st.header("Filters")
    gap_min = st.slider("Gap Min %", 0.0, 30.0, 1.0)
    min_volume = st.number_input("Min Volume", value=10000, step=5000)

if st.button("🔄 Run Live Scan", type="primary", use_container_width=True):
    with st.spinner("Scanning..."):
        df, debug_info = get_live_gainers(min_change=gap_min, min_volume=min_volume)
        
        # Show debug info
        with st.expander("🔍 Debug Information", expanded=True):
            for line in debug_info:
                st.write(line)
        
        if not df.empty:
            df_display = df.copy()
            df_display["Price"] = df_display["Price"].apply(lambda x: f"${x:.3f}")
            df_display["% Change"] = df_display["% Change"].apply(lambda x: f"+{x:.2f}%")
            
            st.dataframe(df_display, use_container_width=True, hide_index=True, height=600)
            st.success(f"Found {len(df)} plays")
        else:
            st.warning("No plays found with current filters.")

st.divider()
st.info("Check the Debug Information expander above after each scan.")
