import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def download_data(ticker, start_date, end_date):
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        return stock_data
    except Exception as e:
        st.error(f"Error downloading data: {e}")
        return None

def calculate_moving_averages(data, short_window=20, long_window=50):
    data['SMA'] = data['Close'].rolling(window=short_window).mean()
    data['LMA'] = data['Close'].rolling(window=long_window).mean()

def calculate_rsi(data, window=14):
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

def plot_analysis(data, ticker):
    st.write(f"### Technical Analysis for {ticker}")
    
    # Plot Price and Moving Averages
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label='Close Price', color='blue')
    plt.plot(data['SMA'], label='Short-term SMA (20)', color='orange')
    plt.plot(data['LMA'], label='Long-term LMA (50)', color='green')
    plt.title('Price Trend Analysis with Moving Averages')
    plt.legend()
    st.pyplot(plt)

    # Plot RSI
    plt.figure(figsize=(12, 4))
    plt.plot(data['RSI'], label='RSI', color='purple')
    plt.axhline(70, linestyle='--', color='red', label='Overbought (70)')
    plt.axhline(30, linestyle='--', color='green', label='Oversold (30)')
    plt.title('Momentum Indicator: RSI')
    plt.legend()
    st.pyplot(plt)

# Streamlit UI
st.title("Stock Technical Analysis App")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL):", "AAPL")
start_date = st.date_input("Start Date", datetime(2022, 1, 1))
end_date = st.date_input("End Date", datetime(2023, 1, 1))

if st.button("Analyze"):
    stock_data = download_data(ticker, start_date, end_date)
    if stock_data is not None:
        calculate_moving_averages(stock_data)
        calculate_rsi(stock_data)
        plot_analysis(stock_data, ticker)
