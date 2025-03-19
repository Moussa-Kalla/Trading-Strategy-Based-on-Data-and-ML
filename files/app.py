import streamlit as st
import pandas as pd
from fetch_data import get_historical_data
from strategy import strategy_1, backtest_strategy, performance_summary
from plotting import plot_candlestick_chart, plot_cumulative_pnl, plot_pnl_distribution

# Set page configuration
st.set_page_config(page_title="Stock Market Trading App", layout="wide")

# Sidebar options for navigation
st.sidebar.title("Options")
selected_option = st.sidebar.selectbox("Choose an option:", ["Chart Visualization", "Trade Table", "Strategy Editor & Execution"])

# Top navigation bar for strategy selection (simulated using a selectbox)
strategy_options = ["Strategy 1", "Strategy 2", "Strategy 3"]
selected_strategy = st.selectbox("Select a trading strategy:", strategy_options)

# Main content rendering based on the selected sidebar option
if selected_option == "Chart Visualization":
    st.title("Chart Visualization")
    symbol = st.text_input("Enter the symbol (e.g., BTC/USDT):", "BTC/USDT")
    timeframe = st.selectbox("Select the timeframe:", ["1m", "5m", "15m", "1h", "1d"])
    start_date = st.date_input("Start date:")
    end_date = st.date_input("End date:")

    if st.button("Fetch Data"):
        # Convert the start and end dates to the required format
        df = get_historical_data(
            symbol, 
            timeframe, 
            start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        )
        st.write("Historical Data", df)
        # Optionally, you might run your trading strategy here to generate trade signals
        df = strategy_1(df, 0.5)
        trades = []  # Populate this list with executed trade details if available.
        st.plotly_chart(plot_candlestick_chart(df, trades))

elif selected_option == "Trade Table":
    st.title("Trade Table")
    # In this example, we suppose that the executed trades are saved in a DataFrame.
    # Note: This table excludes any preliminary data table; it only includes the executed trade details.
    trades_df = pd.DataFrame({
        "Time": ["2025-03-12 21:40:00", "2025-03-12 21:45:00"],
        "Type": ["Buy", "Sell"],
        "Price": [45000, 45500],
        "Quantity": [0.1, 0.1]
    })
    st.write("Executed Trades", trades_df)

elif selected_option == "Strategy Editor & Execution":
    st.title("Strategy Editor & Execution")
    code = st.text_area("Edit Trading Strategy:", """
def strategy_1(df, taille_bougie):
    df['variation'] = 100 * (df['close'] - df['open']) / df['open']
    df['Signal'] = 0
    df.loc[df['variation'] > taille_bougie, 'Signal'] = -1
    df.loc[df['variation'] < -taille_bougie, 'Signal'] = 1
    # Shift the signal to avoid lookahead bias
    df['Signal'] = df['Signal'].shift(1)
    return df
    """, height=250)

    if st.button("Run Strategy"):
        # Use exec to update the strategy code on-the-fly.
        # Warning: Using exec can be risky. Ensure that only trusted code is executed.
        exec(code, globals())
        st.write("Strategy executed.")
        # Example: re-run the strategy on pre-fetched data and show a performance summary.
        symbol = st.text_input("Enter the symbol (e.g., BTC/USDT):", "BTC/USDT", key="strategy_symbol")
        timeframe = st.selectbox("Select the timeframe:", ["1m", "5m", "15m", "1h", "1d"], key="strategy_timeframe")
        start_date = st.date_input("Start date for strategy:", key="strategy_start")
        end_date = st.date_input("End date for strategy:", key="strategy_end")
        if st.button("Fetch & Test Strategy"):
            df = get_historical_data(
                symbol, 
                timeframe, 
                start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
            )
            df = strategy_1(df, 0.5)
            test_df = backtest_strategy(df.copy(), take_profit_pct=0.02, stop_loss_pct=0.01)
            summary = performance_summary(test_df)
            st.write("Strategy Performance Summary:", summary)
            st.plotly_chart(plot_cumulative_pnl(test_df))
            st.plotly_chart(plot_pnl_distribution(test_df))