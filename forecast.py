from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from utils import download_data
from models.arima_garch import fit_arima_garch, forecast_arima_garch
from models.prophet_model import fit_prophet, forecast_prophet
from models.lstm import load_lstm, fit_lstm, forecast_lstm
from app_instance import app

layout = dbc.Container([
    html.H1("Forecast Stock Prices", className='fade-in-element', style={'text-align': 'center', 'margin-top': '40px', 'font-family': 'Prata'}),
    dbc.Row([
        dbc.Col([
            html.H4('Select the Stock to Predict', className='fade-in-element', style={'margin': '20px 0', 'text-align': 'center'}),
            dcc.Dropdown(
                id='index-dropdown',
                options=[
                    {'label': 'NVIDIA', 'value': 'NVDA'},
                    {'label': 'Apple', 'value': 'AAPL'},
                    {'label': 'Google', 'value': 'GOOGL'},
                    {'label': 'Amazon', 'value': 'AMZN'}
                ],
                value='NVDA',
                className='fade-in-element',
                style={'margin-bottom': '20px'}
            ),
        ], width=4),
        dbc.Col([
            html.H4('Select the Forecast Period', className='fade-in-element', style={'margin': '20px 0', 'text-align': 'center'}),
            dcc.Dropdown(
                id='forecast-period-dropdown',
                options=[
                    {'label': '1 Month', 'value': 30},
                    {'label': '3 Months', 'value': 90},
                    {'label': '6 Months', 'value': 180},
                    {'label': '9 Months', 'value': 270},
                    {'label': '1 Year', 'value': 365}
                ],
                value=90,
                className='fade-in-element',
                style={'margin-bottom': '20px'}
            ),
        ], width=4),
        dbc.Col([
            html.H4('Desired Percentage of Earnings (%)', className='fade-in-element', style={'margin': '20px 0', 'text-align': 'center'}),
            dcc.Input(
                id='earnings-percentage-input',
                type='number',
                value=10,
                className='fade-in-element custom-input',
                style={'margin-bottom': '20px', 'width': '100%'}
            ),
        ], width=4)
    ], style={'margin-bottom': '20px'}),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.RadioItems(
                    id='model-selection',
                    options=[
                        {'label': 'ARIMA-GARCH', 'value': 'ARIMA-GARCH'},
                        {'label': 'Prophet', 'value': 'Prophet'},
                        {'label': 'LSTM', 'value': 'LSTM'}
                    ],
                    value='ARIMA-GARCH',
                    labelStyle={'display': 'inline-block'},
                    className='radio-group fade-in-element',
                    style={'font-family': 'Hanken Grotesk'}
                ),
            ], style={'text-align': 'center'}),
            dcc.Loading(
                id="loading-graph",
                type="default",
                children=[
                    dcc.Graph(id='price-graph', className='fade-in-element', style={'margin-top': '30px', 'margin-bottom': '30px', 'height': '500px', 'backgroundColor': 'white', 'border': '1px solid #CCCCCC', 'border-radius': '10px', 'padding': '10px 0px 510px 0px'}),
                    dcc.Graph(id='forecast-graph', className='fade-in-element', style={'margin-top': '30px', 'height': '500px', 'backgroundColor': 'white', 'border': '1px solid #CCCCCC', 'border-radius': '10px', 'padding': '10px 0px 510px 0px'}),
                ]
            ),
            html.Div(id='recommendations-container', className='fade-in-element', style={'margin-top': '20px', 'text-align': 'center', 'font-family': 'Hanken Grotesk'})
        ])
    ], style={'margin-bottom': '20px'}),
], fluid=True, className="container")

@app.callback(
    Output('price-graph', 'figure'),
    [Input('index-dropdown', 'value')]
)
def update_price_graph(ticker):
    data = download_data(ticker)

    moving_average_100 = data['Close'].rolling(window=100).mean()
    moving_average_200 = data['Close'].rolling(window=200).mean()
    last_price = data['Close'].iloc[-1]

    min_price = max(0, data['Close'].min() * 0.9)
    max_price = data['Close'].max() * 1.1

    price_fig = {
        'data': [
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Candlesticks'
            ),
            go.Scatter(
                x=data.index,
                y=moving_average_100,
                mode='lines',
                name='MA 100',
                line=dict(color='blue')
            ),
            go.Scatter(
                x=data.index, 
                y=moving_average_200, 
                mode='lines', 
                name='MA 200',
                line=dict(color='red')
            ),
            go.Scatter(
                x=[data.index[-1]],
                y=[last_price],
                mode='markers+text',
                text=[f'Last {last_price:.2f}'],
                textposition='top right',
                name='Last Price',
                marker=dict(color='green', size=12)
            )
        ],
        'layout': {
            'title': {
                'text': f'Historic Price for {ticker}',
                'font': {'family': 'Prata', 'color': '#050A30'}
            },
            'yaxis': {
                'title': 'Close Price',
                'titlefont': {'family': 'Hanken Grotesk', 'color': '#050A30'},
                'tickfont': {'family': 'Hanken Grotesk'},
                'showgrid': True,
                'gridcolor': 'LightGray',
                'gridwidth': 0.5,
                'range': [min_price, max_price],
                'zeroline': False
            },
            'xaxis': {
                'title': 'Date',
                'type': 'date',
                'tickformat': '%b %Y',
                'tickmode': 'auto',
                'nticks': 20,
                'tickformatstops': [
                    {'dtickrange': [None, 86400000], 'value': '%d %b %Y'},
                    {'dtickrange': [86400000, 604800000], 'value': '%d %b %Y'},
                    {'dtickrange': [604800000, "M1"], 'value': '%d %b %Y'},
                    {'dtickrange': ["M1", "M6"], 'value': '%b %Y'},
                    {'dtickrange': ["M6", None], 'value': '%b %Y'}
                ],
                'rangebreaks': [dict(bounds=["sat", "sun"])],
                'rangeslider': {'visible': False},
                'titlefont': {'family': 'Hanken Grotesk', 'color': '#050A30'},
                'tickfont': {'family': 'Hanken Grotesk'},
                'linewidth': 1,
                'linecolor': 'black'
            },
            'plot_bgcolor': 'white',
            'paper_bgcolor': 'white',
            'font': {'family': 'Hanken Grotesk'},
            'showlegend': True,
            'height': 500,
            'margin': dict(l=50, r=50, t=50, b=50)
        }
    }

    return price_fig

@app.callback(
    [Output('forecast-graph', 'figure'),
     Output('recommendations-container', 'children')],
    [Input('index-dropdown', 'value'),
     Input('model-selection', 'value'),
     Input('forecast-period-dropdown', 'value'),
     Input('earnings-percentage-input', 'value')]
)
def update_forecast_graph(ticker, model_type, forecast_days, earnings_percentage):
    data = download_data(ticker)
        
    shapes = []

    if model_type == 'ARIMA-GARCH':
        arima_model, garch_fitted, train_returns, test_returns, closing_prices = fit_arima_garch(data)
        predicted_prices, forecast_data = forecast_arima_garch(arima_model, garch_fitted, train_returns, test_returns, closing_prices, forecast_days)
        
        min_price = min(closing_prices.min(), forecast_data.min(), predicted_prices.min())
        max_price = max(closing_prices.max(), forecast_data.max(), predicted_prices.max())

        shapes.extend([
            dict(
                type="line",
                x0=closing_prices.index[train_returns.shape[0]],
                y0=min_price,
                x1=closing_prices.index[train_returns.shape[0]],
                y1=max_price,
                line=dict(
                    color="Purple",
                    width=2,
                    dash="dash",
                    name='Train-Test Split'
                ),
            ),
            dict(
                type="line",
                x0=forecast_data.index[0],
                y0=min_price,
                x1=forecast_data.index[0],
                y1=max_price,
                line=dict(
                    color="Black",
                    width=2,
                    dash="dash",
                    name='Forecast Start'
                ),
            )
        ])

        forecast_fig = {
            'data': [
                go.Scatter(
                    x=closing_prices.index,
                    y=closing_prices,
                    mode='lines',
                    name='Actual Prices',
                    line=dict(color='blue')
                ),
                go.Scatter(
                    x=predicted_prices.index,
                    y=predicted_prices,
                    mode='lines',
                    name='Predicted Prices',
                    line=dict(color='red')
                ),
                go.Scatter(
                    x=forecast_data.index,
                    y=forecast_data,
                    mode='lines',
                    name=f'{forecast_days}-Day Forecast',
                    line=dict(color='green')
                ),
                go.Scatter(
                    x=[closing_prices.index[train_returns.shape[0]]],
                    y=[closing_prices.iloc[train_returns.shape[0]]],
                    mode='lines+markers',
                    name='Train-Test Split',
                    line=dict(color='purple', dash='dash')
                ),
                go.Scatter(
                    x=[forecast_data.index[0]],
                    y=[forecast_data.iloc[0]],
                    mode='lines+markers',
                    name='Forecast Start',
                    line=dict(color='black', dash='dash')
                ),
            ],
            'layout': {
                'title': {
                    'text': f'Predicted Stock Price of {ticker} using ARIMA-GARCH',
                    'font': {'family': 'Prata', 'color': '#050A30'}
                },
                'yaxis': {
                    'title': 'Close Price',
                    'titlefont': {'family': 'Hanken Grotesk', 'color': '#050A30'},
                    'tickfont': {'family': 'Hanken Grotesk'},
                    'range': [min_price, max_price],
                    'zeroline': False
                },
                'xaxis': {
                    'title': 'Date',
                    'type': 'date',
                    'tickformat': '%b %Y',
                    'tickmode': 'auto',
                    'nticks': 20,
                    'tickformatstops': [
                        {'dtickrange': [None, 86400000], 'value': '%d %b %Y'},
                        {'dtickrange': [86400000, 604800000], 'value': '%d %b %Y'},
                        {'dtickrange': [604800000, "M1"], 'value': '%d %b %Y'},
                        {'dtickrange': ["M1", "M6"], 'value': '%b %Y'},
                        {'dtickrange': ["M6", None], 'value': '%b %Y'}
                    ],
                    'titlefont': {'family': 'Hanken Grotesk', 'color': '#050A30'},
                    'tickfont': {'family': 'Hanken Grotesk'},
                    'showline': True,  # Ensure the x-axis line is shown
                    'linewidth': 1,
                    'linecolor': 'black'
                },
                'plot_bgcolor': 'white',
                'paper_bgcolor': 'white',
                'font': {'family': 'Hanken Grotesk'},
                'showlegend': True,
                'height': 500,
                'margin': dict(l=50, r=50, t=50, b=50),
                'shapes': shapes
            }
        }

    elif model_type == 'Prophet':
        model, data_prophet = fit_prophet(data)
        forecast_data = forecast_prophet(model, data_prophet, forecast_days)

        min_price = min(data['Close'].min(), forecast_data['yhat'].min())
        max_price = max(data['Close'].max(), forecast_data['yhat'].max())

        shapes.extend([
            dict(
                type="line",
                x0=data_prophet['ds'].iloc[-1],
                y0=min_price,
                x1=data_prophet['ds'].iloc[-1],
                y1=max_price,
                line=dict(
                    color="Black",
                    width=2,
                    dash="dash",
                    name='Forecast Start'
                ),
            )
        ])

        forecast_fig = {
            'data': [
                go.Scatter(
                    x=data_prophet['ds'],
                    y=data_prophet['y'],
                    mode='lines',
                    name='Actual Prices',
                    line=dict(color='blue')
                ),
                go.Scatter(
                    x=forecast_data['ds'][:-forecast_days],
                    y=forecast_data['yhat'][:-forecast_days],
                    mode='lines',
                    name='Predicted Prices',
                    line=dict(color='red')
                ),
                go.Scatter(
                    x=forecast_data['ds'][:-forecast_days],
                    y=forecast_data['yhat_upper'][:-forecast_days],
                    fill=None,
                    mode='lines',
                    line=dict(color='orangered', width=0.4),
                    fillcolor='rgba(255, 69, 0, 0.2)',
                    name='Upper Confidence Interval',
                    showlegend=False
                ),
                go.Scatter(
                    x=forecast_data['ds'][:-forecast_days],
                    y=forecast_data['yhat_lower'][:-forecast_days],
                    fill='tonexty',  # Fill area between yhat and yhat_lower
                    mode='lines',
                    line=dict(color='orangered', width=0.4),
                    fillcolor='rgba(255, 69, 0, 0.2)',
                    name='Lower Confidence Interval',
                    showlegend=False
                ),
                go.Scatter(
                    x=forecast_data['ds'][-forecast_days:],  # Only the new forecast period
                    y=forecast_data['yhat'][-forecast_days:],  # Only the new forecast period
                    mode='lines',
                    name=f'{forecast_days}-Day Forecast',
                    line=dict(color='green')
                ),
                go.Scatter(
                    x=forecast_data['ds'][-forecast_days:],
                    y=forecast_data['yhat_upper'][-forecast_days:],
                    fill=None,
                    mode='lines',
                    line=dict(color='green', width=0.4),
                    fillcolor='rgba(28, 184, 24, 0.25)',
                    name='Upper Confidence Interval',
                    showlegend=False
                ),
                go.Scatter(
                    x=forecast_data['ds'][-forecast_days:],
                    y=forecast_data['yhat_lower'][-forecast_days:],
                    fill='tonexty',  # Fill area between yhat and yhat_lower
                    mode='lines',
                    line=dict(color='green', width=0.4),
                    fillcolor='rgba(28, 184, 24, 0.25)',
                    name='Lower Confidence Interval',
                    showlegend=False
                ),
                go.Scatter(
                    x=[data_prophet['ds'].iloc[-1]],
                    y=[data['Close'].iloc[-1]],
                    mode='lines+markers',
                    name='Forecast Start',
                    line=dict(color='black', dash='dash')
                ),
            ],
            'layout': {
                'title': {
                    'text': f'Predicted Stock Price of {ticker} using Prophet',
                    'font': {'family': 'Prata', 'color': '#050A30'}
                },
                'yaxis': {
                    'title': 'Close Price',
                    'titlefont': {'family': 'Hanken Grotesk', 'color': '#050A30'},
                    'tickfont': {'family': 'Hanken Grotesk'},
                    'range': [max(0, min_price), max_price],
                    'zeroline': False
                },
                'xaxis': {
                    'title': 'Date',
                    'type': 'date',
                    'tickformat': '%b %Y',
                    'tickmode': 'auto',
                    'nticks': 20,
                    'tickformatstops': [
                        {'dtickrange': [None, 86400000], 'value': '%d %b %Y'},
                        {'dtickrange': [86400000, 604800000], 'value': '%d %b %Y'},
                        {'dtickrange': [604800000, "M1"], 'value': '%d %b %Y'},
                        {'dtickrange': ["M1", "M6"], 'value': '%b %Y'},
                        {'dtickrange': ["M6", None], 'value': '%b %Y'}
                    ],
                    'titlefont': {'family': 'Hanken Grotesk', 'color': '#050A30'},
                    'tickfont': {'family': 'Hanken Grotesk'},
                    'showline': True,  # Ensure the x-axis line is shown
                    'linewidth': 1,
                    'linecolor': 'black'
                },
                'plot_bgcolor': 'white',
                'paper_bgcolor': 'white',
                'font': {'family': 'Hanken Grotesk'},
                'showlegend': True,
                'height': 500,
                'margin': dict(l=50, r=50, t=50, b=50),
                'shapes': shapes
            }
        }

    elif model_type == 'LSTM':

        model, sc = load_lstm(ticker)
        closing_prices, train_returns, scaled_prices, stationary, lookback_period = fit_lstm(data, sc)
        predicted_stock_price, forecast_data = forecast_lstm(model, sc, closing_prices, train_returns, scaled_prices, stationary, lookback_period, forecast_days)

        forecast_dates = pd.date_range(start=data.index[-1], periods=forecast_days, freq='B')
        
        # Ensure forecast_data is 1D array for Plotly
        forecast_data = forecast_data.flatten()
        predicted_stock_price = predicted_stock_price.flatten()

        # Convert to Pandas Series
        forecast_data_series = pd.Series(forecast_data, index=forecast_dates)
        predicted_stock_price_series = pd.Series(predicted_stock_price, index=data.index[lookback_period:])
        closing_prices_series = pd.Series(closing_prices.flatten(), index=data.index)

        min_price = min(closing_prices_series.min(), forecast_data_series.min())
        max_price = max(closing_prices_series.max(), forecast_data_series.max())

        shapes.extend([
            dict(
                type="line",
                x0=data.index[-1],
                y0=min_price,
                x1=data.index[-1],
                y1=max_price,
                line=dict(
                    color="Black",
                    width=2,
                    dash="dash",
                    name='Forecast Start'
                ),
            )
        ])

        forecast_fig = {
            'data': [
                go.Scatter(
                    x=closing_prices_series.index,
                    y=closing_prices_series,
                    mode='lines',
                    name='Actual Prices',
                    line=dict(color='blue')
                ),
                go.Scatter(
                    x=predicted_stock_price_series.index,
                    y=predicted_stock_price_series,
                    mode='lines',
                    name='Predicted Prices',
                    line=dict(color='red')
                ),
                go.Scatter(
                    x=forecast_data_series.index,
                    y=forecast_data_series,
                    mode='lines',
                    name=f'{forecast_days}-Day Forecast',
                    line=dict(color='green')
                ),
                go.Scatter(
                    x=[data.index[-1]],
                    y=[closing_prices_series[-1]],
                    mode='lines+markers',
                    name='Forecast Start',
                    line=dict(color='black', dash='dash')
                ),
            ],
            'layout': {
                'title': {
                    'text': f'Predicted Stock Price of {ticker} using LSTM',
                    'font': {'family': 'Prata', 'color': '#050A30'}
                },
                'yaxis': {
                    'title': 'Close Price',
                    'titlefont': {'family': 'Hanken Grotesk', 'color': '#050A30'},
                    'tickfont': {'family': 'Hanken Grotesk'},
                    'range': [min_price, max_price],
                    'zeroline': False
                },
                'xaxis': {
                    'title': 'Date',
                    'type': 'date',
                    'tickformat': '%b %Y',
                    'tickmode': 'auto',
                    'nticks': 20,
                    'tickformatstops': [
                        {'dtickrange': [None, 86400000], 'value': '%d %b %Y'},
                        {'dtickrange': [86400000, 604800000], 'value': '%d %b %Y'},
                        {'dtickrange': [604800000, "M1"], 'value': '%d %b %Y'},
                        {'dtickrange': ["M1", "M6"], 'value': '%b %Y'},
                        {'dtickrange': ["M6", None], 'value': '%b %Y'}
                    ],
                    'titlefont': {'family': 'Hanken Grotesk', 'color': '#050A30'},
                    'tickfont': {'family': 'Hanken Grotesk'},
                    'showline': True,  # Ensure the x-axis line is shown
                    'linewidth': 1,
                    'linecolor': 'black'
                },
                'plot_bgcolor': 'white',
                'paper_bgcolor': 'white',
                'font': {'family': 'Hanken Grotesk'},
                'showlegend': True,
                'height': 500,
                'margin': dict(l=50, r=50, t=50, b=50),
                'shapes': shapes
            }
        }

    # Define recommended buy price
    today_price = data['Close'].iloc[-1]
    recommended_buy_price = today_price
    buy_date = pd.to_datetime('today').strftime('%B %d, %Y')

    recommended_sell_price = recommended_buy_price * (1 + earnings_percentage / 100)

    if model_type == 'ARIMA-GARCH':
        future_forecast_data = forecast_data[forecast_data.index >= pd.to_datetime('today')]
        possible_sell = (future_forecast_data >= recommended_sell_price).any()
    elif model_type == 'Prophet':
        future_forecast_data = forecast_data[forecast_data['ds'] >= pd.to_datetime('today')]
        possible_sell = (future_forecast_data['yhat'] >= recommended_sell_price).any()
    else:
        future_forecast_data = pd.DataFrame(forecast_data, index=forecast_dates)
        possible_sell = (future_forecast_data >= recommended_sell_price).any().any()

    if not possible_sell:
        sell_date = "Not possible within forecasted period"
        recommended_sell_price = "N/A"
    else:
        if model_type == 'ARIMA-GARCH':
            sell_candidates = future_forecast_data[future_forecast_data >= recommended_sell_price]
            sell_date_idx = sell_candidates.index[0] if not sell_candidates.empty else None
        elif model_type == 'Prophet':
            sell_candidates = future_forecast_data[future_forecast_data['yhat'] >= recommended_sell_price]
            sell_date_idx = sell_candidates['ds'].iloc[0] if not sell_candidates.empty else None
        else:
            sell_candidates = future_forecast_data[future_forecast_data[0] >= recommended_sell_price]
            sell_date_idx = sell_candidates.index[0] if not sell_candidates.empty else None

        if sell_date_idx is not None:
            sell_date = sell_date_idx.strftime('%B %d, %Y')
            recommended_sell_price = f"{recommended_sell_price:.2f}"
        else:
            sell_date = "Not possible within forecasted period"
            recommended_sell_price = "N/A"

    recommendations = dbc.Container([
        dbc.Card([
            dbc.CardBody([
                html.H4("Investment Recommendations", className="card-title", style={'color': '#050A30', 'font-family': 'Prata', 'text-align': 'center'}),
                html.Div([
                    html.Div([
                        html.Img(src='/assets/forecast/buy.png', style={'width': '30px', 'margin-right': '15px'}),
                        html.Span(f"Buy Price: ${recommended_buy_price:.2f} on {buy_date}", style={'color': '#050A30', 'font-family': 'Hanken Grotesk', 'font-size': '18px'})
                    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                    html.Div([
                        html.Img(src='/assets/forecast/sell.png', style={'width': '30px', 'margin-right': '15px'}),
                        html.Span(f"Sell Price: ${recommended_sell_price} on {sell_date}", style={'color': '#050A30', 'font-family': 'Hanken Grotesk', 'font-size': '18px'})
                    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'margin-top': '20px'})
                ], style={'text-align': 'center', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'width': '600px'})
            ])
        ], className='fade-in-card', style={'margin-top': '5px', 'text-align': 'center'})
    ], className='fade-in-element', style={'display': 'flex', 'justify-content': 'center'})

    return forecast_fig, recommendations

@app.callback(
    Output('recommendations-container', 'key'),
    [Input('index-dropdown', 'value'),
     Input('model-selection', 'value'),
     Input('earnings-percentage-input', 'value')]
)
def update_recommendations_key(ticker, model_type, earnings_percentage):
    return f"recommendations-{ticker}-{model_type}-{earnings_percentage}"
