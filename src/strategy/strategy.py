import pandas as pd

def strategy_1(df, taille_bougie):
    df['variation'] = 100 * (df['close'] - df['open']) / df['open']
    df['Signal'] = 0
    df.loc[df['variation'] > taille_bougie, 'Signal'] = -1
    df.loc[df['variation'] < -taille_bougie, 'Signal'] = 1
    df['Signal'] = df['Signal'].shift(1)
    return df
