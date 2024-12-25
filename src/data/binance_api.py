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
    start_time = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%SZ')
    end_time = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%SZ')
    delta = timedelta(minutes=1000)
    all_data = []

    while start_time < end_time:
        since = int(start_time.timestamp() * 1000)
        df = fetch_binance_data(symbol, timeframe, since=since)
        if df.empty:
            break
        all_data.append(df)
        start_time = df['timestamp'].iloc[-1] + timedelta(minutes=1)

    full_data = pd.concat(all_data, ignore_index=True)
    return full_data

symbol = "BTC/USDT"
timeframe = "30m"  
start_date = "2010-11-30T00:00:00Z"  # Format complet avec année, mois, jour, heure et minute
end_date = "2024-11-30T23:59:59Z"  # Format complet avec année, 

df = get_historical_data(symbol, timeframe, start_date, end_date)
df.to_csv('data/processed/historical_data.csv')