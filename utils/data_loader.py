"""
Data loader utility for Bitcoin price dashboard.
Fetches data from CoinGecko API and handles data processing.
"""

import pandas as pd
import requests
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import streamlit as st


class BitcoinDataLoader:
    """Handles Bitcoin data loading from CoinGecko API."""
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    @staticmethod
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def fetch_bitcoin_data(days: int = 365) -> pd.DataFrame:
        """
        Fetch Bitcoin price data from CoinGecko API.
        
        Args:
            days: Number of days of historical data to fetch
            
        Returns:
            DataFrame with Bitcoin price data
        """
        try:
            # Fetch price data
            price_url = f"{BitcoinDataLoader.BASE_URL}/coins/bitcoin/market_chart"
            price_params = {
                "vs_currency": "usd",
                "days": days,
                "interval": "daily" if days > 90 else "hourly"
            }
            
            price_response = requests.get(price_url, params=price_params, timeout=10)
            price_response.raise_for_status()
            price_data = price_response.json()
            
            # Process price data
            prices = price_data['prices']
            volumes = price_data['total_volumes']
            market_caps = price_data['market_caps']
            
            df = pd.DataFrame({
                'timestamp': [item[0] for item in prices],
                'price': [item[1] for item in prices],
                'volume': [item[1] for item in volumes],
                'market_cap': [item[1] for item in market_caps]
            })
            
            # Convert timestamp to datetime
            df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
            df = df.drop('timestamp', axis=1)
            
            # Calculate additional metrics
            df['price_change'] = df['price'].pct_change()
            df['volume_sma_7'] = df['volume'].rolling(window=7).mean()
            df['price_sma_7'] = df['price'].rolling(window=7).mean()
            df['price_sma_30'] = df['price'].rolling(window=30).mean()
            
            # Add volatility calculation
            df['volatility'] = df['price_change'].rolling(window=7).std()
            
            return df.sort_values('date').reset_index(drop=True)
            
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data from API: {str(e)}")
            return BitcoinDataLoader.load_sample_data()
        except Exception as e:
            st.error(f"Error processing data: {str(e)}")
            return BitcoinDataLoader.load_sample_data()
    
    @staticmethod
    def load_sample_data() -> pd.DataFrame:
        """Load sample data when API is unavailable."""
        try:
            sample_path = "data/bitcoin_sample.csv"
            df = pd.read_csv(sample_path)
            df['date'] = pd.to_datetime(df['date'])
            return df
        except FileNotFoundError:
            # Generate minimal sample data
            dates = pd.date_range(
                start=datetime.now() - timedelta(days=30),
                end=datetime.now(),
                freq='D'
            )
            
            # Generate realistic Bitcoin price data
            import numpy as np
            np.random.seed(42)
            
            base_price = 45000
            prices = []
            current_price = base_price
            
            for _ in dates:
                change = np.random.normal(0, 0.02)  # 2% daily volatility
                current_price *= (1 + change)
                prices.append(max(current_price, 1000))  # Minimum price floor
            
            df = pd.DataFrame({
                'date': dates,
                'price': prices,
                'volume': np.random.uniform(20000000000, 50000000000, len(dates)),
                'market_cap': [p * 19000000 for p in prices],  # Approximate circulating supply
                'price_change': [0] + [prices[i]/prices[i-1] - 1 for i in range(1, len(prices))],
                'price_sma_7': prices,
                'price_sma_30': prices,
                'volume_sma_7': np.random.uniform(20000000000, 50000000000, len(dates)),
                'volatility': np.random.uniform(0.01, 0.05, len(dates))
            })
            
            return df
    
    @staticmethod
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def get_current_stats() -> Dict[str, Any]:
        """Get current Bitcoin statistics."""
        try:
            url = f"{BitcoinDataLoader.BASE_URL}/coins/bitcoin"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'current_price': data['market_data']['current_price']['usd'],
                'price_change_24h': data['market_data']['price_change_percentage_24h'],
                'market_cap': data['market_data']['market_cap']['usd'],
                'total_volume': data['market_data']['total_volume']['usd'],
                'circulating_supply': data['market_data']['circulating_supply'],
                'last_updated': data['last_updated']
            }
        except Exception as e:
            st.warning(f"Could not fetch current stats: {str(e)}")
            return {
                'current_price': 45000,
                'price_change_24h': 2.5,
                'market_cap': 850000000000,
                'total_volume': 25000000000,
                'circulating_supply': 19000000,
                'last_updated': datetime.now().isoformat()
            }
    
    @staticmethod
    def filter_data_by_date(df: pd.DataFrame, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Filter DataFrame by date range."""
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        return df.loc[mask].copy()
    
    @staticmethod
    def calculate_metrics(df: pd.DataFrame) -> Dict[str, float]:
        """Calculate key metrics from the data."""
        if df.empty:
            return {}
        
        return {
            'total_return': ((df['price'].iloc[-1] / df['price'].iloc[0]) - 1) * 100,
            'max_price': df['price'].max(),
            'min_price': df['price'].min(),
            'avg_volume': df['volume'].mean(),
            'volatility': df['price_change'].std() * 100,
            'sharpe_ratio': (df['price_change'].mean() / df['price_change'].std()) * (365 ** 0.5) if df['price_change'].std() > 0 else 0
        }