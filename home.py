import dash_bootstrap_components as dbc

# Layout for home page
layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    dbc.Carousel(
                        items=[
                            {
                                "key": "1",
                                "src": "assets/home/1.png",
                                "header": "Welcome to TrendAnalyzer",
                                "caption": "Analyze stock trends with forecasting models such as ARIMA-GARCH, Prophet, and LSTM models, offering comprehensive insights into market dynamics and helping you stay ahead of the curve.",
                            },
                            {
                                "key": "2",
                                "src": "/assets/home/2.png",
                                "header": "Get Accurate Predictions",
                                "caption": "Make informed decisions with our reliable stock price predictions, designed to give you an edge in the market by leveraging advanced statistical techniques and data analysis.",
                            },
                            {
                                "key": "3",
                                "src": "/assets/home/3.png",
                                "header": "Cutting-edge Technology",
                                "caption": "Leverage the power of machine learning for your investments, utilizing advanced algorithms and state-of-the-art technologies for optimal results, ensuring you maximize your returns.",
                            }
                        ],
                        className="carousel-fade fade-in-element",
                        interval=3000,
                        variant="dark"
                    )
                ],
                className="p-0"
            )
        )
    ],
    fluid=True,
    className='container-fluid fade-in-container'
)
