import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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

# Layout of the app
app.layout = html.Div([
    html.H1("Stock Price Visualization"),
    
    html.Label("Enter Stock Ticker Symbol:"),
    dcc.Input(id='stock-input', type='text', value=''),

    html.Label("Select Date Range:"),
    dcc.DatePickerRange(
        id='date-picker',
        start_date=dt.date(2022, 1, 1),
        end_date=dt.date.today(),
        display_format='YYYY-MM-DD'
    ),

    dcc.Graph(id='stock-plot'),

])

# Callback to update the plot based on user input
@app.callback(
    Output('stock-plot', 'figure'),
    [Input('stock-input', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_plot(selected_stock, start_date, end_date):
    stock_data = get_stock_data(selected_stock, start_date, end_date)
    plot = create_plot(stock_data)

    return {'data': [{'x': stock_data.index, 'y': stock_data['Close'], 'type': 'line', 'name': 'Closing Price'}],
            'layout': {'title': f'{selected_stock} Stock Price Over Time',
                       'xaxis': {'title': 'Date'},
                       'yaxis': {'title': 'Closing Price'}}}

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)