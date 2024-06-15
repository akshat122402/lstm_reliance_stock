# Reliance Stock Prediction Using LSTM

Welcome to the LSTM Reliance Stock Prediction project! This project uses Long Short-Term Memory (LSTM) networks, a type of recurrent neural network (RNN), to predict Reliance stock prices based on historical data.

## Project Overview
This project provides a web interface to predict Reliance stock prices, using historical stock data fetched from Alpha Vantage to train the model. The application consists of:
- **Data Fetching**: `fetch_data.py` to fetch and preprocess stock data.
- **Model Training**: `model.py` to train the LSTM model.
- **API Endpoints**: `app.py` to set up API Endpoints using Flask.
- **Web Application**: `streamlit_app.py` to serve the prediction interface via Streamlit.

## Features
- Automated data fetching and model training.
- User-friendly web interface for stock prediction.
- Dockerized application for easy deployment.

## Getting Started
### Running the Application Locally
#### 1. Clone the Repository
```sh
git clone https://github.com/akshat122402/lstm_reliance_stock.git
cd lstm_reliance_stock
```
#### 2. Install Python 3.9
If not already installed locally, install python 3.9 from [here](https://www.python.org/downloads/release/python-390/)

#### 3. Set up a Virtual Environment
```
python3.9 -m venv env
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
#### 4. Install Dependencies
Install the required Python packages using pip:
```
pip install -r requirements.txt
```
#### 5. Set up Alpha Vantage API Key
Create a .env file and set AV_API_KEY=<YOUR_API_KEY> in the file.
You can access your free API key [here](https://www.alphavantage.co/support/#api-key).

#### 6. Train on Latest Data
You can train on latest stock data by running 
1. ```python fetch_data.py```
2. ```python model.py```

#### 7. Run the App
Execute the run_app.py script to start the application:
```
python run_app.py
```
The application will be available at http://localhost:8501/.

## Usage
#### Historical Data
Interact with past data of Reliance Stock available in a table and an interactive graph.
#### Predict Future Stock prices
Select number of days in future to predict the closed price of Reliance Stock and click "Predict" button.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

---

### Links
- [Live Demo](http://68.183.244.97:8501/) 

Please feel free to open issues or pull requests on our [GitHub repository](https://github.com/akshat122402/lstm_reliance_stock).
