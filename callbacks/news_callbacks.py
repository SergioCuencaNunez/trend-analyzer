from dash import Input, Output, State, callback_context, html
import dash_bootstrap_components as dbc
from datetime import datetime
from helpers.news_helpers import (
    get_stock_news,
    get_stock_performance_data,
    get_stock_ratings,
    display_ratings_table,
    display_performance_data,
    generate_news_card
)

def register_callbacks(app):
    # Store callback for click count
    @app.callback(
        Output('clicks-store', 'data'),
        [Input('stock-dropdown', 'value'), Input('load-more-button', 'n_clicks')],
        [State('clicks-store', 'data')]
    )
    def update_click_count(selected_stock, n_clicks, clicks_data):
        if callback_context.triggered[0]['prop_id'] == 'stock-dropdown.value':
            return 1
        elif n_clicks:
            return clicks_data + 1
        return clicks_data

    # Main callback to update content
    @app.callback(
        [
            Output('performance-table', 'children'),
            Output('news-cards-row', 'children'),
            Output('info-title', 'style'),
            Output('news-title', 'style'),
            Output('ratings-table', 'children'),
            Output('ratings-title', 'style'),
            Output('load-more-ratings-button', 'n_clicks'),
            Output('load-more-ratings-button', 'style'),
            Output('load-more-button', 'style')
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

        # Get news data
        news_df, total_news = get_stock_news(ticker)
        news_limit = 4 * clicks_data
        displayed_news = news_df.head(news_limit)
        news_cards = [dbc.Col(generate_news_card(news), width=6) for _, news in displayed_news.iterrows()]

        if len(displayed_news) >= total_news:
            news_cards.append(
                dbc.Col(
                    html.P(f"No More News for {datetime.today().strftime('%A, %d %b. %Y')}",
                           style={'text-align': 'center'}),
                    width=12
                )
            )
            news_button_style = {'display': 'none'}
        else:
            news_button_style = {'display': 'block'}

        # Get performance data
        performance_table = display_performance_data(get_stock_performance_data(ticker))

        # Get ratings data
        ratings_df, total_ratings = get_stock_ratings(ticker, limit=ratings_limit)
        ratings_table = display_ratings_table(ratings_df)

        # Determine ratings button visibility
        ratings_button_style = {'display': 'block'} if len(ratings_df) < total_ratings else {'display': 'none'}

        show_style = {'display': 'block'}

        return (
            performance_table, 
            news_cards,
            show_style, 
            show_style, 
            ratings_table, 
            show_style, 
            load_more_ratings_clicks, 
            ratings_button_style, 
            news_button_style
        )
