import streamlit as st
import requests

# Initial UI
st.title("Stock Profile Viewer")
ticker = st.text_input("Enter Ticker (e.g., NFLX):", "NFLX").upper()
buttonClicked = st.button("Fetch Data")

# Callbacks
if buttonClicked:
    # Construct the request URL
    request_url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=assetProfile%2Cprice"

    try:
        # Send a GET request to the Yahoo Finance API
        response = requests.get(request_url, headers={"USER-AGENT": "Mozilla/5.0"})
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse the JSON response
        json_data = response.json()
        quote_summary = json_data.get("quoteSummary", {})
        result = quote_summary.get("result", None)

        if result and len(result) > 0:
            data = result[0]

            # Display the profile information
            st.header("Profile")
            st.metric("Sector", data["assetProfile"].get("sector", "N/A"))
            st.metric("Industry", data["assetProfile"].get("industry", "N/A"))
            st.metric("Website", data["assetProfile"].get("website", "N/A"))
            st.metric("Market Cap", data["price"]["marketCap"].get("fmt", "N/A"))

            with st.expander("About Company"):
                st.write(data["assetProfile"].get("longBusinessSummary", "No information available."))
        else:
            st.error("No data found for the given ticker. Please check the ticker symbol.")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching data: {e}")
    except KeyError as e:
        st.error(f"Unexpected data format. Missing key: {e}")
