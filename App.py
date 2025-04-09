import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title('Phân tích kỹ thuật BTC/USD')

btc = yf.Ticker("BTC-USD")
hist = btc.history(period="1mo", interval="1h")

hist['MA20'] = hist['Close'].rolling(window=20).mean()
hist['MA50'] = hist['Close'].rolling(window=50).mean()
hist['RSI'] = 100 - (100 / (1 + hist['Close'].pct_change().rolling(window=14).mean() / hist['Close'].pct_change().rolling(window=14).std()))
hist['MACD'] = hist['Close'].ewm(span=12, adjust=False).mean() - hist['Close'].ewm(span=26, adjust=False).mean()

st.subheader('Biểu đồ giá và các chỉ báo kỹ thuật')
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(hist.index, hist['Close'], label='Giá đóng cửa', color='blue')
ax.plot(hist.index, hist['MA20'], label='MA20', color='red')
ax.plot(hist.index, hist['MA50'], label='MA50', color='green')
ax.set_xlabel('Ngày')
ax.set_ylabel('Giá (USD)')
ax.legend()
st.pyplot(fig)

st.subheader('Dữ liệu chi tiết')
st.dataframe(hist[['Close', 'MA20', 'MA50', 'RSI', 'MACD']].tail(20))

st.subheader('Gợi ý mua/bán')
if hist['MA20'].iloc[-1] > hist['MA50'].iloc[-1] and hist['RSI'].iloc[-1] < 70:
    st.write('**Tín hiệu MUA**: MA20 cắt lên MA50 và RSI < 70')
elif hist['MA20'].iloc[-1] < hist['MA50'].iloc[-1] and hist['RSI'].iloc[-1] > 30:
    st.write('**Tín hiệu BÁN**: MA20 cắt xuống MA50 và RSI > 30')
else:
    st.write('**Chưa có tín hiệu rõ ràng**')
