import streamlit as st
import requests

# Alpha Vantage API Key (Sign up at https://www.alphavantage.co/support/#api-key for a free API key)
API_KEY = "your_api_key_here"  # Replace with your actual Alpha Vantage API key

# Initial UI
st.title("Stock Profile Viewer")
ticker = st.text_input("Enter Ticker (e.g., NFLX):", "NFLX").upper()
buttonClicked = st.button("Fetch Data")

# Callbacks
if buttonClicked:
    # Construct the request URL
    request_url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}"

    try:
        # Send a GET request to the Alpha Vantage API
        response = requests.get(request_url)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse the JSON response
        data = response.json()

        if "Symbol" in data:  # Check if valid data is returned
            # Display the profile information
            st.header("Profile")
            st.metric("Symbol", data.get("Symbol", "N/A"))
            st.metric("Sector", data.get("Sector", "N/A"))
            st.metric("Industry", data.get("Industry", "N/A"))
            st.metric("Market Capitalization", data.get("MarketCapitalization", "N/A"))

            with st.expander("About Company"):
                st.write(data.get("Description", "No information available."))
        else:
            st.error("No data found for the given ticker. Please check the ticker symbol.")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching data: {e}")
