import pandas as pd

def strategy_1(df, taille_bougie):
    # Calculate percentage variation for each candlestick
    df['variation'] = 100 * (df['close'] - df['open']) / df['open']
    df['Signal'] = 0
    # Generate signals: 1 for buy and -1 for sell based on variation thresholds
    df.loc[df['variation'] > taille_bougie, 'Signal'] = -1
    df.loc[df['variation'] < -taille_bougie, 'Signal'] = 1
    # Shift signal to avoid lookahead bias
    df['Signal'] = df['Signal'].shift(1)
    return df

def backtest_strategy(df, take_profit_pct, stop_loss_pct):
    # Initialize backtesting columns
    df['Take_Profit'] = None
    df['Stop_Loss'] = None
    df['Position_Closed'] = False
    df['PnL'] = 0

    current_position = None
    entry_price = None

    for i in range(len(df)):
        if current_position is None:
            # Enter a position based on the generated signal
            if df.loc[i, 'Signal'] == 1:
                current_position = 'long'
                entry_price = df.loc[i, 'close']
                df.loc[i, 'Take_Profit'] = entry_price * (1 + take_profit_pct)
                df.loc[i, 'Stop_Loss'] = entry_price * (1 - stop_loss_pct)
            elif df.loc[i, 'Signal'] == -1:
                current_position = 'short'
                entry_price = df.loc[i, 'close']
                df.loc[i, 'Take_Profit'] = entry_price * (1 - take_profit_pct)
                df.loc[i, 'Stop_Loss'] = entry_price * (1 + stop_loss_pct)
        else:
            # Check conditions to close the current open position
            if current_position == 'long' and (
                (df.loc[i, 'high'] >= df.loc[i-1, 'Take_Profit']) or 
                (df.loc[i, 'low'] <= df.loc[i-1, 'Stop_Loss'])
            ):
                df.loc[i, 'PnL'] = df.loc[i, 'close'] - entry_price
                current_position = None
            elif current_position == 'short' and (
                (df.loc[i, 'low'] <= df.loc[i-1, 'Take_Profit']) or 
                (df.loc[i, 'high'] >= df.loc[i-1, 'Stop_Loss'])
            ):
                df.loc[i, 'PnL'] = entry_price - df.loc[i, 'close']
                current_position = None
                
    df.dropna(subset=['low', 'Take_Profit'], inplace=True)
    df['Cumulative_PnL'] = df['PnL'].cumsum()
    return df

def performance_summary(df):
    # Generate basic performance statistics for the strategy
    total_profit = df['PnL'].sum()
    winning_trades = df[df['PnL'] > 0]['PnL'].count()
    losing_trades = df[df['PnL'] < 0]['PnL'].count()
    neutral_trades = df[df['PnL'] == 0]['PnL'].count()
    total_trades = winning_trades + losing_trades
    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0

    summary = {
        "Total Profit": total_profit,
        "Winning Trades": winning_trades,
        "Losing Trades": losing_trades,
        "Neutral Trades": neutral_trades,
        "Win Rate (%)": win_rate,
        "Total Trades": total_trades
    }

    return summary