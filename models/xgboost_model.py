# Import necessary libraries
import pandas as pd
import numpy as np
import yfinance as yf
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV

# Set random seed for reproducibility
np.random.seed(42)

def prepare_and_train_model(data):
    data['EMA_9'] = data['Adj Close'].ewm(span=9, adjust=False).mean().shift(1)
    data['SMA_5'] = data['Adj Close'].rolling(window=5).mean().shift(1)
    data['SMA_10'] = data['Adj Close'].rolling(window=10).mean().shift(1)
    data['SMA_15'] = data['Adj Close'].rolling(window=15).mean().shift(1)
    data['SMA_30'] = data['Adj Close'].rolling(window=30).mean().shift(1)
    data['SMA_50'] = data['Adj Close'].rolling(window=50).mean().shift(1)
    data['Returns'] = data['Adj Close'].pct_change()
    data['Adj Close'] = data['Adj Close'].shift(-1)
    data = data.dropna()

    # Split data into train and test sets
    train_size = int(len(data) * 0.7)
    train_df = data.iloc[:train_size]
    test_df = data.iloc[train_size:]

    # Define features and target
    feature_cols = ['EMA_9', 'SMA_5', 'SMA_10', 'SMA_15', 'SMA_30', 'SMA_50', 'Returns']
    X_train = train_df[feature_cols].fillna(0)
    X_test = test_df[feature_cols].fillna(0)
    y_test = test_df['Adj Close']
    y_train_log = np.log(train_df['Adj Close'])

    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train the model using Grid Search
    param_grid = {
        'n_estimators': [50, 100, 150],
        'learning_rate': [0.01, 0.05, 0.1],
        'max_depth': [3, 5, 7],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0],
        'gamma': [0, 0.1, 0.2],
        'min_child_weight': [1, 5, 10]
    }
    xgb_model = xgb.XGBRegressor(objective='reg:squarederror')
    grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid, 
                               scoring='neg_mean_squared_error', cv=3, verbose=1, n_jobs=-1)
    grid_search.fit(X_train_scaled, y_train_log)

    # Get the best model
    best_model = grid_search.best_estimator_

    y_pred_log_xgb = best_model.predict(X_test_scaled)

    # Transform Predictions Back to Original Scale
    y_pred_test = np.exp(y_pred_log_xgb)

    return train_df, test_df, scaler, best_model, feature_cols, y_test, y_pred_test

def forecast_without_rolling(best_model, test_df, scaler, feature_cols, y_test, y_pred_test, forecast_days=30):
    forecast_input = test_df.copy()
    forecast_df = pd.DataFrame(columns=test_df.columns)
    
    for i in range(forecast_days):
        last_date = forecast_input.index[-1]
        next_date = last_date + pd.offsets.BDay(1)
        
        ema_9 = forecast_input['Adj Close'].ewm(span=9, adjust=False).mean().iloc[-1]
        sma_5 = forecast_input['Adj Close'].rolling(window=5).mean().iloc[-1]
        sma_10 = forecast_input['Adj Close'].rolling(window=10).mean().iloc[-1]
        sma_15 = forecast_input['Adj Close'].rolling(window=15).mean().iloc[-1]
        sma_30 = forecast_input['Adj Close'].rolling(window=30).mean().iloc[-1]
        sma_50 = forecast_input['Adj Close'].rolling(window=50).mean().iloc[-1]
        returns = forecast_input['Returns'].iloc[-1]
        
        feature_row = {
            'EMA_9': ema_9, 'SMA_5': sma_5, 'SMA_10': sma_10,
            'SMA_15': sma_15, 'SMA_30': sma_30, 'SMA_50': sma_50, 'Returns': returns
        }
        
        input_features = pd.DataFrame([feature_row], index=[next_date], columns=feature_cols)
        input_scaled = scaler.transform(input_features.fillna(0))
        
        pred_log_xgb = best_model.predict(input_scaled)
        predicted_close = np.exp(pred_log_xgb)
        
        feature_row['Adj Close'] = predicted_close
        forecast_input = pd.concat([forecast_input, pd.DataFrame(feature_row, index=[next_date])])
        forecast_df = pd.concat([forecast_df, pd.DataFrame(feature_row, index=[next_date])])

    return pd.Series(y_pred_test, index=test_df.index), pd.Series(forecast_df['Adj Close'], index=forecast_df.index)

def forecast_with_rolling(best_model, train_df, test_df, feature_cols, scaler, mse_threshold=70, window_size=90, forecast_days=30):
    test_predicted = []
    rolling_forecast = []
    
    # Prediction on Test Set
    for i in range(len(test_df)):
        rolling_train_df = pd.concat([train_df, test_df.iloc[:i]])[-window_size:]
        X_rolling_train = scaler.fit_transform(rolling_train_df[feature_cols].fillna(0))
        y_rolling_train_log = np.log(rolling_train_df['Adj Close'])
        
        if i > 0 and mean_squared_error(test_df['Adj Close'].iloc[:i], test_predicted) > mse_threshold:
            best_model.fit(X_rolling_train, y_rolling_train_log)
        
        X_test_point = scaler.transform(test_df[feature_cols].iloc[[i]].fillna(0))
        y_pred_log_xgb = best_model.predict(X_test_point)
        y_pred_test_point = np.exp(y_pred_log_xgb)[0]
        
        test_predicted.append(y_pred_test_point)
    
    # 30-Day Forecast
    current_input = test_df.copy()
    for i in range(forecast_days):
        rolling_train_df = current_input.iloc[-window_size:]
        X_rolling_train = scaler.fit_transform(rolling_train_df[feature_cols].fillna(0))
        y_rolling_train_log = np.log(rolling_train_df['Adj Close'])
        
        best_model.fit(X_rolling_train, y_rolling_train_log)
        
        last_close = current_input['Adj Close'].iloc[-1]
        ema_9 = current_input['Adj Close'].ewm(span=9, adjust=False).mean().iloc[-1]
        sma_5 = current_input['Adj Close'].rolling(window=5).mean().iloc[-1]
        sma_10 = current_input['Adj Close'].rolling(window=10).mean().iloc[-1]
        sma_15 = current_input['Adj Close'].rolling(window=15).mean().iloc[-1]
        sma_30 = current_input['Adj Close'].rolling(window=30).mean().iloc[-1]
        sma_50 = current_input['Adj Close'].rolling(window=50).mean().iloc[-1]
        returns = current_input['Returns'].iloc[-1]
        
        feature_row = {
            'EMA_9': ema_9, 'SMA_5': sma_5, 'SMA_10': sma_10,
            'SMA_15': sma_15, 'SMA_30': sma_30, 'SMA_50': sma_50, 'Returns': returns
        }
        
        input_features = pd.DataFrame([feature_row], columns=feature_cols)
        input_scaled = scaler.transform(input_features.fillna(0))
        
        pred_log_xgb = best_model.predict(input_scaled)
        predicted_close = np.exp(pred_log_xgb)[0]
        
        rolling_forecast.append(predicted_close)
        
        next_date = current_input.index[-1] + pd.offsets.BDay(1)
        new_row = pd.DataFrame({'Adj Close': [predicted_close], 'Returns': [(predicted_close - last_close) / last_close]}, index=[next_date])
        current_input = pd.concat([current_input, new_row])

    return pd.Series(test_predicted, index=test_df.index), pd.Series(rolling_forecast, index=current_input.index[-forecast_days:])