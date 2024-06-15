import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from io import StringIO

def footer():
    footer_html = """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #0e1016;
        text-align: center;
        padding: 15px 0;
        font-size: 18px;
    }
    .icon-container {
            display: inline-flex;
            gap: 40px;
            justify-content: center;
    }
    </style>
    <div class="footer">
        <p>Made with ❤️ by Akshat Gupta</p>
        <div class="icon-container">
            <a href="https://github.com/akshat122402" target="_blank">
                <img src="https://img.icons8.com/glyph-neue/64/FFFFFF/github.png" alt="GitHub"/ height=30 width=30>
            </a>
            <a href="https://www.kaggle.com/akshatgupta7" target="_blank">
                <img src="https://img.icons8.com/windows/32/FFFFFF/kaggle.png" alt="Kaggle"/ height=30 width=30>
            </a>
            <a href="https://www.linkedin.com/in/akshat-gupta-a82923227/" target="_blank">
                <img src="https://img.icons8.com/ios-filled/50/FFFFFF/linkedin.png" alt="LinkedIn"/ height=30 width=30>
            </a>
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

st.title("Reliance Stock Prediction using LSTM📈🧑‍💻")
st.caption("Predict future stock prices of Reliance Industries using historical data and LSTM model.")

def fetch_data(api_url):
    response = requests.get(api_url)
    response.raise_for_status()
    return pd.read_json(StringIO(response.text))

def plot_historical_data(data):
    fig = px.line(data, x='date', y='close', title='Closed Stock Prices')
    st.plotly_chart(fig)

def plot_predictions(predictions):
    fig = px.line(predictions, x='date', y='predicted_close', title='Future Reliance Stock Price Predictions')
    st.plotly_chart(fig)

try:
    data = fetch_data("http://127.0.0.1:8501/data")
    
    st.header("Historical Stock Data")
    st.dataframe(data)
    plot_historical_data(data)

    st.header("Predict Future Stock Prices")
    days_to_predict = st.slider('Select number of future days to predict', 1, 200, 1)

    if st.button('Predict'):
        try:
            predictions = fetch_data("http://127.0.0.1:8501/predict")

            future_predictions = predictions.head(days_to_predict)

            st.header(f"Predicted Data for Next {days_to_predict} Days")
            st.dataframe(future_predictions)
            plot_predictions(future_predictions)

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

except requests.exceptions.RequestException as e:
    st.error(f"Failed to fetch historical data: {e}")
st.caption("Note: The predictions are based on historical data and may not be accurate.")
st.markdown("""<br><br><p>Check out the <a href="https://github.com/akshat122402/streamlit-reliance-stock-prediction" target="_blank" style="color: white; text-decoration: underline;">GitHub repository</a> for this project.</p>""", unsafe_allow_html=True)
footer()