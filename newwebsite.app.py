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
    data['EMA_short'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA_long'] = data['Close'].ewm(span=long_window, adjust=False).mean()

def calculate_rsi(data, window=14):
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

def calculate_macd(data, short_span=12, long_span=26, signal_span=9):
    data['MACD'] = data['Close'].ewm(span=short_span, adjust=False).mean() - data['Close'].ewm(span=long_span, adjust=False).mean()
    data['Signal_Line'] = data['MACD'].ewm(span=signal_span, adjust=False).mean()

def generate_explanations(data):
    explanations = []

    # SMA and EMA Crossovers
    if data['SMA'].iloc[-1] > data['LMA'].iloc[-1]:
        explanations.append("The short-term SMA is above the long-term LMA, indicating a BUY signal (Golden Cross).")
    elif data['SMA'].iloc[-1] < data['LMA'].iloc[-1]:
        explanations.append("The short-term SMA is below the long-term LMA, indicating a SELL signal (Death Cross).")
    
    if data['EMA_short'].iloc[-1] > data['EMA_long'].iloc[-1]:
        explanations.append("The short-term EMA is above the long-term EMA, indicating a BUY signal.")
    elif data['EMA_short'].iloc[-1] < data['EMA_long'].iloc[-1]:
        explanations.append("The short-term EMA is below the long-term EMA, indicating a SELL signal.")

    # RSI Analysis
    if data['RSI'].iloc[-1] < 30:
        explanations.append("The RSI is below 30, indicating the stock is OVERSOLD. This is a BUY signal.")
    elif data['RSI'].iloc[-1] > 70:
        explanations.append("The RSI is above 70, indicating the stock is OVERBOUGHT. This is a SELL signal.")
    else:
        explanations.append("The RSI is between 30 and 70, indicating neutral momentum. No strong buy or sell signal.")

    # MACD Analysis
    if data['MACD'].iloc[-1] > data['Signal_Line'].iloc[-1]:
        explanations.append("The MACD line is above the signal line, indicating a BUY signal.")
    elif data['MACD'].iloc[-1] < data['Signal_Line'].iloc[-1]:
        explanations.append("The MACD line is below the signal line, indicating a SELL signal.")

    return explanations

def plot_analysis(data, ticker):
    st.write(f"### Technical Analysis for {ticker}")

    # Plot Price and Moving Averages
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label='Close Price', color='blue')
    plt.plot(data['SMA'], label='Short-term SMA (20)', color='orange')
    plt.plot(data['LMA'], label='Long-term LMA (50)', color='green')
    plt.plot(data['EMA_short'], label='Short-term EMA (20)', linestyle='--', color='red')
    plt.plot(data['EMA_long'], label='Long-term EMA (50)', linestyle='--', color='purple')
    plt.title('Price Trend Analysis with Moving Averages and EMAs')
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

    # Plot MACD
    plt.figure(figsize=(12, 4))
    plt.plot(data['MACD'], label='MACD Line', color='blue')
    plt.plot(data['Signal_Line'], label='Signal Line', color='orange')
    plt.axhline(0, linestyle='--', color='gray', label='Zero Line')
    plt.title('Momentum Indicator: MACD')
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
        calculate_macd(stock_data)
        plot_analysis(stock_data, ticker)

        # Generate and display explanations
        explanations = generate_explanations(stock_data)
        st.write("### Recommendations and Explanations")
        for explanation in explanations:
            st.write(f"- {explanation}")
