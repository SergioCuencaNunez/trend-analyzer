import os
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
from layouts.forecast import layout as forecast_layout
from layouts.home import layout as home_layout
from layouts.news import layout as news_layout
from layouts.about import layout as about_layout
from layouts.terms import layout as terms_layout
from callbacks.forecast_callbacks import register_callbacks as forecast_callbacks
from callbacks.news_callbacks import register_callbacks as news_callbacks

# External stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "TrendAnalyzer"
app._favicon = 'assets/favicon.ico'

# Custom index HTML
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        <link rel="icon" type="image/x-icon" href="assets/favicon.ico">
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

# Suppress callback exceptions
app.config.suppress_callback_exceptions = True

# Define main app layout
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
            " | © Sergio Cuenca Núñez, December 2024 | Version: 3.1"
        ], style={'text-align': 'center'}),
    ], className="footer")
])

# Validation layout to include all sub-app layouts
app.validation_layout = html.Div([
    forecast_layout,
    home_layout,
    news_layout,
    about_layout,
    terms_layout
])

# Page routing callback
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home_layout
    elif pathname == '/forecast':
        return forecast_layout
    elif pathname == '/about':
        return about_layout
    elif pathname == '/terms':
        return terms_layout
    elif pathname == '/news':
        return news_layout
    else:
        return "404 Page Not Found"

# Register callbacks
forecast_callbacks(app)
news_callbacks(app)

# Main entry point for local development
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run_server(debug = True)
    #app.run_server(host='0.0.0.0', port=port)