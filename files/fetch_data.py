import ccxt
import pandas as pd
from datetime import datetime, timedelta

exchange = ccxt.binance()

def fetch_binance_data(symbol, timeframe, since, limit=1000):
    data = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def get_historical_data(symbol, timeframe, start_date, end_date):
    # Convert string dates to datetime objects
    start_time = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%SZ')
    end_time = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%SZ')
    all_data = []
    
    # Loop to fetch data in chunks to cover the full date range
    while start_time < end_time:
        since = int(start_time.timestamp() * 1000)
        df = fetch_binance_data(symbol, timeframe, since=since)
        if df.empty:
            break
        all_data.append(df)
        # Advance start_time based on the last retrieved timestamp
        start_time = df['timestamp'].iloc[-1] + timedelta(minutes=1)
    
    full_data = pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
    return full_data