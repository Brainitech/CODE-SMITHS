import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt

# Initialize the Dash app
app = dash.Dash(__name__)

# Function to fetch stock data
def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# Function to create a plot
def create_plot(stock_data):
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data['Close'], label='Closing Price')
    plt.title('Stock Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend()
    return plt

# Layout of the app
app.layout = html.Div([
    html.H1("Stock Price Visualization"),
    
    html.Label("Enter Stock Code:"),
    dcc.Input(id='stock-input', type='text', value='MSFT'),

    html.Label("Select Date Range:"),
    dcc.DatePickerRange(
        id='date-picker',
        start_date=dt.date(2022, 1, 1),
        end_date=dt.date.today(),
        display_format='YYYY-MM-DD'
    ),

    html.Button('PLOT GRAPH', id='plot-button', n_clicks=0),

    dcc.Graph(id='stock-plot'),

])

# Callback to update the plot based on user input
@app.callback(
    Output('stock-plot', 'figure'),
    [Input('plot-button', 'n_clicks')],
    [State('stock-input', 'value'),
     State('date-picker', 'start_date'),
     State('date-picker', 'end_date')]
)
def update_plot(n_clicks, selected_stock, start_date, end_date):
    if n_clicks > 0:
        stock_data = get_stock_data(selected_stock, start_date, end_date)
        plt = create_plot(stock_data)

        return {'data': [{'x': stock_data.index, 'y': stock_data['Close'], 'type': 'line', 'name': 'Closing Price'}],
                'layout': {'title': f'{selected_stock} Stock Price Over Time',
                           'xaxis': {'title': 'Date'},
                           'yaxis': {'title': 'Closing Price'}}}
    else:
        # If the button has not been clicked, return an empty graph
        return {'data': [], 'layout': {}}

# Start app
if __name__ == '__main__':
    app.run_server(debug=True)