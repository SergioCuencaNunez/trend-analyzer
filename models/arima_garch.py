import numpy as np
import pandas as pd
import pmdarima as pm
from arch import arch_model
import statsmodels.api as sm

def fit_arima_garch(data):
    # Set random seed for reproducibility
    np.random.seed(42)

    # Load the data
    closing_prices = data['Close']

    # Compute Returns
    returns = closing_prices.pct_change().dropna()
    scaled_returns = returns * 100

    # Train-Test Split
    train_size = int(len(scaled_returns) * 0.8)
    train_returns, test_returns = scaled_returns[:train_size], scaled_returns[train_size:]

    # Convert train_returns to DataFrame
    train_returns = pd.DataFrame(train_returns)
    train_returns.rename(columns={train_returns.columns[0]: 'Log Return Rate'}, inplace=True)

    # Re-evaluate ARIMA Model Order
    arima_model = pm.auto_arima(train_returns, seasonal=False, trace=True, error_action='ignore', suppress_warnings=True)
    order = arima_model.order
    arma_mod01 = sm.tsa.ARIMA(train_returns, order=order).fit()

    # GARCH Model Fitting
    def fit_garch_model(train_returns):
        best_aic = np.inf
        best_params = None
        for p in range(1, 4):
            for q in range(1, 4):
                model = arch_model(train_returns, vol='Garch', p=p, q=q, dist='StudentsT')
                res = model.fit(update_freq=5, disp='off')
                if res.aic < best_aic:
                    best_aic = res.aic
                    best_params = (p, q)
        final_model = arch_model(train_returns, vol='Garch', p=best_params[0], q=best_params[1], dist='StudentsT')
        final_res = final_model.fit(update_freq=5, disp='off')
        return final_res

    res = fit_garch_model(train_returns)

    return arma_mod01, res, train_returns, test_returns, closing_prices

def forecast_arima_garch(arima_model, garch_fitted, train_returns, test_returns, closing_prices, forecast_days=90):
    # Extract parameters
    mu = arima_model.params.get('const', 0)
    theta = arima_model.params.get('ar.L1', 0)
    omega = garch_fitted.params['omega']
    alpha = garch_fitted.params['alpha[1]']
    beta = garch_fitted.params['beta[1]']

    # Returns Prediction Function
    def returns_predict(period, mu, theta, omega, alpha, beta, res):
        returns_pool = []
        sigma_t = res.conditional_volatility.iloc[-1]
        for i in range(period):
            epsilon_t = sigma_t * np.random.standard_normal()
            sigma_forecast = np.sqrt(omega + alpha * epsilon_t ** 2 + beta * sigma_t ** 2)
            sigma_forecast = np.clip(sigma_forecast, 1e-8, 10)
            epsilon_forecast = sigma_forecast * np.random.standard_normal()
            returns_forecast = mu + epsilon_forecast + theta * epsilon_t
            returns_forecast = np.clip(returns_forecast, -10, 10)
            returns_pool.append(returns_forecast)
            sigma_t = sigma_forecast
        return returns_pool

    # Generate Predictions
    predicted_returns = returns_predict(len(test_returns), mu, theta, omega, alpha, beta, garch_fitted)
    predicted_returns_df = pd.DataFrame(predicted_returns, index=test_returns.index, columns=['Predicted Returns'])
    test_returns = test_returns.iloc[:len(predicted_returns_df)]
    initial_price = closing_prices.iloc[len(train_returns) - 1]
    predicted_prices = initial_price * np.exp(predicted_returns_df.cumsum() / 100)

    # Forecast for specified days
    new_predicted_returns = returns_predict(forecast_days, mu, theta, omega, alpha, beta, garch_fitted)
    last_date = closing_prices.index[-1]
    new_predicted_dates = pd.date_range(last_date + pd.DateOffset(1), periods=forecast_days)
    new_predicted_returns_df = pd.DataFrame(new_predicted_returns, index=new_predicted_dates, columns=['Predicted Returns'])
    new_initial_price = closing_prices.iloc[-1]
    new_predicted_prices = new_initial_price * np.exp(new_predicted_returns_df.cumsum() / 100)

    return predicted_prices.iloc[:, 0], new_predicted_prices.iloc[:, 0]
