from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from helpers.forecast_helpers import fetch_stock_data, create_metrics_card, calculate_metrics, create_growth_bar, create_profitability_bar, create_volatility_graph 
from helpers.forecast_helpers import calculate_moving_averages, create_price_figure, perform_forecast, calculate_recommendations
from models.utils import download_data

def register_callbacks(app):
    @app.callback(
        Output('metrics-cards-row', 'children'),
        [Input('index-dropdown', 'value')]
    )
    def update_metrics_cards(ticker):
        stock_data, stock_info = fetch_stock_data(ticker)
        metrics = calculate_metrics(stock_data, stock_info)
        return [create_metrics_card(metric) for metric in metrics]

    @app.callback(
        Output('growth-bar', 'figure'),
        [Input('index-dropdown', 'value')]
    )
    def update_growth_bar(ticker):
        stock_data, stock_info = fetch_stock_data(ticker)
        growth_metrics = {
            'Revenue Growth (YoY)': stock_info.get('revenueGrowth'),
            'Earnings Growth (YoY)': stock_info.get('earningsGrowth'),
            'Revenue Quarterly Growth (QoQ)': stock_info.get('revenueQuarterlyGrowth'),
            'Earnings Quarterly Growth (QoQ)': stock_info.get('earningsQuarterlyGrowth')
        }
        growth_metrics = {k: v * 100 for k, v in growth_metrics.items() if v is not None}
        return create_growth_bar(growth_metrics)

    @app.callback(
        Output('profitability-bar', 'figure'),
        [Input('index-dropdown', 'value')]
    )
    def update_profitability_bar(ticker):
        stock_data, stock_info = fetch_stock_data(ticker)
        profitability_metrics = {
            'Profit Margins': stock_info.get('profitMargins'),
            'Gross Margins': stock_info.get('grossMargins'),
            'Operating Margins': stock_info.get('operatingMargins'),
            'Return on Assets': stock_info.get('returnOnAssets'),
            'Return on Equity': stock_info.get('returnOnEquity')
        }
        profitability_metrics = {k: v * 100 for k, v in profitability_metrics.items() if v is not None}
        return create_profitability_bar(profitability_metrics)

    @app.callback(
        Output('volatility-graph', 'figure'),
        [Input('index-dropdown', 'value')]
    )
    def update_volatility_graph(ticker):
        stock_data, _ = fetch_stock_data(ticker)
        return create_volatility_graph(stock_data)

    @app.callback(
        Output('price-graph', 'figure'),
        [Input('index-dropdown', 'value')]
    )
    def update_price_graph(ticker):
        data = download_data(ticker)
        ma50, ma200 = calculate_moving_averages(data)
        return create_price_figure(data, ma50, ma200, ticker)

    @app.callback(
        [
            Output('forecast-graph', 'figure'),
            Output('forecast-graph', 'style'),
            Output('recommendations-container', 'children'),
            Output('recommendations-container', 'style'),
            Output('gauge-container', 'children'),
            Output('gauge-container', 'style'),
            Output('loading-forecast', 'style'), 
        ],
        [
            Input('generate-forecast-btn', 'n_clicks')
        ],
        [
            State('index-dropdown', 'value'),
            State('model-selection', 'value'),
            State('forecast-period-dropdown', 'value'),
            State('earnings-percentage-input', 'value')
        ]
    )
    def update_forecast_graph(n_clicks, ticker, model_type, forecast_days, earnings_percentage):
        first_click_style = {
            'position': 'relative',
            'z-index': '1'
        }
        subsequent_click_style = {
            'position': 'absolute',
            'top': 0,
            'left': 0,
            'width': '100%',
            'height': '100%',
            'display': 'flex',
            'align-items': 'center',
            'justify-content': 'center',
            'z-index': 10,
        }

        if not n_clicks:
            return {}, {'display': 'none'}, None, {'display': 'none'}, None, {'display': 'none'},first_click_style
        
        data = download_data(ticker)
        _, stock_info = fetch_stock_data(ticker)
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

        forecast_graph_style = {
            'margin-top': '30px',
            'height': '500px',
            'backgroundColor': 'white',
            'border': '1px solid #CCCCCC',
            'border-radius': '10px',
            'padding': '10px 0px 510px 0px',
            'display': 'block'
        }

        recommendation_key = stock_info.get('recommendationKey', 'N/A').capitalize()
        recommendation_mean = stock_info.get('recommendationMean', 'N/A')

        gauge_graph = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=recommendation_mean if recommendation_mean != 'N/A' else 0,
            delta={'reference': 2.5},
            gauge={
                'axis': {'range': [1, 5], 'tickvals': [1, 2, 3, 4, 5], 'ticktext': ['Strong Buy', 'Buy', 'Hold', 'Sell', 'Strong Sell']},
                'bar': {'color': "green" if recommendation_mean and recommendation_mean < 3 else "red"},
                'steps': [
                    {'range': [1, 2], 'color': "lightgreen"},
                    {'range': [2, 3], 'color': "yellow"},
                    {'range': [3, 4], 'color': "orange"},
                    {'range': [4, 5], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "blue", 'width': 4},
                    'thickness': 0.75,
                    'value': recommendation_mean if recommendation_mean != 'N/A' else 0
                }
            },
            title={
                'text': f'Market Sentiment Recommendation: {recommendation_key.replace("_", " ").title()}', 
                'font': {'family': 'Prata', 'size': 18, 'color': '#050A30'}
            }
        ))
        gauge_graph.update_layout(
            font={'family': 'Hanken Grotesk', 'color': '#050A30'},
            margin=dict(l=20, r=20, t=50, b=20),
            height=250,
            paper_bgcolor="white"
        )
        gauge_graph_style = {
            'display': 'block',
            'justify-content': 'center',
            'align-items': 'center',
            'backgroundColor': 'white',
            'border': '1px solid #CCCCCC',
            'border-radius': '10px',
            'overflow': 'hidden',
            'padding': '10px',
        }
    
        buy_date, recommended_buy_price, sell_date, recommended_sell_price = calculate_recommendations(data, model_type, forecast_data, earnings_percentage)

        recommendations = dbc.Container([
            html.Div([
                html.H5("Buy and Sell Strategy for Target Earnings", 
                        className="fade-in-text", 
                        style={'color': '#050A30', 
                            'font-family': 'Prata', 
                            'text-align': 'center', 
                            'margin-bottom': '35px'}),
                html.Div([
                    html.Div([
                        html.Img(src='/assets/forecast/buy.png', style={'width': '50px', 'margin-right': '15px'}),
                        html.Span(f"Buy Price: ${recommended_buy_price:.2f} on {buy_date}", 
                                style={'color': '#050A30', 'font-family': 'Hanken Grotesk', 'font-size': '18px'})
                    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                    html.Div([
                        html.Img(src='/assets/forecast/sell.png', style={'width': '50px', 'margin-right': '15px'}),
                        html.Span(f"Sell Price: ${recommended_sell_price} on {sell_date}", 
                                style={'color': '#050A30', 'font-family': 'Hanken Grotesk', 'font-size': '18px'})
                    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'margin-top': '20px'})
                ], style={
                    'text-align': 'center', 
                    'display': 'flex', 
                    'flex-direction': 'column', 
                    'align-items': 'center', 
                    'width': '600px'
                })
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})
        ], className='fade-in-element', style={
            'display': 'flex', 
            'justify-content': 'center', 
            'align-items': 'center'
        })

        recommendations_style = {
            'display': 'flex',
            'flex-direction': 'column',
            'justify-content': 'center',
            'align-items': 'center',
            'padding': '10px',
            'height': '100%',
            'overflow': 'hidden',
            'border': '1px solid #CCCCCC',
            'border-radius': '10px',
            'backgroundColor': 'white'
        }
        loading_style = first_click_style if n_clicks and n_clicks < 1 else subsequent_click_style

        return forecast_fig, forecast_graph_style, recommendations, recommendations_style, dcc.Graph(figure=gauge_graph), gauge_graph_style, loading_style
