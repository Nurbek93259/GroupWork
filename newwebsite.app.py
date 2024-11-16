# Enhancing the code to include explanations for buy/sell signals based on the analysis

enhanced_code = """
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

def generate_explanations(data):
    explanations = []
    if data['SMA'].iloc[-1] > data['LMA'].iloc[-1]:
        explanations.append("The short-term SMA is above the long-term LMA, indicating a BUY signal.")
    elif data['SMA'].iloc[-1] < data['LMA'].iloc[-1]:
        explanations.append("The short-term SMA is below the long-term LMA, indicating a SELL signal.")
    else:
        explanations.append("The short-term SMA is equal to the long-term LMA, indicating a HOLD signal.")

    if data['RSI'].iloc[-1] < 30:
        explanations.append("The RSI is below 30, indicating the stock is OVERSOLD. This is a BUY signal.")
    elif data['RSI'].iloc[-1] > 70:
        explanations.append("The RSI is above 70, indicating the stock is OVERBOUGHT. This is a SELL signal.")
    else:
        explanations.append("The RSI is between 30 and 70, indicating neutral momentum. No strong buy or sell signal.")

    return explanations

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

        # Generate and display explanations
        explanations = generate_explanations(stock_data)
        st.write("### Recommendations and Explanations")
        for explanation in explanations:
            st.write(f"- {explanation}")
"""

# Writing the enhanced Python script to a file
enhanced_script_path = "/mnt/data/technical_analysis_app_with_explanations.py"
with open(enhanced_script_path, "w") as f:
    f.write(enhanced_code)

# Provide the file path for the enhanced script
enhanced_script_path
