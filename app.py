import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("📈 Real-Time Stock Market Dashboard")

st.sidebar.header("Stock Settings")
symbol = st.sidebar.text_input("Stock Symbol", value="AAPL").upper()
period = st.sidebar.selectbox("Time Period", ["1mo", "3mo", "6mo", "1y"])

if st.sidebar.button("Update Dashboard"):
    with st.spinner("Fetching data..."):
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if hist.empty:
            st.error(f"No data found for symbol '{symbol}'. Try AAPL, TSLA, MSFT.")
        else:
            current_price = hist['Close'].iloc[-1]
            st.metric(f"{symbol} Current Price", f"${current_price:.2f}")
            
            fig = go.Figure(data=[go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close']
            )])
            fig.update_layout(title=f"{symbol} Price Chart", xaxis_title="Date", yaxis_title="Price (USD)")
            st.plotly_chart(fig, use_container_width=True)
            
            if len(hist) >= 20:
                hist['SMA20'] = hist['Close'].rolling(window=20).mean()
                st.subheader("Closing Price vs 20-Day SMA")
                st.line_chart(hist[['Close', 'SMA20']])
            else:
                st.info("Not enough data for 20-day moving average.")