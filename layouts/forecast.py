from dash import dcc, html
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.H1("Forecast Stock Prices", className='fade-in-element', style={'text-align': 'center', 'margin-top': '40px', 'font-family': 'Prata'}),
    dbc.Row([
        dbc.Col([
            html.H4('Select the Stock to Predict', className='fade-in-element', style={'margin': '20px 0', 'text-align': 'center'}),
            dcc.Dropdown(
                id='index-dropdown',
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
        ], width=4),
        dbc.Col([
            html.H4('Select the Forecast Period', className='fade-in-element', style={'margin': '20px 0', 'text-align': 'center'}),
            dcc.Dropdown(
                id='forecast-period-dropdown',
                options=[
                    {'label': '1 Week', 'value': 7},
                    {'label': '1 Month', 'value': 30},
                    {'label': '3 Months', 'value': 90},
                ],
                value=30,
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
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.RadioItems(
                    id='model-selection',
                    options=[
                        {'label': 'Prophet', 'value': 'Prophet'},
                        {'label': 'XGBoost', 'value': 'XGBoost'}
                    ],
                    value='Prophet',
                    labelStyle={'display': 'inline-block'},
                    className='radio-group fade-in-element',
                    style={'font-family': 'Hanken Grotesk'}
                ),
            ], style={'text-align': 'center'}),
            dcc.Loading(
                id="loading-graph",
                type="default",
                children=[
                    dcc.Graph(id='price-graph', className='fade-in-graph', style={'margin-top': '30px', 'margin-bottom': '30px', 'height': '500px', 'backgroundColor': 'white', 'border': '1px solid #CCCCCC', 'border-radius': '10px', 'padding': '10px 0px 510px 0px'}),
                    dcc.Graph(id='forecast-graph', className='fade-in-graph', style={'margin-top': '30px', 'height': '500px', 'backgroundColor': 'white', 'border': '1px solid #CCCCCC', 'border-radius': '10px', 'padding': '10px 0px 510px 0px'})
                ],
                style={'min-height': '600px'}
            ),
            html.Div(id='recommendations-container', className='fade-in-element', style={'margin-top': '20px', 'text-align': 'center', 'font-family': 'Hanken Grotesk'})
        ])
    ], style={'margin-bottom': '20px'}),
], fluid=True, className="container")
