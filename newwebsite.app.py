import streamlit as st
import yfinance as yf
import pandas as pd

# Streamlit app details
st.set_page_config(page_title="Financial Analysis", layout="wide")

with st.sidebar:
    st.title("Financial Analysis")
    ticker = st.text_input("Enter a stock ticker (e.g. AAPL)", "AAPL")
    period = st.selectbox("Enter a time frame", ("1D", "5D", "1M", "6M", "YTD", "1Y", "5Y"), index=2)
    button = st.button("Submit")

# Format market cap and enterprise value into something readable
def format_value(value):
    if not isinstance(value, (int, float)):
        return "N/A"
    suffixes = ["", "K", "M", "B", "T"]
    suffix_index = 0
    while value >= 1000 and suffix_index < len(suffixes) - 1:
        value /= 1000
        suffix_index += 1
    return f"${value:.1f}{suffixes[suffix_index]}"

# If Submit button is clicked
if button:
    if not ticker.strip():
        st.error("Please provide a valid stock ticker.")
    else:
        try:
            with st.spinner('Please wait...'):
                # Retrieve stock data
                stock = yf.Ticker(ticker)
                info = stock.info

                st.subheader(f"{ticker} - {info.get('longName', 'N/A')}")

                # Plot historical stock price data
                if period == "1D":
                    history = stock.history(period="1d", interval="1h")
                elif period == "5D":
                    history = stock.history(period="5d", interval="1d")
                elif period == "1M":
                    history = stock.history(period="1mo", interval="1d")
                elif period == "6M":
                    history = stock.history(period="6mo", interval="1wk")
                elif period == "YTD":
                    history = stock.history(period="ytd", interval="1mo")
                elif period == "1Y":
                    history = stock.history(period="1y", interval="1mo")
                elif period == "5Y":
                    history = stock.history(period="5y", interval="3mo")
                
                chart_data = pd.DataFrame(history["Close"])
                st.line_chart(chart_data)

                col1, col2, col3 = st.columns(3)

                # Display stock information as a dataframe
                country = info.get('country', 'N/A')
                sector = info.get('sector', 'N/A')
                industry = info.get('industry', 'N/A')
                market_cap = format_value(info.get('marketCap', None))
                ent_value = format_value(info.get('enterpriseValue', None))
                employees = info.get('fullTimeEmployees', 'N/A')

                stock_info = [
                    ("Stock Info", "Value"),
                    ("Country", country),
                    ("Sector", sector),
                    ("Industry", industry),
                    ("Market Cap", market_cap),
                    ("Enterprise Value", ent_value),
                    ("Employees", employees)
                ]
                
                df = pd.DataFrame(stock_info[1:], columns=stock_info[0])
                col1.dataframe(df, width=400, hide_index=True)
                
                # Display price information as a dataframe
                def safe_format(value, prefix="$", suffix=""):
                    if not isinstance(value, (int, float)):
                        return "N/A"
                    return f"{prefix}{value:.2f}{suffix}"

                current_price = safe_format(info.get('currentPrice'))
                prev_close = safe_format(info.get('previousClose'))
                day_high = safe_format(info.get('dayHigh'))
                day_low = safe_format(info.get('dayLow'))
                ft_week_high = safe_format(info.get('fiftyTwoWeekHigh'))
                ft_week_low = safe_format(info.get('fiftyTwoWeekLow'))
                
                price_info = [
                    ("Price Info", "Value"),
                    ("Current Price", current_price),
                    ("Previous Close", prev_close),
                    ("Day High", day_high),
                    ("Day Low", day_low),
                    ("52 Week High", ft_week_high),
                    ("52 Week Low", ft_week_low)
                ]
                
                df = pd.DataFrame(price_info[1:], columns=price_info[0])
                col2.dataframe(df, width=400, hide_index=True)

                # Display business metrics as a dataframe
                forward_eps = safe_format(info.get('forwardEps'), prefix="")
                forward_pe = safe_format(info.get('forwardPE'), prefix="")
                peg_ratio = safe_format(info.get('pegRatio'), prefix="")
                dividend_rate = safe_format(info.get('dividendRate'))
                dividend_yield = safe_format(info.get('dividendYield', 0) * 100, suffix="%")
                recommendation = info.get('recommendationKey', 'N/A').capitalize()
                
                biz_metrics = [
                    ("Business Metrics", "Value"),
                    ("EPS (FWD)", forward_eps),
                    ("P/E (FWD)", forward_pe),
                    ("PEG Ratio", peg_ratio),
                    ("Div Rate (FWD)", dividend_rate),
                    ("Div Yield (FWD)", dividend_yield),
                    ("Recommendation", recommendation)
                ]
                
                df = pd.DataFrame(biz_metrics[1:], columns=biz_metrics[0])
                col3.dataframe(df, width=400, hide_index=True)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
