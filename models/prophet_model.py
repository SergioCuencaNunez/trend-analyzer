from prophet import Prophet

def fit_prophet(data):
    # Prepare the Data for Prophet
    data_prophet = data.reset_index()
    data_prophet = data_prophet.rename(columns={'Date': 'ds', 'Close': 'y'})

    # Create and fit Prophet model
    model = Prophet(daily_seasonality=True)
    model.fit(data_prophet)
    
    return model, data_prophet

def forecast_prophet(model, data_prophet, forecast_days=90):
    # Create future dataframe for the next forecast_days
    future = model.make_future_dataframe(periods=forecast_days)
    forecast = model.predict(future)

    return forecast
