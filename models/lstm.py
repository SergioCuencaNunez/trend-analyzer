import os
import pandas as pd
import numpy as np
import pickle
from keras.models import load_model
from statsmodels.tsa.stattools import adfuller

def load_lstm(ticker):
    # Get the directory where this script is located
    script_dir = os.path.dirname(__file__)

    # Construct the full paths to the model and scaler files
    model_path = os.path.join(script_dir, f'{ticker}_lstm_model.h5')
    scaler_path = os.path.join(script_dir, f'{ticker}_scaler.pkl')

    # Load the pre-trained LSTM model
    if os.path.exists(model_path):
        model = load_model(model_path)
    else:
        raise FileNotFoundError(f"Model file not found at {model_path}")

    # Load the scaler
    if os.path.exists(scaler_path):
        with open(scaler_path, 'rb') as f:
            sc = pickle.load(f)
    else:
        raise FileNotFoundError(f"Scaler file not found at {scaler_path}")

    return model, sc

def fit_lstm(data, sc):
    
    def check_stationarity(data, threshold=0.05):
        result = adfuller(data)
        p_value = result[1]
        return p_value < threshold

    def difference_data(data, interval=1):
        diff = []
        for i in range(interval, len(data)):
            diff.append(data[i] - data[i - interval])
        return np.array(diff)

    def create_lagged_features(data, lookback_period):
        df = pd.DataFrame(data)
        columns = [df.shift(i) for i in range(1, lookback_period+1)]
        df_lagged = pd.concat(columns, axis=1)
        df_lagged.columns = ['lag_{}'.format(i) for i in range(1, lookback_period+1)]
        df_lagged.dropna(inplace=True)
        return df_lagged.values

    def preprocess_data(sc, closing_prices, lookback_period, stationary=False):
        if stationary:
            closing_prices = difference_data(closing_prices.flatten())
            closing_prices = closing_prices.reshape(-1, 1)

        scaled_prices = sc.fit_transform(closing_prices)
        
        lagged_features = create_lagged_features(scaled_prices, lookback_period)
        X, y = lagged_features, scaled_prices[lookback_period:]
        
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        return X, y, scaled_prices
    
    lookback_period = 60

    closing_prices = data['Close'].values.reshape(-1, 1)

    # Determine if data is stationary
    stationary = check_stationarity(closing_prices.flatten())

    # Preprocess data
    train_returns, test_returns, scaled_prices = preprocess_data(sc, closing_prices, lookback_period, stationary)

    return closing_prices, train_returns, scaled_prices, stationary, lookback_period


def forecast_lstm(model, sc, closing_prices, train_returns, scaled_prices, stationary, lookback_period, forecast_days=90):
    def inverse_difference(last_ob, value):
        return value + last_ob

    def predict_future(model, sc, lookback_period, scaled_prices, forecast_days):
        future_predictions = []
        last_lookback_period = scaled_prices[-lookback_period:]
        current_input = last_lookback_period.reshape((1, lookback_period, 1))

        for _ in range(forecast_days):
            future_price = model.predict(current_input)
            future_predictions.append(future_price[0, 0])
            current_input = np.append(current_input[:, 1:, :], future_price.reshape(1, 1, 1), axis=1)

        future_predictions = sc.inverse_transform(np.array(future_predictions).reshape(-1, 1))
        return future_predictions

    # Predicting the stock prices
    predicted_stock_price = model.predict(train_returns)
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)

    if stationary:
        # Reconstruct the predicted stock prices if differenced
        predicted_stock_price = np.array([inverse_difference(closing_prices[i], predicted_stock_price[i]) for i in range(len(predicted_stock_price))])

    future_predictions = predict_future(model, sc, lookback_period, scaled_prices, forecast_days)

    if stationary:
        last_ob = closing_prices[-1]
        future_predictions = [inverse_difference(last_ob, future_predictions[i]) for i in range(len(future_predictions))]

    return predicted_stock_price, future_predictions