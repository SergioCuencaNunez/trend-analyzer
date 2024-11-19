from dash import dcc, html
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.H1("Stock News & Performance", className='fade-in-element', style={'text-align': 'center', 'margin-top': '40px', 'font-family': 'Prata'}),
    dcc.Store(id='clicks-store', data=1),
    dbc.Row(
        justify="center",
        children=[
            dbc.Col(
                html.H4('Select Stock', className='fade-in-element', style={'margin-right': '10px', 'text-align': 'center'}),
                width="auto",
                className="d-flex align-items-center"
            ),
            dbc.Col(
                dcc.Dropdown(
                    id='stock-dropdown',
                    options=[
                        {'label': 'AAPL', 'value': 'AAPL'},
                        {'label': 'AMZN', 'value': 'AMZN'},
                        {'label': 'NVDA', 'value': 'NVDA'},
                        {'label': 'ASML', 'value': 'ASML'},
                        {'label': 'TSLA', 'value': 'TSLA'},
                        {'label': 'GOOGL', 'value': 'GOOGL'},
                        {'label': 'MARA', 'value': 'MARA'},
                        {'label': 'RIOT', 'value': 'RIOT'},
                        {'label': 'MSFT', 'value': 'MSFT'},
                        {'label': 'NFLX', 'value': 'NFLX'},
                        {'label': 'SMCI', 'value': 'SMCI'},
                        {'label': 'MSTR', 'value': 'MSTR'}
                    ],
                    value='AAPL',
                    className='fade-in-element',
                    style={'margin-bottom': '20px'}
                ),
                width=4
            )
        ],
        className="mb-3"
    ),
    dbc.Row(
        dbc.Col(
            dcc.Loading(
                id="loading-full-content",
                type="default",
                children=html.Div(
                    id='data-content',
                    children=[
                        dbc.Row([
                            dbc.Col(html.H3("Relevant Information", id='info-title', className='fade-in-text', style={'text-align': 'center', 'font-family': 'Prata', 'display': 'none'}), style={'text-align': 'center'}, width=12),
                        ]),
                        dbc.Row([
                            dbc.Col(html.Div(id='performance-table', className='fade-in-element'), width=12)
                        ], style={'margin-bottom': '20px'}),
                        dbc.Row([
                            dbc.Col(html.H3("Latest News", id='news-title', className='fade-in-text', style={'text-align': 'center', 'font-family': 'Prata', 'display': 'none'}), style={'text-align': 'center'}, width=12),
                        ]),
                        dbc.Row(
                            id='news-cards-row', 
                            className="g-3 fade-in-element", 
                            style={'margin-bottom': '20px'}
                        ),
                        dbc.Row(
                            dbc.Col(
                                dbc.Button("Load More News", id='load-more-button', color="primary", style={'display': 'block'}, className='fade-in-button'),
                                width="auto",
                                style={'display': 'flex', 'justify-content': 'center', 'margin-top': '10px'}
                            ),
                            className="mb-4 justify-content-center"
                        ),
                        dbc.Row([
                            dbc.Col(html.H3("Ratings", id='ratings-title', className='fade-in-text', style={'text-align': 'center', 'font-family': 'Prata', 'display': 'none'}), style={'text-align': 'center'}, width=12),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.Div(id='ratings-table', className='fade-in-table'),
                                dbc.Row(
                                    dbc.Col(
                                        dbc.Button("Load More Ratings", id='load-more-ratings-button', color="primary", style={'display': 'block'}, className='fade-in-button'),
                                        width="auto"
                                    ),
                                    justify='center',
                                    style={'margin-top': '10px'}
                                )
                            ], width=12)
                        ])
                    ],
                    style={'min-height': '600px'}
                )
            )
        )
    )
], fluid=True, className="container")
