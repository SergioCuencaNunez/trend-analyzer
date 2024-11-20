
<p align="center">
  <img src="src/assets/banner-dark.png" alt="Logo" width="500">
</p>

## Overview

Trend Analyzer is a web application built with Flask and Dash, designed to analyze, visualize, and forecast financial trends using various models such as XGBoost and Prophet models. The app provides interactive graphs and insights based on the provided financial data.

## Features

- **Financial Trend Analysis**: Leverages XGBoost and Prophet models to provide accurate predictions.
- **Interactive Graphs**: Built with Dash and Plotly for dynamic data visualization.
- **Advanced Metrics**: Displays comprehensive financial metrics such as growth, profitability, volatility, and sentiment analysis.
- **Buy & Sell Strategies**: Offers market sentiment recommendations and investment strategies based on stock trends.
- **News Integration**: Includes the latest financial news to help users stay informed about market movements.
- **User-Friendly Interface**: Easy-to-use interface for analyzing and forecasting financial data.

## New Additions

- **Metrics Section**: Analyze key financial metrics like:
  - Growth
  - Profitability
  - Volatility
  - Market Sentiment
- **News Integration**: View the latest financial news to understand market trends better and incorporate them into decision-making.
- **Investment Recommendations**: Buy and sell strategies are displayed, helping users make informed investment decisions based on the forecast data.
- **Interactive Financial Insights**: Enhanced visuals for volume trends, market capitalization, and average volume trends for better decision-making.

---

## Prerequisites

- Docker installed on your system.
- Docker Hub account (for image hosting).

---

## Commands

### For the Developer (Building the Docker Image)

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/SergioCuencaNunez/trend-analyzer.git
   cd trend-analyzer
   ```

2. **Build the Docker Image and Push it to DockerHub**:
   ```sh
   docker buildx create --use
   docker buildx inspect --bootstrap
   docker buildx build --platform linux/amd64,linux/arm64 -t sergiocuenca1/trend-analyzer --push .
   ```

3. **Save the Docker Image** (optional for distribution):
   ```sh
   docker save -o my-flask-app.tar sergiocuenca1/trend-analyzer
   ```

---

### For the User (Running the Docker Container)

1. **Pull the Docker Image from Docker Hub**:
   ```sh
   docker pull sergiocuenca1/trend-analyzer:latest
   ```

2. **Run the Docker Container** (specifying the platform):
   - **For Intel-based**:
     ```sh
     docker run --platform linux/amd64 -p 8080:8080 sergiocuenca1/trend-analyzer:latest
     ```
   - **For M1 or later-based**:
     ```sh
     docker run --platform linux/arm64 -p 8080:8080 sergiocuenca1/trend-analyzer:latest
     ```

---

## Usage

1. **Access the Application**:
   Open your web browser and navigate to `http://localhost:8080`.

2. **Explore Key Metrics**:
   Gain insights into:
   - Volume and Average Volume trends
   - Market Capitalization and Volatility
   - Dividends and Growth analysis

3. **Forecast Stock Prices**:
   - Forecast stock price trends based on the number of days or desired earnings percentage.
   - View Buy & Sell recommendations with clear market sentiment analysis.

4. **Stay Updated**:
   Check the integrated **News Section** for the latest market updates and events that could impact stock trends.

5. **Visualize Data**:
   - Explore dynamic candlestick charts.
   - Analyze sparklines for financial metrics like volume and volatility.

---

## Troubleshooting

- **Worker Timeout Issues**:
  If you encounter worker timeout issues, try increasing the Gunicorn timeout in the Dockerfile.

  ```Dockerfile
  CMD ["gunicorn", "-b", ":8080", "--timeout", "120", "app_instance:server"]
  ```

- **Compatibility Issues**:
  Ensure you specify the correct platform when running the Docker container on different architectures.

---

## Contribution

For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the Apache License. See the [LICENSE](LICENSE) file for details.

---

For more information, visit the [TrendAnalyzer GitHub Repository](https://github.com/SergioCuencaNunez/trend-analyzer).
