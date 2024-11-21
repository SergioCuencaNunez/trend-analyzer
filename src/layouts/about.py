from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container(
    [
        html.H1("About TrendAnalyzer", className='fade-in-text', style={'text-align': 'center', 'margin-top': '40px'}),
        html.P("TrendAnalyzer is a powerful tool designed to help you analyze and forecast stock prices using cutting-edge models like XGBoost and Prophet. Our mission is to provide accurate and reliable stock price predictions to help you make informed investment decisions.", className='fade-in-text', style={'text-align': 'center'}),
        
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
                    md=6
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardImg(src='/assets/about/boosting.png', top=True, className='zoom-in-image', style={'width': '20%', 'padding': '10px 0px 0px 0px'}),
                            dbc.CardBody(
                                [
                                    html.H4("XGBoost Model", className="card-title"),
                                    html.P("XGBoost uses gradient boosting to deliver fast, accurate, and efficient stock price predictions. It excels in handling complex relationships and interactions within the data. With its ability to process large datasets, and prevent overfitting through regularization techniques, XGBoost ensures robust and reliable forecasting results.", className="card-text"),
                                ]
                            ),
                        ],
                        className='fade-in-card',  # Add this class for animation
                        style={'text-align': 'center'}
                    ),
                    md=6
                ),
            ],
            style={'margin-top': '40px'}
        ),
        html.H2("News & Performance", className='fade-in-text', style={'text-align': 'center', 'margin-top': '40px'}),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardImg(src='/assets/about/news.png', top=True, className='zoom-in-image', style={'width': '20%', 'padding': '10px 0px 0px 0px'}),
                            dbc.CardBody(
                                [
                                    html.H4("Latest Financial News", className="card-title"),
                                    html.P(
                                        "Stay informed with the latest developments in the financial world. Our platform aggregates news from trusted sources, "
                                        "providing insights into market trends, company earnings, and industry updates. This comprehensive coverage ensures you "
                                        "never miss important financial events or opportunities.",
                                        className="card-text"
                                    ),
                                    html.Hr(),
                                    html.H4("Stock Performance Metrics", className="card-title"),
                                    dbc.Col(
                                        html.P(
                                            "Track essential performance indicators such as Price-to-Earnings (P/E) ratios, Return on Investment (ROI), "
                                            "volatility trends, and profit margins. These metrics allow you to evaluate a stock's valuation, profitability, "
                                            "and risk level effectively. Our platform enables data-driven decision-making by presenting these metrics alongside "
                                            " news and analysis. Whether you're monitoring a portfolio or exploring new investment opportunities, you’ll have the tools to succeed.",
                                            className="card-text"
                                        ),
                                        className="d-flex align-items-center"
                                    ),
                                ]
                            ),
                        ],
                        className='fade-in-card',
                        style={'text-align': 'center'}
                    ),
                    md=12
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
                        className='fade-in-card',
                        style={'text-align': 'center'}
                    ),
                    md=12
                ),
            ],
            style={'margin-top': '40px', 'margin-bottom': '40px'}
        ),
    ],
    className='container-fluid',
)
