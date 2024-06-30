import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "TrendAnalyzer"
app._favicon = 'favicon.ico'  # Referencia al favicon

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
