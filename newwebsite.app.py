# Updated code to fix the IndexError by checking for valid data before accessing indicators

fixed_code = """
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
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

    # Check if SMA and EMA columns are fully populated
    if data['SMA_short'].notna().all() and data['SMA_long'].notna().all():
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

    if data['EMA_short'].notna().all() and data['EMA_long'].notna().all():
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

    if data['RSI'].notna().all():
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

    if data['MACD'].notna().all() and data['Signal_Line'].notna().all():
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

def plot_interactive_charts(data, ticker):
    st.write(f"### Interactive Technical Analysis for {ticker}")

    # Plot Price and Moving Averages
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
    fig1.add_trace(go.Scatter(x=data.index, y=data['SMA_short'], mode='lines', name='SMA (50)'))
    fig1.add_trace(go.Scatter(x=data.index, y=data['SMA_long'], mode='lines', name='SMA (200)'))
    fig1.update_layout(title="Price with SMA", xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig1)

    # Plot RSI
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI'))
    fig2.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
    fig2.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
    fig2.update_layout(title="RSI Indicator", xaxis_title="Date", yaxis_title="RSI Value")
    st.plotly_chart(fig2)

    # Plot MACD
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=data.index, y=data['MACD'], mode='lines', name='MACD Line'))
    fig3.add_trace(go.Scatter(x=data.index, y=data['Signal_Line'], mode='lines', name='Signal Line'))
    fig3.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Zero Line")
    fig3.update_layout(title="MACD Indicator", xaxis_title="Date", yaxis_title="MACD Value")
    st.plotly_chart(fig3)

# Streamlit UI
st.title("Interactive Stock Technical Analysis App")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL):", "AAPL")
start_date = st.date_input("Start Date", datetime(2022, 1, 1))
end_date = st.date_input("End Date", datetime(2023, 1, 1))

if st.button("Analyze"):
    stock_data = download_data(ticker, start_date, end_date)
    if stock_data is not None:
        calculate_moving_averages(stock_data)
        calculate_rsi(stock_data)
        calculate_macd(stock_data)
        plot_interactive_charts(stock_data, ticker)

        # Generate and display recommendations
        recommendations = generate_recommendations(stock_data)
        display_recommendations_table(recommendations)
"""

# Writing the fixed Python script to a file
fixed_script_path = "/mnt/data/fixed_interactive_technical_analysis_app.py"
with open(fixed_script_path, "w") as f:
    f.write(fixed_code)

# Provide the file path for the fixed script
fixed_script_path
