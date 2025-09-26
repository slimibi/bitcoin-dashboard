# Bitcoin Interactive Dashboard

A comprehensive, real-time Bitcoin price analysis dashboard built with Python and Streamlit. This professional-grade application provides interactive visualizations, technical analysis, and market insights for Bitcoin cryptocurrency data.

![Bitcoin Dashboard](https://img.shields.io/badge/Bitcoin-Dashboard-orange?style=for-the-badge&logo=bitcoin)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## Project Overview

This Bitcoin dashboard delivers a modern, interactive web application that displays real-time Bitcoin market data with professional-grade visualizations. The application features a responsive design, dark theme, and comprehensive analytics tools perfect for traders, analysts, and cryptocurrency enthusiasts.

### Key Highlights
- **Real-time Data**: Live Bitcoin price feeds from CoinGecko API
- **Modern UI**: Dark theme with responsive design
- **Interactive Charts**: Multiple chart types with technical indicators
- **Offline Support**: Fallback sample data when API is unavailable
- **Data Export**: CSV and JSON export functionality
- **Tested Code**: Comprehensive unit tests included

## Technology Stack

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Core programming language | 3.8+ |
| **Streamlit** | Interactive web framework | 1.28.1 |
| **Pandas** | Data manipulation and analysis | 2.1.3 |
| **Plotly** | Interactive data visualization | 5.17.0 |
| **Requests** | API data fetching | 2.31.0 |
| **NumPy** | Numerical computing | 1.24.3 |
| **Pytest** | Unit testing framework | 7.4.3 |

## Project Structure

```
bitcoin-dashboard/
├── app.py                     # Main Streamlit dashboard application
├── requirements.txt           # Python dependencies with pinned versions
├── README.md                  # Comprehensive project documentation
├── data/                      # Sample datasets and cached data
│   └── bitcoin_sample.csv     # Fallback dataset for offline use
├── utils/                     # Helper utilities and data processing
│   └── data_loader.py        # Bitcoin API data loader and processor
└── tests/                     # Unit tests and test utilities
    └── test_data.py          # Data loading and processing tests
```

## Features

### Dashboard Components

1. **Key Metrics Cards**
   - Current Bitcoin price with 24h change
   - Market capitalization
   - 24-hour trading volume
   - Period return calculation

2. **Interactive Charts**
   - **Price Chart**: Candlestick-style with moving averages (7-day and 30-day SMA)
   - **Volume Chart**: Trading volume analysis with overlay options
   - **Market Cap Chart**: Market capitalization trends
   - **Volatility Chart**: Price volatility analysis with rolling calculations

3. **Advanced Filtering**
   - Date range picker for historical analysis
   - Chart type multiselect
   - Technical indicator toggles
   - Real-time data refresh

4. **Data Management**
   - Interactive data table with sorting and filtering
   - Export functionality (CSV and JSON formats)
   - Automatic caching for performance optimization
   - Offline mode with sample data fallback

### User Interface

- **Dark Theme**: Professional dark background (`#121317`) with accent colors
- **Responsive Layout**: Works seamlessly on desktop and tablet devices
- **Interactive Elements**: Hover effects, tooltips, and dynamic updates
- **Clean Typography**: Optimized for readability and professional appearance

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection for live data (optional - works offline with sample data)

### Installation

1. **Clone or download the project:**
   ```bash
   # If you have the files, navigate to the directory
   cd bitcoin-dashboard
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard:**
   ```bash
   streamlit run app.py
   ```

4. **Access the application:**
   - Open your web browser
   - Navigate to `http://localhost:8501`
   - The dashboard will load automatically

### Alternative Installation (Virtual Environment)

```bash
# Create virtual environment
python -m venv bitcoin_dashboard_env

# Activate virtual environment
# On Windows:
bitcoin_dashboard_env\\Scripts\\activate
# On macOS/Linux:
source bitcoin_dashboard_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Data Sources

### Primary Data Source: CoinGecko API

The application fetches real-time Bitcoin data from the [CoinGecko API](https://www.coingecko.com/en/api), which provides:

- **Historical Price Data**: Up to 365 days of historical prices
- **Trading Volume**: 24-hour and historical volume data
- **Market Capitalization**: Real-time market cap calculations
- **Market Statistics**: Current price, price changes, and supply data

### API Endpoints Used:
- `https://api.coingecko.com/api/v3/coins/bitcoin/market_chart` - Historical data
- `https://api.coingecko.com/api/v3/coins/bitcoin` - Current statistics

### Offline Functionality

When the API is unavailable, the dashboard automatically switches to sample data mode with:
- 30 days of realistic Bitcoin price data
- Calculated technical indicators
- All dashboard features remain functional

## Testing

The project includes comprehensive unit tests to ensure data integrity and functionality.

### Running Tests

```bash
# Run with pytest
pytest tests/test_data.py -v

# Run with Python directly
python tests/test_data.py
```

### Test Coverage

The test suite covers:
- Data loading and API integration
- Date filtering and data processing
- Metrics calculations and validation
- Data integrity and error handling
- Sample data fallback functionality

## Deployment Options

### Option 1: Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click

### Option 2: Local Deployment

```bash
# Run with custom port
streamlit run app.py --server.port 8080

# Run with external access
streamlit run app.py --server.address 0.0.0.0
```

### Option 3: Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

## Usage Examples

### Basic Usage

1. **View Current Bitcoin Price**: Check the main metrics cards for real-time price and 24h change
2. **Analyze Price Trends**: Use the interactive price chart with moving averages
3. **Compare Time Periods**: Adjust the date range to analyze different periods
4. **Export Data**: Use the export buttons to download data for external analysis

### Advanced Features

```python
# Custom date range analysis
start_date = "2024-01-01"
end_date = "2024-12-31"
# Use sidebar date picker to set custom ranges

# Technical Analysis
# Enable moving averages in sidebar
# Toggle volume overlay for price correlation analysis

# Data Export
# Click "Download as CSV" for spreadsheet analysis
# Click "Download as JSON" for programmatic use
```

## Contributing

We welcome contributions to improve the Bitcoin Dashboard! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Run the test suite**: `pytest tests/`
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add unit tests for new features
- Update documentation for significant changes
- Test with both live API and offline mode

## Troubleshooting

### Common Issues

**Issue**: Dashboard won't start
```bash
# Solution: Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Issue**: API connection errors
- The dashboard automatically falls back to sample data
- Check internet connection
- CoinGecko API may have rate limits

**Issue**: Charts not displaying
- Ensure all dependencies are installed
- Check browser console for JavaScript errors
- Try refreshing the page

### Performance Optimization

- Data is cached for 5 minutes to reduce API calls
- Use date filtering to reduce data processing
- Clear cache using the "Refresh Data" button if needed

## Roadmap

### Upcoming Features

- [ ] Multiple cryptocurrency support (Ethereum, Litecoin, etc.)
- [ ] Advanced technical indicators (RSI, MACD, Bollinger Bands)
- [ ] Price alerts and notifications
- [ ] Portfolio tracking functionality
- [ ] Historical comparison tools
- [ ] Mobile app version

### Enhancement Ideas

- [ ] Machine learning price predictions
- [ ] Social sentiment analysis integration
- [ ] News feed integration
- [ ] Real-time trading signals
- [ ] Multi-language support

## License

This project is licensed under the MIT License - see the details below:

```
MIT License

Copyright (c) 2024 Bitcoin Dashboard

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Author

Created for the cryptocurrency community

## Acknowledgments

- **CoinGecko** for providing free, reliable cryptocurrency API
- **Streamlit** team for the amazing web app framework
- **Plotly** for powerful interactive visualizations
- **Python** community for excellent data science libraries

---

**Star this repository if you found it helpful!**

For questions, issues, or suggestions, please open an issue on GitHub.