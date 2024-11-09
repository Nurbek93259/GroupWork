import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Setting the page layout
st.set_page_config(layout="centered", page_title="Golden Cross Analysis")

# Sidebar inputs
st.sidebar.header("Input")

# Input for stock symbol
stock_symbol = st.sidebar.text_input("Stock symbol:", "NVDA")

# Sliders for moving average periods
short_ma = st.sidebar.slider("Short-term moving average days:", min_value=10, max_value=100, value=10)
long_ma = st.sidebar.slider("Long-term moving average days:", min_value=50, max_value=200, value=50)

# Date inputs
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2021-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("today"))

# Fetching and processing data
if st.button("Analyze"):
    # Download stock data
    data = yf.download(stock_symbol, start=start_date, end=end_date)

    # Calculate moving averages
    data["Short_MA"] = data["Close"].rolling(window=short_ma).mean()
    data["Long_MA"] = data["Close"].rolling(window=long_ma).mean()

    # Plotting with candlesticks
    fig = go.Figure()

    # Candlestick trace for stock price
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name="Candlestick"
    ))

    # Adding moving averages to the plot
    fig.add_trace(go.Scatter(x=data.index, y=data['Short_MA'], mode='lines', name=f'{short_ma}-Day MA', line=dict(width=1.5)))
    fig.add_trace(go.Scatter(x=data.index, y=data['Long_MA'], mode='lines', name=f'{long_ma}-Day MA', line=dict(width=1.5)))

    # Highlighting Golden Cross events
    golden_cross = (data['Short_MA'] > data['Long_MA']) & (data['Short_MA'].shift(1) <= data['Long_MA'].shift(1))
    golden_cross_dates = data[golden_cross].index

    # Ensure dates are in datetime format before adding to Plotly
    golden_cross_dates = pd.to_datetime(golden_cross_dates)

    # Debugging output to verify date format
    st.write("Golden Cross Dates (for debugging):", golden_cross_dates)

    # Adding vertical lines for Golden Cross dates
    for date in golden_cross_dates:
        fig.add_vline(x=date, line=dict(color="green", width=1), annotation_text="Golden Cross", annotation_position="top")

    # Update layout for better visualization
    fig.update_layout(
        title=f"{stock_symbol} Price with {short_ma}-Day and {long_ma}-Day Moving Averages",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,  # Hide the rangeslider to focus on the chart
        template="plotly_dark"
    )

    # Display plot
    st.plotly_chart(fig, use_container_width=True)

    # Display data table (optional)
    st.subheader("Data with Moving Averages")
    st.write(data[["Open", "High", "Low", "Close", "Short_MA", "Long_MA"]].dropna())
