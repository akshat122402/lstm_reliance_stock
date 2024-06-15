import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()

def fetch_data(symbol, db_name='stocks.db'):
    api_key = os.getenv('AV_API_KEY')
    if api_key is None:
        raise ValueError("API_KEY not found in environment variables.")
    
    try:
        ts = TimeSeries(key=api_key, output_format='pandas')
        data, _ = ts.get_daily(symbol=symbol, outputsize='full')
        data.reset_index(inplace=True)
        data.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        data = data.iloc[::-1]
        data['date'] = pd.to_datetime(data['date'])  
        
        with sqlite3.connect(db_name) as conn:
            data.to_sql('reliance', conn, if_exists='replace', index=False)
    except Exception as e:
        print(f"Data fetching failed: {e}")

if __name__ == "__main__":
    SYMBOL = 'RELIANCE.BSE'
    fetch_data(SYMBOL)