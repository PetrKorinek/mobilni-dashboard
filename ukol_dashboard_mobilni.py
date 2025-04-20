
import streamlit as st
import pandas as pd
import yfinance as yf
import requests
from ta.momentum import RSIIndicator

st.set_page_config(page_title="📱 Mobilní obchodní přehled", layout="centered")
st.title("📱 Akciový přehled – mobilní verze")

FINNHUB_API_KEY = "d02ijr1r01qi6jgh9sugd02ijr1r01qi6jgh9sv0"

markets = {
    "USA": ["AAPL", "MSFT", "TSLA", "NVDA", "META", "GOOGL"],
    "Evropa": ["SAP.DE", "ADS.DE", "AIR.PA", "MC.PA"],
    "Česko": ["CEZ.PR", "KOMB.PR", "MONET.PR", "ERSTE.VI"],
    "ETF": ["SPY", "QQQ", "VTI", "EEM", "XLF"]
}

trh = st.selectbox("🌍 Vyber trh", list(markets.keys()))
tickery = markets[trh]

st.markdown("🧠 Zjednodušený přehled signálů (RSI < 50 nebo pokles > 10 %)")

for ticker in tickery:
    try:
        data = yf.download(ticker, period="6mo", group_by="ticker", progress=False)
        close_series = data[(ticker, "Close")]
        if close_series.empty or len(close_series) < 50:
            continue
        rsi = RSIIndicator(close=close_series).rsi()
        rsi_val = round(rsi.iloc[-1], 2)
        max_price = float(close_series.max())
        close = float(close_series.iloc[-1])
        pokles = round(((close - max_price) / max_price) * 100, 2)

        url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_API_KEY}"
        res = requests.get(url).json()
        cena = res.get("c", "❓")

        if rsi_val < 50 or pokles < -10:
            st.markdown(f"### {ticker}")
            st.write(f"📉 RSI: {rsi_val}   |   🔻 Pokles: {pokles}%")
            st.write(f"💡 Live cena: {cena}")
            with st.expander("📊 Detail (graf a více)", expanded=False):
                st.line_chart(close_series)
    except Exception as e:
        st.warning(f"{ticker}: chyba – {e}")
