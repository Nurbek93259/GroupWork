import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Set page configuration (must be first Streamlit command)
st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")

# Minimalist black theme styling
st.markdown("""
    <style>
    body {
        background-color: #1c1c1c;
        color: #e0e0e0;
    }
    .css-1v3fvcr {
        background-color: #1c1c1c !important;
    }
    .stButton>button {
        background-color: #00BFFF !important;
        color: white !important;
    }
    .css-2trqyj {
        color: white !important;
    }
    h1, h2, h3, h4, h5 {
        color: #00BFFF;
    }
    </style>
""", unsafe_allow_html=True)

# Continue with the rest of your code
