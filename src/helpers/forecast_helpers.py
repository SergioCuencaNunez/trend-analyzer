import pandas as pd
import plotly.graph_objs as go
from pandas.tseries.holiday import USFederalHolidayCalendar
from models.xgboost_model import prepare_and_train_model, forecast_with_rolling, forecast_without_rolling
from models.prophet_model import fit_prophet, forecast_prophet


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
