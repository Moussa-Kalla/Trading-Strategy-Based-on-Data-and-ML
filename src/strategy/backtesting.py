def backtest_strategy(df, take_profit_pct, stop_loss_pct):
    df['Take_Profit'] = None
    df['Stop_Loss'] = None
    df['Position_Closed'] = False
    df['PnL'] = 0

    current_position = None
    entry_price = None

    for i in range(len(df)):
        if current_position is None:
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
