import subprocess
from flask import Flask, jsonify
import sqlite3
import pandas as pd
import os

app = Flask(__name__)

def connect_db():
    return sqlite3.connect('stocks.db')

@app.route('/data', methods=['GET'])
def get_data():
    try:
        with connect_db() as conn:
            data = pd.read_sql('SELECT * FROM reliance', conn)
        return data.to_json(orient='records')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/train', methods=['GET'])
def train():
    try:
        print("Starting model training...")
        
        result = subprocess.run(
            [os.sys.executable, "model.py"],  
            capture_output=True,
            text=True,
            env=os.environ.copy()
        )

        if result.returncode != 0:
            raise Exception(result.stderr)
        
        print("Training finished successfully.")
        return jsonify({"message": "Training Successful"})
    except Exception as e:
        print(f"Training error: {e}")
        return jsonify({"error": str(e), "output": result.stderr}), 500

@app.route('/predict', methods=['GET'])
def predict():
    try:
        with connect_db() as conn:
            predictions = pd.read_sql('SELECT * FROM predictions', conn)
        return predictions.to_json(orient='records')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)