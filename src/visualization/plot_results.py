import plotly.express as px

def plot_cumulative_pnl(df):
    fig = px.line(df, x='timestamp', y='Cumulative_PnL', title="Évolution des Profits Cumulés")
    fig.update_layout(xaxis_title="Temps", yaxis_title="Profits ($)")
    return fig.show()

def plot_pnl_distribution(df):
    fig = px.histogram(df, x='PnL', nbins=50, title="Répartition des Profits et Pertes")
    fig.update_layout(xaxis_title="Profit ou Perte ($)", yaxis_title="Fréquence")
    return fig.show()
