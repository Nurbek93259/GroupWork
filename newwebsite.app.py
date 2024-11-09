pip install streamlit yfinance pandas numpy matplotlib
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Streamlit app title and description
st.title("Technical Indicator Dashboard")
st.write("Explore various technical indicators for stock analysis.")

# Sidebar for user input
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL", max_chars=10)
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2021-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-01-01"))
st.sidebar.write("### Indicator Settings")
sma_period = st.sidebar.slider("Simple Moving Average (SMA) Period", 5, 200, 50)
ema_period = st.sidebar.slider("Exponential Moving Average (EMA) Period", 5, 200, 20)
rsi_period = st.sidebar.slider("Relative Strength Index (RSI) Period", 5, 50, 14)

# Fetch stock data
data = yf.download(ticker, start=start_date, end=end_date)
data['Close'] = data['Close'].fillna(method='ffill')

# Calculate Technical Indicators
data['SMA'] = data['Close'].rolling(window=sma_period).mean()
data['EMA'] = data['Close'].ewm(span=ema_period, adjust=False).mean()

# RSI Calculation
delta = data['Close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
rs = gain / loss
data['RSI'] = 100 - (100 / (1 + rs))

# MACD Calculation
data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()
data['MACD'] = data['EMA_12'] - data['EMA_26']
data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

# Bollinger Bands Calculation
data['20_SMA'] = data['Close'].rolling(window=20).mean()
data['BB_upper'] = data['20_SMA'] + (data['Close'].rolling(window=20).std() * 2)
data['BB_lower'] = data['20_SMA'] - (data['Close'].rolling(window=20).std() * 2)

# Plotting
st.write(f"### {ticker} Stock Data and Indicators")

# Line Chart: Stock Price with SMA and EMA
st.write("#### Stock Price with Moving Averages")
fig, ax = plt.subplots()
ax.plot(data.index, data['Close'], label='Close Price', color='blue')
ax.plot(data.index, data['SMA'], label=f'{sma_period}-Day SMA', color='orange')
ax.plot(data.index, data['EMA'], label=f'{ema_period}-Day EMA', color='green')
ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.legend()
st.pyplot(fig)

# RSI Plot
st.write("#### Relative Strength Index (RSI)")
fig, ax = plt.subplots()
ax.plot(data.index, data['RSI'], label='RSI', color='purple')
ax.axhline(70, linestyle='--', alpha=0.5, color='red')  # Overbought level
ax.axhline(30, linestyle='--', alpha=0.5, color='green')  # Oversold level
ax.set_xlabel('Date')
ax.set_ylabel('RSI')
ax.legend()
st.pyplot(fig)

# MACD Plot
st.write("#### Moving Average Convergence Divergence (MACD)")
fig, ax = plt.subplots()
ax.plot(data.index, data['MACD'], label='MACD', color='blue')
ax.plot(data.index, data['Signal'], label='Signal Line', color='orange')
ax.bar(data.index, data['MACD'] - data['Signal'], label='MACD Histogram', color='gray', alpha=0.5)
ax.set_xlabel('Date')
ax.set_ylabel('MACD')
ax.legend()
st.pyplot(fig)

# Bollinger Bands Plot
st.write("#### Bollinger Bands")
fig, ax = plt.subplots()
ax.plot(data.index, data['Close'], label='Close Price', color='blue')
ax.plot(data.index, data['BB_upper'], label='Upper Bollinger Band', color='red', linestyle='--')
ax.plot(data.index, data['BB_lower'], label='Lower Bollinger Band', color='red', linestyle='--')
ax.fill_between(data.index, data['BB_lower'], data['BB_upper'], color='grey', alpha=0.3)
ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.legend()
st.pyplot(fig)

# Display raw data table at the end
st.write("#### Stock Data with Indicators")
st.dataframe(data[['Close', 'SMA', 'EMA', 'RSI', 'MACD', 'Signal', 'BB_upper', 'BB_lower']].dropna())
