# app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator

# Page Configuration
st.set_page_config(
    page_title="Stock Analysis App",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Styling
st.markdown("""
    <style>
        .main-header { font-size: 40px; color: #4CAF50; font-weight: bold; text-align: center; margin-bottom: 20px; }
        .sub-header { font-size: 20px; color: #333; font-weight: bold; margin-top: 20px; }
        .highlight { font-weight: bold; color: #FF5722; }
        .stButton > button { background-color: #4CAF50; color: white; }
        .stButton > button:hover { background-color: #45A049; }
        .metric-container { text-align: center; margin-top: 20px; }
        .metric { font-size: 18px; font-weight: bold; color: #4CAF50; margin-bottom: 10px; }
        .metric-value { font-size: 24px; font-weight: bold; color: #FF5722; }
    </style>
""", unsafe_allow_html=True)

# Main Title
st.markdown('<div class="main-header">📊 Stock Analysis & Investment Guide</div>', unsafe_allow_html=True)
st.write("Get actionable insights on stocks through Fundamental and Technical Analysis.")

# Sidebar
st.sidebar.header("Stock Selection")
st.sidebar.write("Select a company to analyze:")
ticker_symbol = st.sidebar.text_input("Enter Stock Ticker", "AAPL")
fetch_data_button = st.sidebar.button("Analyze Stock")

if fetch_data_button:
    try:
        # Fetch Stock Data
        stock = yf.Ticker(ticker_symbol)
        stock_info = stock.info
        st.markdown(f"<div class='sub-header'>🏢 {stock_info.get('shortName', ticker_symbol)}</div>", unsafe_allow_html=True)

        # Display Basic Company Info
        col1, col2, col3 = st.columns(3)
        col1.metric("Sector", stock_info.get("sector", "N/A"))
        col2.metric("Industry", stock_info.get("industry", "N/A"))
        col3.metric("Market Cap", f"${stock_info.get('marketCap', 0):,}")

        st.markdown('<div class="sub-header">📋 Fundamental Analysis</div>', unsafe_allow_html=True)
        fa_col1, fa_col2, fa_col3, fa_col4 = st.columns(4)
        fa_col1.metric("P/E Ratio", stock_info.get("forwardPE", "N/A"))
        fa_col2.metric("P/B Ratio", stock_info.get("priceToBook", "N/A"))
        fa_col3.metric("EPS", stock_info.get("trailingEps", "N/A"))
        fa_col4.metric("Dividend Yield", f"{stock_info.get('dividendYield', 0):.2%}")

        # Fetch Historical Data for Technical Analysis
        st.markdown('<div class="sub-header">📈 Technical Analysis</div>', unsafe_allow_html=True)
        historical_data = stock.history(period="1y")
        historical_data["SMA50"] = SMAIndicator(historical_data["Close"], 50).sma_indicator()
        historical_data["SMA200"] = SMAIndicator(historical_data["Close"], 200).sma_indicator()
        historical_data["RSI"] = RSIIndicator(historical_data["Close"], 14).rsi()
        macd_indicator = MACD(historical_data["Close"])
        historical_data["MACD"] = macd_indicator.macd()
        historical_data["Signal"] = macd_indicator.macd_signal()

        # Display Charts
        st.write("**Moving Averages**")
        st.line_chart(historical_data[["Close", "SMA50", "SMA200"]])
        st.write("**MACD**")
        st.line_chart(historical_data[["MACD", "Signal"]])
        st.write("**RSI**")
        st.line_chart(historical_data["RSI"])

        # Recommendation Logic
        st.markdown('<div class="sub-header">🔍 Recommendation</div>', unsafe_allow_html=True)
        recommendation = "Hold"
        recommendation_color = "#FFC107"  # Yellow
        if historical_data["SMA50"].iloc[-1] > historical_data["SMA200"].iloc[-1] and historical_data["RSI"].iloc[-1] < 70:
            recommendation = "Buy"
            recommendation_color = "#4CAF50"  # Green
        elif historical_data["SMA50"].iloc[-1] < historical_data["SMA200"].iloc[-1] or historical_data["RSI"].iloc[-1] > 70:
            recommendation = "Sell"
            recommendation_color = "#F44336"  # Red

        st.markdown(
            f'<div class="metric-container">'
            f'<span class="metric">Recommendation:</span><br>'
            f'<span class="metric-value" style="color:{recommendation_color};">{recommendation}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    except Exception as e:
        st.error(f"An error occurred: {e}")
