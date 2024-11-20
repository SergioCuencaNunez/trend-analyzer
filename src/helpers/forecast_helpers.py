import pandas as pd
import yfinance as yf
import numpy as np
from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from pandas.tseries.holiday import USFederalHolidayCalendar
from models.xgboost_model import prepare_and_train_model, forecast_with_rolling, forecast_without_rolling
from models.prophet_model import fit_prophet, forecast_prophet

def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    info = stock.info
    return hist, info

def calculate_metrics(stock_data, stock_info):
    stock_data['MA20'] = stock_data['Close'].rolling(window=20).mean()
    stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()

    stock_data['Returns'] = stock_data['Close'].pct_change()
    stock_data['Volatility'] = stock_data['Returns'].rolling(window=20).std() * np.sqrt(252)

    current_price = stock_info.get('currentPrice', None)
    shares_outstanding = stock_info.get('sharesOutstanding', None)
    if current_price and shares_outstanding:
        current_market_cap = current_price * shares_outstanding
    else:
        current_market_cap = None

    current_volume = stock_data['Volume'].iloc[-1] if len(stock_data) >=1 else None
    current_avg_volume = stock_data['Volume'].rolling(window=20).mean().iloc[-1] if len(stock_data) >= 20 else None

    target_high_price = stock_info.get('targetHighPrice', None)
    target_low_price = stock_info.get('targetLowPrice', None)

    def get_past_value(series, days_ago):
        if len(series) >= days_ago + 1:
            return series.iloc[-days_ago -1]
        else:
            return None

    def calculate_trend(current_value, past_value):
        if current_value and past_value:
            change = current_value - past_value
            percent_change = (change / past_value) * 100
            trend_symbol = '↑' if change > 0 else '↓' if change < 0 else ''
            trend = f"{trend_symbol} {abs(percent_change):.2f}%"
        else:
            trend = 'N/A'
        return trend

    past_price_week = get_past_value(stock_data['Close'], 5)
    past_price_month = get_past_value(stock_data['Close'], 21)
    if past_price_week and shares_outstanding:
        past_market_cap_week = past_price_week * shares_outstanding
    else:
        past_market_cap_week = None
    if past_price_month and shares_outstanding:
        past_market_cap_month = past_price_month * shares_outstanding
    else:
        past_market_cap_month = None

    market_cap_trend_week = calculate_trend(current_market_cap, past_market_cap_week)
    market_cap_trend_month = calculate_trend(current_market_cap, past_market_cap_month)

    # Volume trends
    past_volume_week = get_past_value(stock_data['Volume'], 5)
    past_volume_month = get_past_value(stock_data['Volume'], 21)

    volume_trend_week = calculate_trend(current_volume, past_volume_week)
    volume_trend_month = calculate_trend(current_volume, past_volume_month)

    # Average Volume trends
    avg_volume_series = stock_data['Volume'].rolling(window=20).mean()
    past_avg_volume_week = get_past_value(avg_volume_series, 5)
    past_avg_volume_month = get_past_value(avg_volume_series, 21)

    avg_volume_trend_week = calculate_trend(current_avg_volume, past_avg_volume_week)
    avg_volume_trend_month = calculate_trend(current_avg_volume, past_avg_volume_month)

    # Compile Metrics
    metrics = [
        {
            "title": "Market Cap",
            "value": f"${current_market_cap / 1e9:,.2f}B" if current_market_cap else 'N/A',
            "trend_week": market_cap_trend_week,
            "trend_month": market_cap_trend_month
        },
        {
            "title": "Volume",
            "value": f"{current_volume:,}" if current_volume else 'N/A',
            "trend_week": volume_trend_week,
            "trend_month": volume_trend_month
        },
        {
            "title": "Average Volume",
            "value": f"{int(current_avg_volume):,}" if current_avg_volume else 'N/A',
            "trend_week": avg_volume_trend_week,
            "trend_month": avg_volume_trend_month
        },
        {
            "title": "Prices",
            "values": {
                "Current Price": f"${current_price:,.2f}" if current_price else 'N/A',
                "Target Low Price": f"${target_low_price:,.2f}" if target_low_price else 'N/A',
                "Target High Price": f"${target_high_price:,.2f}" if target_high_price else 'N/A',
            }
        }
    ]
    return metrics

def create_metrics_card(metric):
    if "values" in metric:
        content = [
            html.H5(
                metric["title"],
                className="card-title",
                style={"text-align": "center", "margin": "5px 0"} 
            ),
        ]
        for key, value in metric["values"].items():
            value_color = ""
            if key == "Target Low Price":
                value_color = "red"
            elif key == "Target High Price":
                value_color = "green"
            content.append(
                html.P(
                    [
                        html.Span(f"{key}: ", style={"color": "black", "margin-right": "1px"}),
                        html.Span(value, style={"color": value_color}),
                    ],
                    style={
                        "margin": "1px 0",
                        "text-align": "center",
                    }
                )
            )

        card_body = dbc.CardBody(
            content,
            style={
                "display": "flex",
                "flex-direction": "column",
                "justify-content": "center",
                "align-items": "center",
                "height": "100%",
            }
        )
    else:
        card_content = [
            html.H5(
                metric["title"],
                className="card-title",
                style={"text-align": "center", "margin": "5px 0"}
            ),
            html.H4(
                metric["value"],
                className="card-text",
                style={"text-align": "center", "margin": "5px 0"}
            ),
        ]
        if "trend_week" in metric and "trend_month" in metric:
            trend_week_color = (
                "green" if "↑" in metric["trend_week"] else "red" if "↓" in metric["trend_week"] else "black"
            )
            trend_month_color = (
                "green" if "↑" in metric["trend_month"] else "red" if "↓" in metric["trend_month"] else "black"
            )
            card_content.extend([
                html.P(
                    [
                        html.Span("Last Week: ", style={"color": "black", "margin-right": "1px"}),
                        html.Span(metric["trend_week"], style={"color": trend_week_color}),
                    ],
                    style={
                        "margin": "1px 0",
                        "text-align": "center",
                    }
                ),
                html.P(
                    [
                        html.Span("Last Month: ", style={"color": "black", "margin-right": "1px"}),
                        html.Span(metric["trend_month"], style={"color": trend_month_color}),
                    ],
                    style={
                        "margin": "1px 0",
                        "text-align": "center",
                    }
                )
            ])

        card_body = dbc.CardBody(
            card_content,
            style={
                "display": "flex",
                "flex-direction": "column",
                "justify-content": "center",
                "align-items": "center",
                "height": "100%",
            }
        )
    
    return dbc.Col(
        dbc.Card(
            card_body,
            style={
                "border-radius": "10px",
                "height": "100%",
                "justify-content": "center",
                "align-items": "center",
            },
            className="fade-in-card"
        ),
        width=3
    )

def create_growth_bar(growth_metrics):
    labels = ['Rev Gr (YoY)', 'Earn Gr (YoY)', 'Rev Gr (QoQ)', 'Earn Gr (QoQ)']
    values = list(growth_metrics.values())

    return go.Figure(data=[
        go.Bar(
            x=labels,
            y=values,
            marker=dict(color='blue'),
            hovertemplate='%{x}: %{y:.2f}%',
            name='Growth Metrics'
        )
    ]).update_layout(
        title={
            'text': 'Growth Analysis (%)',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'family': 'Prata', 'color': '#050A30'}
        },
        xaxis={
            'title': 'Metrics',
            'titlefont': {'family': 'Hanken Grotesk', 'color': '#050A30'},
            'tickfont': {'family': 'Hanken Grotesk'},
            'showgrid': True,
            'gridcolor': 'LightGray',
            'gridwidth': 0.5,
        },
        yaxis={
            'title': 'Growth (%)',
            'titlefont': {'family': 'Hanken Grotesk', 'color': '#050A30'},
            'tickfont': {'family': 'Hanken Grotesk'},
            'showgrid': True,
            'gridcolor': 'LightGray',
            'gridwidth': 0.5,
        },
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'family': 'Hanken Grotesk'},
        height=250,
        margin=dict(l=50, r=50, t=50, b=50)
    )

def create_profitability_bar(profitability_metrics):
    labels = ['Profit Mgn', 'Gross Mgn', 'Oper Mgn', 'ROA', 'ROE']
    values = list(profitability_metrics.values())

    return go.Figure(data=[
        go.Bar(
            x=labels,
            y=values,
            marker=dict(color='red'),
            hovertemplate='%{x}: %{y:.2f}%',
            name='Profitability Metrics'
        )
    ]).update_layout(
        title={
            'text': 'Profitability Analysis (%)',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'family': 'Prata', 'color': '#050A30'}
        },
        xaxis={
            'title': 'Metrics',
            'titlefont': {'family': 'Hanken Grotesk', 'color': '#050A30'},
            'tickfont': {'family': 'Hanken Grotesk'},
            'showgrid': True,
            'gridcolor': 'LightGray',
            'gridwidth': 0.5,
        },
        yaxis={
            'title': 'Percentage (%)',
            'titlefont': {'family': 'Hanken Grotesk', 'color': '#050A30'},
            'tickfont': {'family': 'Hanken Grotesk'},
            'showgrid': True,
            'gridcolor': 'LightGray',
            'gridwidth': 0.5,
        },
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'family': 'Hanken Grotesk'},
        height=250,
        margin=dict(l=50, r=50, t=50, b=50)
    )


def create_volatility_graph(stock_data):
    stock_data['Returns'] = stock_data['Close'].pct_change()
    stock_data['Volatility'] = stock_data['Returns'].rolling(window=20).std() * np.sqrt(252)

    return go.Figure(data=[
        go.Scatter(
            x=stock_data.index,
            y=stock_data['Volatility'],
            line=dict(color='green', width=1.5),
            fill='tozeroy',
            name='Volatility'
        )
    ]).update_layout(
        title={
            'text': 'Volatility',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'family': 'Prata', 'color': '#050A30'}
        },
        yaxis={
            'title': 'Volatility',
            'titlefont': {'family': 'Hanken Grotesk', 'color': '#050A30'},
            'tickfont': {'family': 'Hanken Grotesk'},
            'showgrid': True,
            'gridcolor': 'LightGray',
            'gridwidth': 0.5,
        },
        xaxis={
            'title': 'Date',
            'type': 'date',
            'tickformat': '%b %Y',
            'titlefont': {'family': 'Hanken Grotesk', 'color': '#050A30'},
            'tickfont': {'family': 'Hanken Grotesk'},
            'showgrid': True,
            'gridcolor': 'LightGray',
            'gridwidth': 0.5,
        },
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'family': 'Hanken Grotesk'},
        height=250,
        margin=dict(l=50, r=50, t=50, b=50)
    )

def calculate_moving_averages(data):
    ma50 = data['Close'].rolling(window=50).mean()
    ma200 = data['Close'].rolling(window=200).mean()
    return ma50, ma200

def create_price_figure(data, ma50, ma200, ticker):
    last_price = data['Close'].iloc[-1]
    min_price = max(0, data['Close'].min() * 0.9)
    max_price = data['Close'].max() * 1.1

    return {
        'data': [
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Candlesticks'
            ),
            go.Scatter(
                x=data.index,
                y=ma50,
                mode='lines',
                name='MA 50',
                line=dict(color='blue')
            ),
            go.Scatter(
                x=data.index, 
                y=ma200, 
                mode='lines', 
                name='MA 200',
                line=dict(color='red')
            ),
            go.Scatter(
                x=[data.index[-1]],
                y=[last_price],
                mode='markers+text',
                text=[f'Last {last_price:.2f}'],
                textposition='top right',
                name='Last Price',
                marker=dict(color='green', size=12)
            )
        ],
        'layout': {
            'title': {
                'text': f'Historic Price for {ticker}',
                'font': {'family': 'Prata', 'color': '#050A30'}
            },
            'yaxis': {
                'title': 'Close Price',
                'titlefont': {'family': 'Hanken Grotesk', 'color': '#050A30'},
                'tickfont': {'family': 'Hanken Grotesk'},
                'showgrid': True,
                'gridcolor': 'LightGray',
                'gridwidth': 0.5,
                'range': [min_price, max_price],
                'zeroline': False
            },
            'xaxis': {
                'title': 'Date',
                'type': 'date',
                'tickformat': '%b %Y',
                'tickmode': 'auto',
                'nticks': 20,
                'tickformatstops': [
                    {'dtickrange': [None, 86400000], 'value': '%d %b %Y'},
                    {'dtickrange': [86400000, 604800000], 'value': '%d %b %Y'},
                    {'dtickrange': [604800000, "M1"], 'value': '%d %b %Y'},
                    {'dtickrange': ["M1", "M6"], 'value': '%b %Y'},
                    {'dtickrange': ["M6", None], 'value': '%b %Y'}
                ],
                'rangebreaks': [dict(bounds=["sat", "sun"])],
                'rangeslider': {'visible': False},
                'titlefont': {'family': 'Hanken Grotesk', 'color': '#050A30'},
                'tickfont': {'family': 'Hanken Grotesk'},
                'linewidth': 1,
                'linecolor': 'black'
            },
            'plot_bgcolor': 'white',
            'paper_bgcolor': 'white',
            'font': {'family': 'Hanken Grotesk'},
            'showlegend': True,
            'height': 500,
            'margin': dict(l=50, r=50, t=50, b=50)
        }
    }

def perform_forecast(data, ticker, model_type, forecast_days):
    min_price = max(0, data['Close'].min() * 0.9)
    max_price = data['Close'].max() * 1.1

    if model_type == 'XGBoost':
        train_df, test_df, scaler, best_model, feature_cols, y_test, y_pred_test = prepare_and_train_model(data)

        if ticker in ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'SMCI', 'MSTR']:
            test_predicted, forecast_data = forecast_with_rolling(best_model, train_df, test_df, feature_cols, scaler, forecast_days=forecast_days)
        else:
            test_predicted, forecast_data = forecast_without_rolling(best_model, test_df, scaler, feature_cols, y_test, y_pred_test, forecast_days=forecast_days)
        
        return min_price, max_price, train_df, test_df, test_predicted, forecast_data
    
    elif model_type == 'Prophet':
        model, data_prophet = fit_prophet(data)
        forecast_data = forecast_prophet(model, data_prophet, forecast_days)

        return min_price, max_price, data_prophet, forecast_data

def calculate_recommendations(data, model_type, forecast_data, earnings_percentage):
    today_price = data['Close'].iloc[-1]
    recommended_buy_price = today_price
    buy_date = pd.Timestamp.today().strftime('%B %d, %Y')
    recommended_sell_price = recommended_buy_price * (1 + earnings_percentage / 100)

    cal = USFederalHolidayCalendar()
    holidays = cal.holidays(start=pd.Timestamp.today(), end=forecast_data.index.max()).to_pydatetime()

    if model_type == 'XGBoost':
        future_forecast_data = forecast_data[forecast_data.index >= pd.Timestamp.today()]
        # Remove weekends and holidays
        future_forecast_data = future_forecast_data[~future_forecast_data.index.to_series().dt.weekday.isin([5, 6])]
        future_forecast_data = future_forecast_data[~future_forecast_data.index.isin(holidays)]
        possible_sell = (future_forecast_data >= recommended_sell_price).any()

    elif model_type == 'Prophet':
        future_forecast_data = forecast_data[forecast_data['ds'] >= pd.Timestamp.today()]
        # Remove weekends and holidays
        future_forecast_data = future_forecast_data[~future_forecast_data['ds'].dt.weekday.isin([5, 6])]
        future_forecast_data = future_forecast_data[~future_forecast_data['ds'].isin(holidays)]
        possible_sell = (future_forecast_data['yhat'] >= recommended_sell_price).any()

    if not possible_sell:
        sell_date = "Not possible within forecasted period"
        recommended_sell_price = "N/A"
    else:
        if model_type == 'XGBoost':
            sell_candidates = future_forecast_data[future_forecast_data >= recommended_sell_price]
            sell_date_idx = sell_candidates.index[0] if not sell_candidates.empty else None
        elif model_type == 'Prophet':
            sell_candidates = future_forecast_data[future_forecast_data['yhat'] >= recommended_sell_price]
            sell_date_idx = sell_candidates['ds'].iloc[0] if not sell_candidates.empty else None
        else:
            sell_candidates = future_forecast_data[future_forecast_data[0] >= recommended_sell_price]
            sell_date_idx = sell_candidates.index[0] if not sell_candidates.empty else None

        if sell_date_idx is not None:
            sell_date = sell_date_idx.strftime('%B %d, %Y')
            recommended_sell_price = f"{recommended_sell_price:.2f}"
        else:
            sell_date = "Not possible within forecasted period"
            recommended_sell_price = "N/A"

    return buy_date, recommended_buy_price, sell_date, recommended_sell_price
