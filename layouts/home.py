import dash_bootstrap_components as dbc

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
                                "caption": "Discover market trends and insights with TrendAnalyzer. Dive deep into stock performance analysis, forecast upcoming trends, and stay updated with real-time news to make well-informed and strategic investment decisions.",
                            },
                            {
                                "key": "2",
                                "src": "/assets/home/2.png",
                                "header": "Cutting-edge Technology",
                                "caption": "Empower your investments with our state-of-the-art forecasting models, including XGBoost and Prophet. Our platform leverages advanced machine learning and statistical methods to elevate your market analysis and maximize potential returns.",
                            },
                            {
                                "key": "3",
                                "src": "/assets/home/3.png",
                                "header": "Real-time News",
                                "caption": "Stay ahead with the latest financial news and in-depth stock performance insights. Our platform consolidates essential news and detailed metrics, offering you a holistic view of market conditions and emerging opportunities.",
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
