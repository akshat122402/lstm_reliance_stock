import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import sqlite3
import joblib
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = "0"

gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

print(f"GPUs: {gpus}")

def load_data():
    try:
        with sqlite3.connect('stocks.db') as conn:
            data = pd.read_sql('SELECT * FROM reliance', conn)
        return data
    except Exception as e:
        print(f"Failed to load data: {e}")
        return None

def preprocess_data(data, prediction_days=1000):
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    
    data = data[['close']]  
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    
    X, y = [], []
    for x in range(prediction_days, len(scaled_data)):
        X.append(scaled_data[x - prediction_days:x, 0])
        y.append(scaled_data[x, 0])
    
    X = np.array(X).reshape((len(X), prediction_days, 1))
    y = np.array(y)
    
    return X, y, scaler, data.index[prediction_days:]

def build_model(input_shape):
    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(units=50),
        Dropout(0.2),
        Dense(units=1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def save_predictions(future_predictions, future_dates):
    try:
        future_predictions_df = pd.DataFrame({
            'date': future_dates, 
            'predicted_close': future_predictions.flatten()
        })
        with sqlite3.connect('stocks.db') as conn:
            future_predictions_df.to_sql('predictions', conn, if_exists='replace', index=False)
    except Exception as e:
        print(f"Failed to save predictions: {e}")

def train_model():
    try:
        print("Loading data...")
        data = load_data()
        if data is None:
            return  

        print("Preprocessing data...")
        X, y, scaler, valid_dates = preprocess_data(data, prediction_days=1000)
        
        print("Building model...")
        model = build_model((X.shape[1], 1))
        # early_stopping = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)

        print("Training model...")
        model.fit(X, y, epochs=150, batch_size=128)

        print("Saving model and scaler...")
        model.save('reliance_model.h5')
        joblib.dump(scaler, 'scaler.pkl')

        future_predictions = []
        last_1000_days = X[-1,:].reshape((1, X.shape[1], 1)) 

        for _ in range(200):
            prediction = model.predict(last_1000_days)
            future_predictions.append(prediction[0][0])
            prediction = np.expand_dims(prediction, axis=0)
            last_1000_days = np.concatenate([last_1000_days[:, 1:, :], prediction], axis=1)

        future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))
        future_dates = pd.date_range(start=valid_dates[-1], periods=201)[1:]

        print("Saving predictions...")
        save_predictions(future_predictions, future_dates)

        print("Model training completed.")
        return model, scaler
    except Exception as e:
        print(f"Model training failed: {e}")

if __name__ == "__main__":
    train_model()