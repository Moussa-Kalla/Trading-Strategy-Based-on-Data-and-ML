import streamlit as st
import pandas as pd
from fetch_data import get_historical_data
from strategy import strategy_1, backtest_strategy, performance_summary
from plotting import plot_cumulative_pnl, plot_pnl_distribution, plot_candlestick_chart

# Set page configuration
st.set_page_config(page_title="Stock Market Trading App", layout="wide")

# Sidebar options
st.sidebar.title("Options")
selected_option = st.sidebar.selectbox("Choose an option:", ["Chart Visualization", "Trade Table", "Strategy Editor & Execution"])

# Top navigation bar for strategy selection
strategy_options = ["Strategy 1", "Strategy 2", "Strategy 3"]
selected_strategy = st.selectbox("Select a trading strategy:", strategy_options)

# Main content
if selected_option == "Chart Visualization":
    st.title("Chart Visualization")
    symbol = st.text_input("Enter the symbol (e.g., BTC/USDT):", "BTC/USDT")
    timeframe = st.selectbox("Select the timeframe:", ["1m", "5m", "15m", "1h", "1d"])
    start_date = st.date_input("Start date:")
    end_date = st.date_input("End date:")

    if st.button("Fetch Data"):
        df = get_historical_data(symbol, timeframe, start_date.strftime('%Y-%m-%dT%H:%M:%SZ'), end_date.strftime('%Y-%m-%dT%H:%M:%SZ'))
        st.write("Historical Data", df)
        st.plotly_chart(plot_candlestick_chart(df))

elif selected_option == "Trade Table":
    st.title("Trade Table")
    st.write("Table with executed trades will be displayed here.")

elif selected_option == "Strategy Editor & Execution":
    st.title("Strategy Editor & Execution")
    code = st.text_area("Edit Trading Strategy:", """
def strategy_1(df, taille_bougie):
    df['variation'] = 100 * (df['close'] - df['open']) / df['open']
    df['Signal'] = 0
    df.loc[df['variation'] > taille_bougie, 'Signal'] = -1
    df.loc[df['variation'] < -taille_bougie, 'Signal'] = 1
    df['Signal'] = df['Signal'].shift(1)
    return df
""")

    if st.button("Run Strategy"):
        exec(code, globals())
        st.write("Strategy executed.")