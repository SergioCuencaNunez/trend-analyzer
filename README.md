<p align="center">
  <img src="assets/banner-dark.png" alt="Logo" width="500">
</p>

## Overview

Trend Analyzer is a web application built with Flask and Dash, designed to analyze, visualize and forecast financial trends using various models such as ARIMA-GARCH, Prophet and LSTM Neural Networks. The app provides interactive graphs and insights based on the provided financial data.

## Features

- **Financial Trend Analysis**: Utilizes ARIMA-GARCH, Prophet and LSTM models.
- **Interactive Graphs**: Built with Dash and Plotly for dynamic data visualization.
- **User-Friendly Interface**: Easy-to-use interface for analyzing and forecasting financial data.

## Prerequisites

- Docker installed on your system.
- Docker Hub account (for image hosting).

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

### For the User (Running the Docker Container)

1. **Pull the Docker Image from Docker Hub**:
   ```sh
   docker pull sergiocuenca1/trend-analyzer:latest
   ```

2. **Run the Docker Container** (specifying the platform):
   * For Intel based:  
      ```sh
      docker run --platform linux/amd64 -p 8080:8080 sergiocuenca1/trend-analyzer:latest
      ```
   * For M1 o later based: 
      ```sh
      docker run --platform linux/arm64 -p 8080:8080 sergiocuenca1/trend-analyzer:latest
      ```

## Usage

1. **Access the Application**:
   Open your web browser and navigate to `http://localhost:8080`.

2. **View and Interact with Graphs**:
   Use the provided interface to explore the stocks.

3. **Forecast Stock Proces**:
   Forecast stock price based on the numer of days or desired percentage of earnings and explore the generated graphs and insights.

## Troubleshooting

- **Worker Timeout Issues**:
  If you encounter worker timeout issues, try increasing the Gunicorn timeout in the Dockerfile.

  ```Dockerfile
  CMD ["gunicorn", "-b", ":8080", "--timeout", "120", "app_instance:server"]
  ```

- **Compatibility Issues**:
  Ensure you specify the correct platform when running the Docker container on different architectures.

## Contribution

For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the Apache License. See the [LICENSE](LICENSE) file for details.

---

For more information, visit the [TrendAnalyzer GitHub Repository](https://github.com/SergioCuencaNunez/trend-analyzer).

<!-- For more information, visit the [TrendAnalyzer Web](https://trendanalyzer.com). -->
