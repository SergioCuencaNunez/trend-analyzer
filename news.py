import requests
from bs4 import BeautifulSoup
from finvizfinance.quote import finvizfinance
from dash import dcc, html, callback_context
import dash_bootstrap_components as dbc
from dash import Input, Output, State
from datetime import datetime
import pandas as pd
from app_instance import app

# Function to fetch the logo of the news source
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

# Function to format dates in the ratings table
def format_ratings_date(ratings_df):
    ratings_df['Date'] = pd.to_datetime(ratings_df['Date']).dt.strftime('%b-%d-%y')
    return ratings_df

# Modified get_stock_ratings function to include date formatting
def get_stock_ratings(ticker):
    stock = finvizfinance(ticker)
    ratings = stock.ticker_outer_ratings()
    formatted_ratings = format_ratings_date(ratings)  # Format date column
    return formatted_ratings

# Function to get news
def get_stock_news(ticker):
    stock = finvizfinance(ticker)
    news_df = stock.ticker_news()
    today = datetime.today().date()
    news_df['Date'] = pd.to_datetime(news_df['Date']).dt.date
    return news_df[news_df['Date'] == today]

# Function to format today's date for the News header
def get_news_header_date():
    today = datetime.today()
    formatted_date = today.strftime("%A, %d %b. %Y")
    return f"News - {formatted_date}"

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

# Helper function to determine color based on financial thresholds
def determine_color(label, value):
    try:
        value = float(value.strip('%'))
        if label == 'P/E':
            if value < 15:
                return 'green'  # Undervalued
            elif value > 25:
                return 'red'    # Overvalued
            else:
                return 'black'  # Neutral
        elif label == 'P/S':
            if value < 1:
                return 'green'
            elif value > 4:
                return 'red'
            else:
                return 'black'
        elif label == 'P/B':
            if value < 1:
                return 'green'
            elif value > 3:
                return 'red'
            else:
                return 'black'
        elif label in ['Debt/Eq', 'LT Debt/Eq']:
            if value < 0.5:
                return 'green'  # Low debt
            elif value > 2:
                return 'red'    # High debt
            else:
                return 'black'
        elif label == 'ROA':
            if value > 5:
                return 'green'  # Good return
            elif value < 0:
                return 'red'    # Negative return
            else:
                return 'black'
        elif label == 'ROI':
            if value > 15:
                return 'green'
            elif value < 0:
                return 'red'
            else:
                return 'black'
        elif label == 'Gross Margin':
            if value > 40:
                return 'green'
            elif value < 20:
                return 'red'
            else:
                return 'black'
        elif label == 'Oper. Margin':
            if value > 15:
                return 'green'
            elif value < 5:
                return 'red'
            else:
                return 'black'
        elif label == 'Profit Margin':
            if value > 10:
                return 'green'
            elif value < 2:
                return 'red'
            else:
                return 'black'
        elif label in ['Perf Week', 'Perf Month', 'Perf Quarter', 'Change']:
            if value > 0:
                return 'green'  # Positive performance
            elif value < 0:
                return 'red'    # Negative performance
            else:
                return 'black'
        elif label in ['Volatility W', 'Volatility M']:
            if value > 5:
                return 'red'    # High volatility
            elif value < 2:
                return 'green'  # Low volatility
            else:
                return 'black'
        elif label == 'Beta':
            if value > 1.5:
                return 'red'    # Highly volatile compared to market
            elif value < 0.8:
                return 'green'  # Less volatile
            else:
                return 'black'
        elif label in ['Target Price', 'Prev Close', 'Price']:
            return 'black'      # Neutral indicators
        else:
            return 'black'
    except ValueError:
        return 'black'

# Function to create the transposed performance data table with styled cells
def display_performance_data(performance_data):
    table = dbc.Table([
        html.Tr([
            html.Td("Index"), html.Td(html.B(performance_data['Index'])),
            html.Td("P/E"), html.Td(html.B(performance_data['P/E'], style={'color': determine_color("P/E", performance_data['P/E'])})),
            html.Td("ROA"), html.Td(html.B(performance_data['ROA'], style={'color': determine_color("ROA", performance_data['ROA'])})),
            html.Td("Perf Week"), html.Td(html.B(performance_data['Perf Week'], style={'color': determine_color("Perf Week", performance_data['Perf Week'])})),
            html.Td("Beta"), html.Td(html.B(performance_data['Beta'], style={'color': determine_color("Beta", performance_data['Beta'])}))
        ]),
        
        html.Tr([
            html.Td("Market Cap"), html.Td(html.B(performance_data['Market Cap'])),
            html.Td("P/S"), html.Td(html.B(performance_data['P/S'], style={'color': determine_color("P/S", performance_data['P/S'])})),
            html.Td("ROI"), html.Td(html.B(performance_data['ROI'], style={'color': determine_color("ROI", performance_data['ROI'])})),
            html.Td("Perf Month"), html.Td(html.B(performance_data['Perf Month'], style={'color': determine_color("Perf Month", performance_data['Perf Month'])})),
            html.Td("Target Price"), html.Td(html.B(performance_data['Target Price']))
        ]),
        
        html.Tr([
            html.Td("Income"), html.Td(html.B(performance_data['Income'])),
            html.Td("P/B"), html.Td(html.B(performance_data['P/B'], style={'color': determine_color("P/B", performance_data['P/B'])})),
            html.Td("Gross Margin"), html.Td(html.B(performance_data['Gross Margin'], style={'color': determine_color("Gross Margin", performance_data['Gross Margin'])})),
            html.Td("Perf Quarter"), html.Td(html.B(performance_data['Perf Quarter'], style={'color': determine_color("Perf Quarter", performance_data['Perf Quarter'])})),
            html.Td("Prev Close"), html.Td(html.B(performance_data['Prev Close']))
        ]),
        
        html.Tr([
            html.Td("Sales"), html.Td(html.B(performance_data['Sales'])),
            html.Td("Debt/Eq"), html.Td(html.B(performance_data['Debt/Eq'], style={'color': determine_color("Debt/Eq", performance_data['Debt/Eq'])})),
            html.Td("Oper. Margin"), html.Td(html.B(performance_data['Oper. Margin'], style={'color': determine_color("Oper. Margin", performance_data['Oper. Margin'])})),
            html.Td("Volatility M"), html.Td(html.B(performance_data['Volatility M'], style={'color': determine_color("Volatility M", performance_data['Volatility M'])})),
            html.Td("Price"), html.Td(html.B(performance_data['Price']))
        ]),
        
        html.Tr([
            html.Td("Volume"), html.Td(html.B(performance_data['Volume'])),
            html.Td("LT Debt/Eq"), html.Td(html.B(performance_data['LT Debt/Eq'], style={'color': determine_color("LT Debt/Eq", performance_data['LT Debt/Eq'])})),
            html.Td("Profit Margin"), html.Td(html.B(performance_data['Profit Margin'], style={'color': determine_color("Profit Margin", performance_data['Profit Margin'])})),
            html.Td("Volatility W"), html.Td(html.B(performance_data['Volatility W'], style={'color': determine_color("Volatility W", performance_data['Volatility W'])})),
            html.Td("Change"), html.Td(html.B(performance_data['Change'], style={'color': determine_color("Change", performance_data['Change'])}))
        ]),
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
                                    'width': 'auto',
                                    'max-width': '140px',
                                    'max-height': '30px',
                                    'padding-left': '10px',
                                    'object-fit': 'contain',
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

# Layout with dcc.Store to keep track of the click count
layout = dbc.Container([
    html.H1("Stock News & Performance", className='fade-in-element', style={'text-align': 'center', 'margin-top': '40px', 'font-family': 'Prata'}),
    dcc.Store(id='clicks-store', data=1),  # Store for tracking clicks
    dbc.Row(
        justify="center",  # Center align the row
        children=[
            dbc.Col(
            html.H4('Select Stock', className='fade-in-element', style={'margin-right': '10px', 'text-align': 'center'}),
            width="auto",  # Width auto to fit content
            className="d-flex align-items-center"  # Center vertically
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
                style={'margin-bottom': '20px'}  # Adjust width as needed
            ),
            width=4
            )
        ],
        className="mb-3"  # Margin bottom for spacing
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
                        dbc.Row(
                            dbc.Col(
                                dbc.Button("Load More", id='load-more-button', color="primary", className='fade-in-card'),
                                width="auto",
                                style={'display': 'flex', 'justify-content': 'center'}
                            ),
                            className="mb-4 justify-content-center"  # Margin bottom for spacing and center alignment
                        ),
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

@app.callback(
    Output('clicks-store', 'data'),
    [Input('stock-dropdown', 'value'), Input('load-more-button', 'n_clicks')],
    [State('clicks-store', 'data')]
)
def update_click_count(selected_stock, n_clicks, clicks_data):
    # Reset to 1 if the stock changes or initialize with 1 for the first load
    if callback_context.triggered[0]['prop_id'] == 'stock-dropdown.value':
        return 1
    elif n_clicks:
        return clicks_data + 1
    return clicks_data

# Main callback
@app.callback(
    [Output('performance-table', 'children'),
     Output('news-cards-row', 'children'),
     Output('ratings-table', 'children'),
     Output('info-title', 'style'),
     Output('news-title', 'children'),  # Updated to Output the header text
     Output('ratings-title', 'style')],
    [Input('stock-dropdown', 'value'), Input('clicks-store', 'data')]
)
def update_stock_info(ticker, clicks_data):
    news_df = get_stock_news(ticker)
    news_limit = 4 * clicks_data  # Display news based on click count
    
    news_cards = [dbc.Col(generate_news_card(news), width=6) for _, news in news_df.head(news_limit).iterrows()]
    
    performance_table = display_performance_data(get_stock_performance_data(ticker))
    ratings_table = dbc.Table.from_dataframe(get_stock_ratings(ticker), striped=True, bordered=True, hover=True, responsive=True, className='fade-in-element')
    
    # Format the header text for News with today's date
    news_title_text = get_news_header_date()
    show_style = {'display': 'block'}
    
    return performance_table, news_cards, ratings_table, show_style, news_title_text, show_style
