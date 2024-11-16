import requests
from bs4 import BeautifulSoup
from finvizfinance.quote import finvizfinance
from dash import dcc, html, callback_context
import dash_bootstrap_components as dbc
from dash import Input, Output, State
from datetime import datetime
import pandas as pd
from app_instance import app
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Dictionary to store cached logos
logo_cache = {}

# Function to fetch the logo of the news source with caching
def fetch_news_logo(news_link):
    # Check if the logo for this link is already cached
    if news_link in logo_cache:
        return logo_cache[news_link]
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Check if the domain is Investopedia
        if "investopedia.com" in news_link:
            logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Investopedia_Logo.svg/1150px-Investopedia_Logo.svg.png?20190418033219"
            logo_cache[news_link] = logo_url  # Cache the logo
            return logo_url

        # Fetch the page content for other domains
        response = requests.get(news_link, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # General logic to find images
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src', '')
            alt = img_tag.get('alt', '')

            # Specific condition for Yahoo Finance
            if "https://s.yimg.com/ny/api/res" in src and alt:
                logo_url = src
                logo_cache[news_link] = logo_url  # Cache the logo
                return logo_url
            
            # Check for 'logo' in any attribute
            attributes = img_tag.attrs
            if any("logo" in str(value).lower() for value in attributes.values()):
                # Convert relative URL to absolute
                logo_url = urljoin(news_link, src)
                logo_cache[news_link] = logo_url  # Cache the logo
                return logo_url
        
        # Default logo if none is found
        logo_url = "default_logo.png"
        logo_cache[news_link] = logo_url  # Cache the default logo
        return logo_url

    except Exception as e:
        print(f"Error fetching logo: {e}")
        return "default_logo.png"

# Function to get ratings
def get_stock_ratings(ticker, limit=10):
    stock = finvizfinance(ticker)
    ratings = stock.ticker_outer_ratings()
    
    # Keep track of total ratings count
    total_ratings = len(ratings)
    limited_ratings = ratings.head(limit)
    limited_ratings['Date'] = pd.to_datetime(limited_ratings['Date']).dt.strftime('%b-%d-%y')  # Formatting date to 'Nov-04-24'
    
    # Rename columns to custom headers
    limited_ratings.columns = ["Date", "Action", "Analyst", "Rating Change", "Price Target Change"]
    
    return limited_ratings, total_ratings

# Function to create the styled ratings table
def display_ratings_table(ratings_df):
    table_rows = []

    for _, row in ratings_df.iterrows():
        action_style = {
            'display': 'inline-block',
            'padding': '2px 4px',
            'border-radius': '5px'
        }

        if row['Action'] == 'Downgrade':
            action_style['background-color'] = 'rgba(255, 0, 0, 0.2)'
            color = 'red'
        elif row['Action'] == 'Upgrade':
            action_style['background-color'] = 'rgba(0, 128, 0, 0.2)'
            color = 'green'
        else:
            action_style['background-color'] = 'transparent'
            color = 'black'

        table_rows.append(
            html.Tr([
                html.Td(row['Date']),
                html.Td(html.Span(row['Action'], style=action_style)),
                html.Td(row['Analyst'], style={'color': color}),
                html.Td(row['Rating Change'], style={'color': color}),
                html.Td(row['Price Target Change'], style={'color': color})
            ])
        )

    # Create the table without bordered=True and apply custom CSS for a unified border
    table = dbc.Table([
        html.Thead(
            html.Tr([
                html.Th("Date"),
                html.Th("Action"),
                html.Th("Analyst"),
                html.Th("Rating Change"),
                html.Th("Price Target Change")
            ])
        ),
        html.Tbody(table_rows)
    ], striped=True, hover=True, responsive=True, className='custom-table')

    # Wrap in a card for the outer rounded border and fade-in effect
    table_card = dbc.Card(
        table,
        className='fade-in-table',  # Apply fade-in effect to the outer card for border and content
        style={
            'border-radius': '8px',  # Outer rounded corners
            'overflow': 'hidden'  # Ensures rounded corners are applied
        }
    )

    return table_card

# Function to get news
def get_stock_news(ticker):
    stock = finvizfinance(ticker)
    news_df = stock.ticker_news()
    news_df['Date'] = pd.to_datetime(news_df['Date']).dt.strftime('%b-%d-%Y')  # Format date for display
    total_news = len(news_df)  # Get the total count of news articles
    return news_df, total_news

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
    
    # Define the main components of the card header row
    header_components = [
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
        )
    ]
    
    # Add the logo only if it is not the default logo
    if logo_url != "default_logo.png":
        header_components.append(
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
        )
    
    # Construct the card with conditionally added logo
    return dbc.Card(
        [
            dbc.CardHeader(
                dbc.Row(
                    header_components,
                    align="center",
                    className="g-0"
                ),
                style={
                    'padding': '10px 20px'
                }
            ),
            dbc.CardBody(
                [
                    html.P(
                        f"Source: {news_item['Source']}",
                        style={
                            'font-size': '14px',
                            'color': '#555',
                            'margin': '0',
                            'padding-bottom': '5px'
                        }
                    ),
                    html.P(
                        f"Date: {news_item['Date']}",
                        style={
                            'font-size': '12px',
                            'color': '#888',
                            'margin': '0',
                            'padding-bottom': '12px'
                        }
                    ),
                    dcc.Link(
                        "Link to Full Story",
                        href=news_item['Link'],
                        target="_blank",
                        style={
                            'font-size': '14px',
                            'color': '#007bff',
                            'margin': '0',
                            'padding-bottom': '5px'
                        }
                    )
                ],
                style={
                    'display': 'flex',
                    'flex-direction': 'column',
                    'justify-content': 'center',
                    'height': '100%'
                }
            )
        ],
        style={
            'position': 'relative',
            'height': '100%'
        },
        className='fade-in-card'
    )

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
                                dbc.Button("Load More News", id='load-more-button', color="primary", style={'display': 'block'}),
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
                                        dbc.Button("Load More Ratings", id='load-more-ratings-button', color="primary", style={'display': 'block'}),
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

# Main callback to update content based on click count
@app.callback(
    [
        Output('performance-table', 'children'),
        Output('news-cards-row', 'children'),  # Single Output for news-cards-row
        Output('info-title', 'style'),
        Output('news-title', 'style'),
        Output('ratings-table', 'children'),
        Output('ratings-title', 'style'),
        Output('load-more-ratings-button', 'n_clicks'),
        Output('load-more-ratings-button', 'style'),  # Ratings button visibility
        Output('load-more-button', 'style')  # News button visibility
    ],
    [
        Input('stock-dropdown', 'value'),
        Input('clicks-store', 'data'),
        Input('load-more-ratings-button', 'n_clicks'),
        Input('load-more-button', 'n_clicks')
    ],
    [
        State('load-more-ratings-button', 'n_clicks'),
        State('clicks-store', 'data')
    ]
)
def update_news_performance_and_ratings(
    ticker, clicks_data, load_more_ratings_clicks, load_more_news_clicks, prev_ratings_clicks, prev_clicks_store
):
    # Check if stock selection changed by comparing with callback context
    if callback_context.triggered[0]['prop_id'] == 'stock-dropdown.value':
        ratings_limit = 10
        load_more_ratings_clicks = 0
    else:
        ratings_limit = None if load_more_ratings_clicks else 10

    # Get news data and limit based on clicks
    news_df, total_news = get_stock_news(ticker)
    news_limit = 4 * clicks_data  # Display news based on click count
    displayed_news = news_df.head(news_limit)
    news_cards = [dbc.Col(generate_news_card(news), width=6) for _, news in displayed_news.iterrows()]

    # Add message if no more news
    if len(displayed_news) >= total_news:
        news_cards.append(
            dbc.Col(
                html.P(f"No More News for {datetime.today().strftime('%A, %d %b. %Y')}",
                       style={'text-align': 'center'}),
                width=12
            )
        )
        news_button_style = {'display': 'none'}  # Hide the button
    else:
        news_button_style = {'display': 'block'}  # Show the button

    # Get performance data
    performance_table = display_performance_data(get_stock_performance_data(ticker))

    # Get ratings data with the appropriate limit
    ratings_df, total_ratings = get_stock_ratings(ticker, limit=ratings_limit)
    ratings_table = display_ratings_table(ratings_df)

    # Determine if the ratings button should be shown
    ratings_button_style = {'display': 'block'} if len(ratings_df) < total_ratings else {'display': 'none'}

    # Set styles to show all elements
    show_style = {'display': 'block'}

    return (
        performance_table, 
        news_cards,  # Combined logic for news-cards-row
        show_style, 
        show_style, 
        ratings_table, 
        show_style, 
        load_more_ratings_clicks, 
        ratings_button_style, 
        news_button_style
    )
