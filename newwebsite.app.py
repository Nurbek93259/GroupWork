import os
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from datetime import datetime

# Create the app layout
st.set_page_config(page_title="Stock Analysis App", layout="wide")

# Sidebar Options
st.sidebar.title("Stock Analysis Options")
option = st.sidebar.radio("Choose Analysis Type:", ["Company Overview & Fundamental Analysis", "Technical Analysis"])

# User Input for Stock Ticker
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL):", "AAPL")

# Fetch Stock Data
if ticker:
    stock = yf.Ticker(ticker)

    # Company Overview & Fundamental Analysis
    if option == "Company Overview & Fundamental Analysis":
        st.title(f"Company Overview: {ticker.upper()}")

        # Company Details
        info = stock.info
        st.subheader("About the Company")
        st.write(info.get("longBusinessSummary", "Company information is not available."))
        st.write(f"**Industry:** {info.get('industry', 'N/A')}")
        st.write(f"**Country:** {info.get('country', 'N/A')}")
        if "website" in info:
            st.markdown(f"[**Website**]({info['website']})", unsafe_allow_html=True)

        # Candlestick Chart
        st.subheader("Stock Performance: Candlestick Chart")
        historical = stock.history(period="1y")
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=historical.index,
                    open=historical['Open'],
                    high=historical['High'],
                    low=historical['Low'],
                    close=historical['Close'],
                )
            ]
        )
        fig.update_layout(
            title=f"Candlestick Chart for {ticker.upper()}",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Financial Metrics
        st.subheader("Financial Metrics")
        financials = stock.financials.T
        if not financials.empty:
            st.write("Net Income (Last 4 Years):")
            financials = financials.head(4)
            st.write(financials[['Net Income']])
        else:
            st.warning("Financial data is not available.")

    # Technical Analysis
    elif option == "Technical Analysis":
        st.title(f"Technical Analysis: {ticker.upper()}")

        # Input Dates
        start_date = st.sidebar.date_input("Start Date", datetime(2022, 1, 1))
        end_date = st.sidebar.date_input("End Date", datetime(2023, 1, 1))

        # Fetch and Process Data
        try:
            stock_data = stock.history(start=start_date, end=end_date)
            stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
            stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()
            stock_data['RSI'] = 100 - (100 / (1 + stock_data['Close'].pct_change().rolling(window=14).mean()))

            # Display Data
            st.subheader("Price Chart with Moving Averages")
            plt.figure(figsize=(10, 5))
            plt.plot(stock_data.index, stock_data['Close'], label="Close Price", color="blue")
            plt.plot(stock_data.index, stock_data['SMA_50'], label="50-Day SMA", color="orange")
            plt.plot(stock_data.index, stock_data['SMA_200'], label="200-Day SMA", color="green")
            plt.title("Stock Price with Moving Averages")
            plt.xlabel("Date")
            plt.ylabel("Price (USD)")
            plt.legend()
            st.pyplot(plt)

            # Recommendations
            st.subheader("Recommendations Based on Indicators")
            recommendations = []
            if stock_data['SMA_50'].iloc[-1] > stock_data['SMA_200'].iloc[-1]:
                recommendations.append({"Indicator": "SMA (50 vs 200)", "Recommendation": "BUY"})
            else:
                recommendations.append({"Indicator": "SMA (50 vs 200)", "Recommendation": "SELL"})
            st.table(pd.DataFrame(recommendations))

        except Exception as e:
            st.error(f"Error fetching data: {e}")
else:
    st.warning("Please enter a valid stock ticker.")
