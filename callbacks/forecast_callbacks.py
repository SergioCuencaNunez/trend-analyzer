from dash import Input, Output, html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from helpers.forecast_helpers import calculate_moving_averages, create_price_figure, perform_forecast, calculate_recommendations
from models.utils import download_data

def register_callbacks(app):
    @app.callback(
        Output('price-graph', 'figure'),
        [Input('index-dropdown', 'value')]
    )
    def update_price_graph(ticker):
        data = download_data(ticker)
        ma50, ma200 = calculate_moving_averages(data)
        return create_price_figure(data, ma50, ma200, ticker)

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

        if model_type == 'XGBoost':
            min_price, max_price, train_df, test_df, test_predicted, forecast_data = perform_forecast(data, ticker, model_type, forecast_days)
            shapes.extend([
                dict(
                    type="line",
                    x0=test_df.index[0],
                    y0=min_price,
                    x1=test_df.index[0],
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
                        x=data.index,
                        y=data['Close'],
                        mode='lines',
                        name='Actual Prices',
                        line=dict(color='blue')
                    ),
                    go.Scatter(
                        x=test_df.index,
                        y=test_predicted,
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
                        x=[test_df.index[0]],
                        y=[data['Close'].iloc[len(train_df)]],
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
                        'text': f'Predicted Stock Price of {ticker} using XGBoost',
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
                        'showline': True,
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
            min_price, max_price, data_prophet, forecast_data = perform_forecast(data, ticker, model_type, forecast_days)
        
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
                        fill='tonexty',
                        mode='lines',
                        line=dict(color='orangered', width=0.4),
                        fillcolor='rgba(255, 69, 0, 0.2)',
                        name='Lower Confidence Interval',
                        showlegend=False
                    ),
                    go.Scatter(
                        x=forecast_data['ds'][-forecast_days:],
                        y=forecast_data['yhat'][-forecast_days:],
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
                        fill='tonexty',
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
            
        buy_date, recommended_buy_price, sell_date, recommended_sell_price = calculate_recommendations(data, model_type, forecast_data, earnings_percentage)

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