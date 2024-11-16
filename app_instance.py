import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "TrendAnalyzer"
app._favicon = 'favicon.ico'  # Reference to the favicon

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        <link rel="icon" type="image/x-icon" href="/assets/favicon.ico">
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400&family=Prata&display=swap" rel="stylesheet">
    </head>
    <body>
        <div>
            {%app_entry%}
        </div>
        <footer>
            {%config%}
            {%scripts%}
            <script src="/assets/animations.js"></script>
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Navbar(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='/assets/logo-bright.png', height='60px')),
                    ],
                    align="center",
                    className="g-0",
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavItem(dcc.Link('HOME', href='/', className='nav-link', style={'margin-right': '20px'})),
                            dbc.NavItem(dcc.Link('FORECAST', href='/forecast', className='nav-link', style={'margin-right': '20px'})),
                            dbc.NavItem(dcc.Link('NEWS', href='/news', className='nav-link', style={'margin-right': '20px'})),
                            dbc.NavItem(dcc.Link('ABOUT', href='/about', className='nav-link', style={'margin-right': '20px'}))
                        ],
                        className="ms-auto",
                        navbar=True,
                    ),
                    id="navbar-collapse",
                    navbar=True,
                ),
            ]
        ),
        color="#050A30",
        dark=True,
        className="navbar navbar-expand-md navbar-dark",
    ),
    html.Div(id='page-content', className='main-content'),
    html.Footer([
        html.P([
            dcc.Link('Terms and Conditions', href='/terms', className='footer-link'),
            " | © Sergio Cuenca Núñez, December 2024 | Version: 2.2"
        ], style={'text-align': 'center'}),
    ], className="footer")
])

# Validation layout to include all sub-apps' layouts
def load_validation_layout():
    import forecast
    import home
    import news
    import about
    import terms
    return html.Div([
        forecast.layout,
        home.layout,
        news.layout,
        about.layout,
        terms.layout
    ])

app.validation_layout = load_validation_layout()

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    import forecast
    import home
    import news
    import about
    import terms
    
    if pathname == '/':
        return home.layout
    elif pathname == '/forecast':
        return forecast.layout
    elif pathname == '/about':
        return about.layout
    elif pathname == '/terms':
        return terms.layout
    elif pathname == '/news':
        return news.layout
    else:
        return "404 Page Not Found"
