from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container(
    [
        html.H1("About TrendAnalyzer", className='fade-in-text', style={'text-align': 'center', 'margin-top': '40px'}),
        html.P("TrendAnalyzer is a powerful tool designed to help you analyze and forecast stock prices using cutting-edge models like ARIMA-GARCH, Prophet, and LSTM. Our mission is to provide accurate and reliable stock price predictions to help you make informed investment decisions.", className='fade-in-text', style={'text-align': 'center'}),
        
        html.P("TrendAnalyzer uses stock time series data from Yahoo Finance and applies advanced statistical and machine learning models to make forecasts and provide actionable insights. This process involves data collection, preprocessing, model training, and prediction. The result is a set of accurate and reliable forecasts that can guide your investment strategies in the stock market.", className='fade-in-text', style={'text-align': 'center', 'margin-top': '20px'}),
        
        html.H2("Features", className='fade-in-text', style={'text-align': 'center', 'margin-top': '40px'}),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardImg(src='/assets/about/accuracy.png', top=True, className='zoom-in-image', style={'width': '20%', 'padding': '10px 0px 0px 0px'}),
                            dbc.CardBody(
                                [
                                    html.H4("High Accuracy", className="card-title"),
                                    html.P("Our models leverage advanced machine learning algorithms to deliver highly accurate stock price forecasts. By analyzing historical data and market trends, we provide predictions you can trust.", className="card-text"),
                                ]
                            ),
                        ],
                        className='fade-in-card',  # Add this class for animation
                        style={'text-align': 'center'}
                    ),
                    md=4
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardImg(src='/assets/about/reliability.png', top=True, className='zoom-in-image', style={'width': '20%', 'padding': '10px 0px 0px 0px'}),
                            dbc.CardBody(
                                [
                                    html.H4("Reliability", className="card-title"),
                                    html.P("Our models are backed by extensive research and rigorous testing to ensure dependable results. We continuously update our algorithms to adapt to changing market conditions.", className="card-text"),
                                ]
                            ),
                        ],
                        className='fade-in-card',  # Add this class for animation
                        style={'text-align': 'center'}
                    ),
                    md=4
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardImg(src='/assets/about/user-friendly.png', top=True, className='zoom-in-image', style={'width': '20%', 'padding': '10px 0px 0px 0px'}),
                            dbc.CardBody(
                                [
                                    html.H4("User-Friendly", className="card-title"),
                                    html.P("Designed with an intuitive interface, TrendAnalyzer is easy to navigate for all users. Whether you're a seasoned trader or a beginner, our platform makes it simple to get the insights you need.", className="card-text"),
                                ]
                            ),
                        ],
                        className='fade-in-card',  # Add this class for animation
                        style={'text-align': 'center'}
                    ),
                    md=4
                ),
            ],
            style={'margin-top': '40px'}
        ),

        html.H2("Models", className='fade-in-text', style={'text-align': 'center', 'margin-top': '40px'}),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardImg(src='/assets/about/time-series.png', top=True, className='zoom-in-image', style={'width': '20%', 'padding': '10px 0px 0px 0px'}),
                            dbc.CardBody(
                                [
                                    html.H4("ARIMA-GARCH Model", className="card-title"),
                                    html.P("The ARIMA-GARCH model combines AutoRegressive Integrated Moving Average (ARIMA) and Generalized AutoRegressive Conditional Heteroskedasticity (GARCH) to capture both linear and volatility patterns in stock prices. This dual approach ensures more accurate and robust forecasts.", className="card-text"),
                                ]
                            ),
                        ],
                        className='fade-in-card',  # Add this class for animation
                        style={'text-align': 'center'}
                    ),
                    md=4
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardImg(src='/assets/about/facebook.png', top=True, className='zoom-in-image', style={'width': '20%', 'padding': '10px 0px 0px 0px'}),
                            dbc.CardBody(
                                [
                                    html.H4("Prophet Model", className="card-title"),
                                    html.P("Prophet is a time series forecasting model developed by Facebook. It's designed to handle time series data that exhibits strong seasonal effects and multiple seasonality with a daily cycle. Prophet is robust to missing data and shifts in the trend, and it typically produces accurate forecasts for time series data.", className="card-text"),
                                ]
                            ),
                        ],
                        className='fade-in-card',  # Add this class for animation
                        style={'text-align': 'center'}
                    ),
                    md=4
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardImg(src='/assets/about/neural-network.png', top=True, className='zoom-in-image', style={'width': '20%', 'padding': '10px 0px 0px 0px'}),
                            dbc.CardBody(
                                [
                                    html.H4("LSTM Model", className="card-title"),
                                    html.P("Long Short-Term Memory (LSTM) networks are a type of recurrent neural network capable of learning long-term dependencies. LSTM is particularly powerful for time series forecasting as it can remember past data points over long sequences, making it ideal for predicting stock prices based on historical trends.", className="card-text"),
                                ]
                            ),
                        ],
                        className='fade-in-card',  # Add this class for animation
                        style={'text-align': 'center'}
                    ),
                    md=4
                ),
            ],
            style={'margin-top': '40px'}
        ),

        html.H2("Get in Touch", className='fade-in-text', style={'text-align': 'center', 'margin-top': '40px'}),
        html.P("We'd love to hear from you! Whether you have questions, feedback, or need support, feel free to reach out to us.", className='fade-in-text', style={'text-align': 'center'}),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H4("Contact Us", className="card-title"),
                                    html.P("Email: scuenca06@gmail.com", className="card-text"),
                                ]
                            ),
                        ],
                        className='fade-in-card',  # Add this class for animation
                        style={'text-align': 'center'}
                    ),
                    md=12
                ),
            ],
            style={'margin-top': '40px'}
        ),
    ],
    className='container-fluid',
)
