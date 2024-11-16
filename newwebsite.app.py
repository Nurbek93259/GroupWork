# Updating the code with simpler explanations, pros, and cons for the tablesimplified_code = """
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

def calculate_moving_averages(data, short_window=50, long_window=200):
    data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_long'] = data['Close'].rolling(window=long_window).mean()
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

def generate_recommendations(data):
    recommendations = []

    # SMA and EMA Crossovers
    if data['SMA_short'].iloc[-1] > data['SMA_long'].iloc[-1]:
        recommendations.append({
            "Indicator": "SMA (50 vs 200)",
            "Action": "BUY",
            "Explanation": "The short-term average is higher than the long-term average. This suggests the price is going up.",
            "Pros": "Good for seeing long-term growth trends.",
            "Cons": "Might miss quick changes in the price."
        })
    else:
        recommendations.append({
            "Indicator": "SMA (50 vs 200)",
            "Action": "SELL",
            "Explanation": "The short-term average is lower than the long-term average. This suggests the price is going down.",
            "Pros": "Good for confirming a downward trend.",
            "Cons": "Might react slowly to sudden changes."
        })

    if data['EMA_short'].iloc[-1] > data['EMA_long'].iloc[-1]:
        recommendations.append({
            "Indicator": "EMA (50 vs 200)",
            "Action": "BUY",
            "Explanation": "The short-term EMA is higher than the long-term EMA, showing a price increase.",
            "Pros": "Responds quickly to recent price changes.",
            "Cons": "Might give false signals if prices jump around a lot."
        })
    else:
        recommendations.append({
            "Indicator": "EMA (50 vs 200)",
            "Action": "SELL",
            "Explanation": "The short-term EMA is lower than the long-term EMA, showing a price decrease.",
            "Pros": "Responds quickly to recent price changes.",
            "Cons": "Might give false signals if prices jump around a lot."
        })

    if data['RSI'].iloc[-1] < 30:
        recommendations.append({
            "Indicator": "RSI",
            "Action": "BUY",
            "Explanation": "The stock is oversold. This means it might be cheap and could go up soon.",
            "Pros": "Helps find good times to buy.",
            "Cons": "Might not work well if prices are falling strongly."
        })
    elif data['RSI'].iloc[-1] > 70:
        recommendations.append({
            "Indicator": "RSI",
            "Action": "SELL",
            "Explanation": "The stock is overbought. This means it might be expensive and could go down soon.",
            "Pros": "Helps find good times to sell.",
            "Cons": "Might not work well if prices are rising strongly."
        })
    else:
        recommendations.append({
            "Indicator": "RSI",
            "Action": "HOLD",
            "Explanation": "The stock is in a normal range. No action needed.",
            "Pros": "You don’t need to do anything right now.",
            "Cons": "Might miss chances to act early."
        })

    if data['MACD'].iloc[-1] > data['Signal_Line'].iloc[-1]:
        recommendations.append({
            "Indicator": "MACD",
            "Action": "BUY",
            "Explanation": "The MACD shows upward momentum in the stock.",
            "Pros": "Good at spotting trends early.",
            "Cons": "Might give wrong signals in unstable markets."
        })
    else:
        recommendations.append({
            "Indicator": "MACD",
            "Action": "SELL",
            "Explanation": "The MACD shows downward momentum in the stock.",
            "Pros": "Good at spotting when prices might fall.",
            "Cons": "Might give wrong signals in unstable markets."
        })

    return recommendations

def display_recommendations_table(recommendations):
    st.write("### Recommendations and Explanations")
    table = pd.DataFrame(recommendations)
    st.dataframe(table)

def plot_analysis(data, ticker):
    st.write(f"### Technical Analysis for {ticker}")

    # Plot Price and Moving Averages
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label='Close Price', color='blue')
    plt.plot(data['SMA_short'], label='Short-term SMA (50)', color='orange')
    plt.plot(data['SMA_long'], label='Long-term SMA (200)', color='green')
    plt.plot(data['EMA_short'], label='Short-term EMA (50)', linestyle='--', color='red')
    plt.plot(data['EMA_long'], label='Long-term EMA (200)', linestyle='--', color='purple')
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

        # Generate and display recommendations
        recommendations = generate_recommendations(stock_data)
        display_recommendations_table(recommendations)

# Writing the updated Python script to a file
simplified_script_path = "/mnt/data/technical_analysis_app_simplified_explanations.py"
with open(simplified_script_path, "w") as f:
    f.write(simplified_code)

# Provide the file path for the updated script
simplified_script_path
