import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from pnl_calculator import calculate_pnl, performance_summary
from src.visualization.plot_results import plot_cumulative_pnl, plot_pnl_distribution

# Charger les données
df = pd.read_csv('data/processed/historical_data.csv')

# Calculer les PnL et la stratégie
df = calculate_pnl(df)
summary = performance_summary(df)

# Initialiser l'application Dash
app = dash.Dash(__name__)

# Layout de l'application
app.layout = html.Div([
    html.H1("Application de Trading - Analyse des Performances", style={'textAlign': 'center'}),
    
    # Résumé des performances
    html.Div([
        html.H3("Résumé des Performances"),
        html.P(f"Total des Profits : {summary['Total Profit']:.2f} $"),
        html.P(f"Nombre de Trades Gagnants : {summary['Winning Trades']}"),
        html.P(f"Nombre de Trades Perdants : {summary['Losing Trades']}"),
        html.P(f"Nombre de Trades Neutres : {summary['Neutral Trades']}"),
        html.P(f"Taux de Succès : {summary['Win Rate (%)']:.2f} %"),
        html.P(f"Nombre Total de Trades : {summary['Total Trades']}"),
    ], style={'padding': '20px', 'backgroundColor': '#f9f9f9', 'marginBottom': '20px'}),
    
    # Graphique des profits cumulés
    html.Div([
        html.H3("Évolution des Profits Cumulés"),
        dcc.Graph(figure=px.line(df, x='timestamp', y='Cumulative_PnL', 
                                 title="Profits Cumulés", labels={'timestamp': 'Temps', 'Cumulative_PnL': 'Profits ($)'})),
    ], style={'marginBottom': '20px'}),
    
    # Histogramme des profits et pertes
    html.Div([
        html.H3("Répartition des Profits et Pertes"),
        dcc.Graph(figure=px.histogram(df, x='PnL', nbins=50, 
                                      title="Répartition des Profits et Pertes", 
                                      labels={'PnL': 'Profit ou Perte ($)', 'count': 'Fréquence'})),
    ])
])

# Lancer le serveur
if __name__ == '__main__':
    app.run_server(debug=True)
