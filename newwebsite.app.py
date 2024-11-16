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
)

# Main Title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📊 Stock Analysis & Investment Guide</h1>", unsafe_allow_html=True)
st.write("Analyze stocks with Fundamental and Technical Analysis to make informed investment decisions.")

# Sidebar
st.sidebar.header("Stock Selection")
ticker_symbol = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL)", "AAPL")
fetch_data_button = st.sidebar.button("Analyze Stock")

if fetch_data_button:
    try:
        # Fetch Stock Data
        stock = yf.Ticker(ticker_symbol)
        stock_info = stock.info

        # Display Company Overview
        st.subheader(f"🏢 Company Overview: {stock_info.get('shortName', ticker_symbol)}")
        st.write(f"**Sector:** {stock_info.get('sector', 'N/A')}")
        st.write(f"**Industry:** {stock_info.get('industry', 'N/A')}")
        st.write(f"**Market Cap:** ${stock_info.get('marketCap', 'N/A'):,}")
        st.write(f"**Website:** {stock_info.get('website', 'N/A')}")

        # Fundamental Analysis
        st.subheader("📋 Fundamental Analysis")
        st.write(f"**P/E Ratio:** {stock_info.get('forwardPE', 'N/A')}")
        st.write(f"**P/B Ratio:** {stock_info.get('priceToBook', 'N/A')}")
        st.write(f"**EPS:** {stock_info.get('trailingEps', 'N/A')}")
        st.write(f"**Dividend Yield:** {stock_info.get('dividendYield', 'N/A')}")

        # Fetch Historical Data for Technical Analysis
        st.subheader("📈 Technical Analysis")
        historical_data = stock.history(period="1y")
        historical_data["SMA50"] = SMAIndicator(historical_data["Close"], 50).sma_indicator()
        historical_data["SMA200"] = SMAIndicator(historical_data["Close"], 200).sma_indicator()
        historical_data["RSI"] = RSIIndicator(historical_data["Close"], 14).rsi()
        macd_indicator = MACD(historical_data["Close"])
        historical_data["MACD"] = macd_indicator.macd()
        historical_data["Signal"] = macd_indicator.macd_signal()

        # Display Technical Charts
        st.write("**Moving Averages**")
        st.line_chart(historical_data[["Close", "SMA50", "SMA200"]])
        st.write("**MACD**")
        st.line_chart(historical_data[["MACD", "Signal"]])
        st.write("**RSI**")
        st.line_chart(historical_data["RSI"])

        # Recommendation Logic
        st.subheader("🔍 Recommendation")
        recommendation = "Hold"
        recommendation_color = "#FFC107"  # Yellow
        if historical_data["SMA50"].iloc[-1] > historical_data["SMA200"].iloc[-1] and historical_data["RSI"].iloc[-1] < 70:
            recommendation = "Buy"
            recommendation_color = "#4CAF50"  # Green
        elif historical_data["SMA50"].iloc[-1] < historical_data["SMA200"].iloc[-1] or historical_data["RSI"].iloc[-1] > 70:
            recommendation = "Sell"
            recommendation_color = "#F44336"  # Red

        st.markdown(
            f'<div style="text-align: center; font-size: 24px; font-weight: bold; color: {recommendation_color};">'
            f"Recommendation: {recommendation}</div>",
            unsafe_allow_html=True,
        )

    except Exception as e:
        st.error(f"An error occurred: {e}")
