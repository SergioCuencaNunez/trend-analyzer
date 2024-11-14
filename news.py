import requests
from bs4 import BeautifulSoup
from finvizfinance.quote import finvizfinance
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash import Input, Output, State
from datetime import datetime
import pandas as pd
from app_instance import app

def fetch_news_logo(news_link):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(news_link, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src', '')
            alt = img_tag.get('alt', '')
            if "https://s.yimg.com/ny/api/res" in src and alt:  
                return src
        
        return "default_logo.png"
    except Exception as e:
        print(f"Error fetching logo: {e}")
        return "default_logo.png"

# Function to get ratings
def get_stock_ratings(ticker):
    stock = finvizfinance(ticker)
    ratings = stock.ticker_outer_ratings()
    return ratings

# Function to get news
def get_stock_news(ticker):
    stock = finvizfinance(ticker)
    news_df = stock.ticker_news()
    today = datetime.today().date()
    news_df['Date'] = pd.to_datetime(news_df['Date']).dt.date
    return news_df[news_df['Date'] == today]

# Function to get stock performance data
def get_stock_performance_data(ticker):
    stock = finvizfinance(ticker)
    snapshot = stock.ticker_fundament()
    performance_data = {
        'Index': snapshot.get('Index', 'N/A'),
        'Market Cap': snapshot.get('Market Cap', 'N/A'),
        'Income': snapshot.get('Income', 'N/A'),
        'Sales': snapshot.get('Sales', 'N/A'),
        'Volume': snapshot.get('Volume', 'N/A'),
        'P/E': snapshot.get('P/E', 'N/A'),
        'P/S': snapshot.get('P/S', 'N/A'),
        'P/B': snapshot.get('P/B', 'N/A'),
        'Debt/Eq': snapshot.get('Debt/Eq', 'N/A'),
        'LT Debt/Eq': snapshot.get('LT Debt/Eq', 'N/A'),
        'ROA': snapshot.get('ROA', 'N/A'),
        'ROI': snapshot.get('ROI', 'N/A'),
        'Gross Margin': snapshot.get('Gross Margin', 'N/A'),
        'Oper. Margin': snapshot.get('Oper. Margin', 'N/A'),
        'Profit Margin': snapshot.get('Profit Margin', 'N/A'),
        'Perf Week': snapshot.get('Perf Week', 'N/A'),
        'Perf Month': snapshot.get('Perf Month', 'N/A'),
        'Perf Quarter': snapshot.get('Perf Quarter', 'N/A'),
        'Volatility W': snapshot.get('Volatility W', 'N/A'),
        'Volatility M': snapshot.get('Volatility M', 'N/A'),
        'Beta': snapshot.get('Beta', 'N/A'),
        'Target Price': snapshot.get('Target Price', 'N/A'),
        'Prev Close': snapshot.get('Prev Close', 'N/A'),
        'Price': snapshot.get('Price', 'N/A'),
        'Change': snapshot.get('Change', 'N/A')
    }
    return performance_data

# Function to create the performance data table
def display_performance_data(performance_data):
    table = dbc.Table([
        html.Tr([html.Td("Index"), html.Td(performance_data['Index']),
                 html.Td("Market Cap"), html.Td(performance_data['Market Cap']),
                 html.Td("Income"), html.Td(performance_data['Income']),
                 html.Td("Sales"), html.Td(performance_data['Sales']),
                 html.Td("Volume"), html.Td(performance_data['Volume'])]),
        html.Tr([html.Td("P/E"), html.Td(performance_data['P/E']),
                 html.Td("P/S"), html.Td(performance_data['P/S']),
                 html.Td("P/B"), html.Td(performance_data['P/B']),
                 html.Td("Debt/Eq"), html.Td(performance_data['Debt/Eq']),
                 html.Td("LT Debt/Eq"), html.Td(performance_data['LT Debt/Eq'])]),
        html.Tr([html.Td("ROA"), html.Td(performance_data['ROA']),
                 html.Td("ROI"), html.Td(performance_data['ROI']),
                 html.Td("Gross Margin"), html.Td(performance_data['Gross Margin']),
                 html.Td("Oper. Margin"), html.Td(performance_data['Oper. Margin']),
                 html.Td("Profit Margin"), html.Td(performance_data['Profit Margin'])]),
        html.Tr([html.Td("Perf Week"), html.Td(performance_data['Perf Week']),
                 html.Td("Perf Month"), html.Td(performance_data['Perf Month']),
                 html.Td("Perf Quarter"), html.Td(performance_data['Perf Quarter']),
                 html.Td("Volatility W"), html.Td(performance_data['Volatility W']),
                 html.Td("Volatility M"), html.Td(performance_data['Volatility M'])]),
        html.Tr([html.Td("Beta"), html.Td(performance_data['Beta']),
                 html.Td("Target Price"), html.Td(performance_data['Target Price']),
                 html.Td("Prev Close"), html.Td(performance_data['Prev Close']),
                 html.Td("Price"), html.Td(performance_data['Price']),
                 html.Td("Change"), html.Td(performance_data['Change'])]),
    ], bordered=True, striped=True, hover=True, responsive=True, className='fade-in-element')
    return table

# Function to generate news card with logos
def generate_news_card(news_item):
    logo_url = fetch_news_logo(news_item['Link'])
    return dbc.Card(
        [
            dbc.CardHeader(
                dbc.Row(
                    [
                        dbc.Col(
                            html.H4(
                                news_item['Title'],
                                style={
                                    'font-size': '16px',
                                    'font-weight': 'bold',
                                    'margin': '0'
                                }
                            ),
                            width=True
                        ),
                        dbc.Col(
                            dbc.CardImg(
                                src=logo_url,
                                style={
                                    'width': '75px',
                                    'height': 'auto',
                                    'padding-left': '10px',
                                    'overflow': 'visible'
                                }
                            ),
                            width="auto",
                            className="d-flex align-items-center justify-content-end"
                        )
                    ],
                    align="center",
                    className="g-0"
                ),
                style={
                    'padding': '10px 20px'
                }
            ),
            dbc.CardBody([
                html.P(
                    f"Source: {news_item['Source']}",
                    style={
                        'font-size': '14px',
                        'color': '#555'
                    }
                ),
                dcc.Link(
                    "Link to Full Story",
                    href=news_item['Link'],
                    target="_blank",
                    style={
                        'font-size': '14px',
                        'color': '#007bff'
                    }
                )
            ])
        ],
        style={
            'position': 'relative',
            'height': '100%'
        },
        className='fade-in-card'
    )

# Layout
layout = dbc.Container([
    html.H1("Stock News & Performance", className='fade-in-element', style={'text-align': 'center', 'margin-top': '40px', 'font-family': 'Prata'}),
    dbc.Row([
        dbc.Col([
            html.H4('Select Stock', className='fade-in-element', style={'margin': '20px 0', 'text-align': 'center'}),
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
            )
        ], width=4)
    ]),
    dbc.Row(
        dbc.Col(
            dcc.Loading(
                id="loading-full-content",
                type="default",
                children=html.Div(
                    id='data-content',
                    children=[
                        dbc.Row([
                            dbc.Col(html.H2("Relevant Information", id='info-title', className='fade-in-text', style={'text-align': 'center', 'font-family': 'Prata', 'display': 'none'}), width=12, style={'text-align': 'center'}),
                        ]),
                        dbc.Row([
                            dbc.Col(html.Div(id='performance-table', className='fade-in-element'), width=12)
                        ], style={'margin-bottom': '20px'}),
                        dbc.Row([
                            dbc.Col(html.H2("News", id='news-title', className='fade-in-text', style={'text-align': 'center', 'font-family': 'Prata', 'display': 'none'}), width=12, style={'text-align': 'center'}),
                        ]),
                        dbc.Row(
                            id='news-cards-row', 
                            className="g-3 fade-in-element", 
                            style={'margin-bottom': '20px'}
                        ),
                        dbc.Row([
                            dbc.Col(dbc.Button("Load More", id='load-more-button', color="primary"), width="auto", style={'text-align': 'center', 'display': 'flex', 'justify-content': 'center'}),
                        ]),
                        dbc.Row([
                            dbc.Col(html.H2("Ratings", id='ratings-title', className='fade-in-text', style={'text-align': 'center', 'font-family': 'Prata', 'display': 'none'}), width=12, style={'text-align': 'center'}),
                        ]),
                        dbc.Row([
                            dbc.Col(html.Div(id='ratings-table', className='fade-in-element'), width=12)
                        ])
                    ],
                    style={'min-height': '600px'}
                )
            )
        )
    )
], fluid=True, className="container")

# Updated callback to control visibility of titles and load more news
@app.callback(
    [Output('performance-table', 'children'),
     Output('news-cards-row', 'children'),
     Output('ratings-table', 'children'),
     Output('info-title', 'style'),
     Output('news-title', 'style'),
     Output('ratings-title', 'style')],
    [Input('stock-dropdown', 'value'), Input('load-more-button', 'n_clicks')],
    [State('news-cards-row', 'children')]
)
def update_stock_info(ticker, n_clicks, current_news):
    news_df = get_stock_news(ticker)
    if not n_clicks:
        n_clicks = 1  # Initialize with one load
    
    news_limit = 4 * n_clicks  # Increment by 4 on each click
    news_cards = [dbc.Col(generate_news_card(news), width=6) for _, news in news_df.head(news_limit).iterrows()]
    
    performance_table = display_performance_data(get_stock_performance_data(ticker))
    ratings_table = dbc.Table.from_dataframe(get_stock_ratings(ticker), striped=True, bordered=True, hover=True, responsive=True, className='fade-in-element')
    show_style = {'display': 'block'}
    
    return performance_table, news_cards, ratings_table, show_style, show_style, show_style
