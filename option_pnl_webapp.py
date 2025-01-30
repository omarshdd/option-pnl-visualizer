import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Option P&L Visualizer"),
    html.Label("Underlying Price at Purchase:"),
    dcc.Input(id='underlying-price', type='number', value=100),
    
    html.Label("Option Premium:"),
    dcc.Input(id='option-premium', type='number', value=5),
    
    html.Label("Delta at Purchase:"),
    dcc.Input(id='delta-purchase', type='number', value=0.5),
    
    html.Label("Adjust Hypothetical Price (% Change):"),
    dcc.Slider(id='hypothetical-slider', min=-20, max=20, step=1, value=0,
               marks={i: f"{i}%" for i in range(-20, 21, 5)}),
    
    dcc.Graph(id='pnl-graph'),
])

# Callback to update P&L graph
@app.callback(
    Output('pnl-graph', 'figure'),
    [Input('underlying-price', 'value'),
     Input('option-premium', 'value'),
     Input('delta-purchase', 'value'),
     Input('hypothetical-slider', 'value')]
)
def update_graph(underlying, premium, delta, hypo_change):
    price_range = np.linspace(underlying * 0.8, underlying * 1.2, 50)
    estimated_pnl = (price_range - underlying) * delta * 100 - premium * 100
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=price_range, y=estimated_pnl, mode='lines',
                             name='Estimated P&L'))
    
    fig.update_layout(title="P&L vs. Hypothetical Stock Price",
                      xaxis_title="Stock Price",
                      yaxis_title="Estimated P&L")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
