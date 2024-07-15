import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import numpy as np
import time

# Initialize the Dash app
app = dash.Dash(__name__)

# Simulated initial data
actual_scores = np.array([15, 17, 33, 38, 40, 44, 49, 56, 64, 75, 80, 95, 101, 105, 113, 122, 131, 137, 153, 167])
predicted_scores_initial = actual_scores[:15]  # Initial predicted scores for the first 15 overs
predicted_scores_next = np.array([140, 145, 150, 155, 160])  # Predicted scores for the next 5 overs (simulated)

# Define app layout
app.layout = html.Div([
    html.H1("Cricket Score Prediction"),
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=3000,  # Update every 2 seconds
        n_intervals=0
    ),
])

# Callback to update graph dynamically
@app.callback(
    Output('live-update-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    # Simulate updating the predicted scores every 2 seconds
    current_predicted_scores = np.concatenate([predicted_scores_initial, predicted_scores_next[:n]])
    
    # Create figure object
    fig = go.Figure()
    
    # Add actual scores trace
    fig.add_trace(go.Scatter(x=np.arange(1, 21), y=actual_scores, mode='lines+markers', name='Actual Scores'))
    
    # Add updated predicted scores trace
    fig.add_trace(go.Scatter(x=np.arange(1, 21), y=current_predicted_scores, mode='lines+markers', name='Predicted Scores'))
    
    # Update layout
    fig.update_layout(
        title='Actual vs Predicted Scores',
        xaxis_title='Over Number',
        yaxis_title='Score',
        legend=dict(x=0, y=1, traceorder='normal'),
        autosize=False,
        width=800,
        height=500,
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
