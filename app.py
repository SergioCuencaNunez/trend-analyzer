from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app_instance import app
import forecast  # Import forecast after app is created
import home  # Import home after app is created
import about  # Import about after app is created
import terms  # Import terms after app is created

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
                            dbc.NavItem(dcc.Link('ABOUT', href='/about', className='nav-link', style={'margin-right': '20px'})),
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
            " | Sergio Cuenca Núñez, June 2024 | Version: 1.0"
        ], style={'text-align': 'center'}),
    ], className="footer")
])

# Validation layout to include all sub-apps' layouts
app.validation_layout = html.Div([
    forecast.layout,
    home.layout,
    about.layout,
    terms.layout
])

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == '/forecast':
        return forecast.layout
    elif pathname == '/about':
        return about.layout
    elif pathname == '/terms':
        return terms.layout
    else:
        return "404 Page Not Found"

if __name__ == '__main__':
    app.run_server()
