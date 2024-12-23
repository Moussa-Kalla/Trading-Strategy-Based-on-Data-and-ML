import pandas as pd

def calculate_pnl(df):
    """
    Calcule les profits et pertes (PnL) pour chaque trade et le PnL cumulé.
    """
    df['PnL'] = 0  # Profits et pertes par trade
    df['Cumulative_PnL'] = 0  # Profits cumulés

    current_position = None
    entry_price = None

    for i in range(len(df)):
        if current_position is None:  # Pas de position ouverte
            if df.loc[i, 'Signal'] == 1:  # Signal d'achat
                current_position = 'long'
                entry_price = df.loc[i, 'close']
            elif df.loc[i, 'Signal'] == -1:  # Signal de vente
                current_position = 'short'
                entry_price = df.loc[i, 'close']
        else:  # Une position est ouverte
            if df.loc[i, 'Position_Closed']:  # La position est fermée
                if current_position == 'long':  # Achat fermé
                    df.loc[i, 'PnL'] = df.loc[i, 'close'] - entry_price
                elif current_position == 'short':  # Vente fermée
                    df.loc[i, 'PnL'] = entry_price - df.loc[i, 'close']
                current_position = None
                entry_price = None

    # Calcul des profits cumulés
    df['Cumulative_PnL'] = df['PnL'].cumsum()
    return df

def performance_summary(df):
    """
    Génère un résumé des performances de la stratégie.
    """
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
