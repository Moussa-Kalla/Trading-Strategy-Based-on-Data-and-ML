import plotly.graph_objs as go
import plotly.express as px

def plot_candlestick_chart(df, trades=None):
    # Create a basic candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])

    # If trades data is available, overlay buy/sell markers
    if trades is not None:
        for trade in trades:
            if trade['type'] == 'buy':
                marker = dict(color='green', symbol='triangle-up', size=10)
            elif trade['type'] == 'sell':
                marker = dict(color='red', symbol='triangle-down', size=10)
            fig.add_trace(go.Scatter(
                x=[trade['timestamp']],
                y=[trade['price']],
                mode='markers',
                marker=marker
            ))

    fig.update_layout(
        title="Candlestick Chart with Trade Markers",
        xaxis_title="Time",
        yaxis_title="Price"
    )
    return fig

def plot_cumulative_pnl(df):
    # Plot cumulative profit and loss over time
    fig = px.line(df, x='timestamp', y='Cumulative_PnL', title="Cumulative PnL Over Time")
    fig.update_layout(xaxis_title="Time", yaxis_title="PnL ($)")
    return fig

def plot_pnl_distribution(df):
    # Plot histogram of PnL distribution
    fig = px.histogram(df, x='PnL', nbins=50, title="PnL Distribution")
    fig.update_layout(xaxis_title="PnL ($)", yaxis_title="Frequency")
    return fig