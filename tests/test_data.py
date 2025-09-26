"""
Unit tests for Bitcoin dashboard data loading functionality.
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to Python path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import BitcoinDataLoader


class TestBitcoinDataLoader:
    """Test cases for BitcoinDataLoader class."""
    
    def test_load_sample_data(self):
        """Test loading sample data."""
        df = BitcoinDataLoader.load_sample_data()
        
        # Check if DataFrame is not empty
        assert not df.empty, "Sample data should not be empty"
        
        # Check required columns
        required_columns = ['date', 'price', 'volume', 'market_cap']
        for col in required_columns:
            assert col in df.columns, f"Column '{col}' should be present in sample data"
        
        # Check data types
        assert pd.api.types.is_datetime64_any_dtype(df['date']), "Date column should be datetime"
        assert pd.api.types.is_numeric_dtype(df['price']), "Price column should be numeric"
        assert pd.api.types.is_numeric_dtype(df['volume']), "Volume column should be numeric"
        assert pd.api.types.is_numeric_dtype(df['market_cap']), "Market cap column should be numeric"
    
    def test_filter_data_by_date(self):
        """Test date filtering functionality."""
        # Create sample data
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        df = pd.DataFrame({
            'date': dates,
            'price': range(len(dates)),
            'volume': range(len(dates)),
            'market_cap': range(len(dates))
        })
        
        # Filter data
        start_date = datetime(2024, 6, 1)
        end_date = datetime(2024, 6, 30)
        filtered_df = BitcoinDataLoader.filter_data_by_date(df, start_date, end_date)
        
        # Check filtering
        assert not filtered_df.empty, "Filtered data should not be empty"
        assert all(filtered_df['date'] >= start_date), "All dates should be >= start_date"
        assert all(filtered_df['date'] <= end_date), "All dates should be <= end_date"
        assert len(filtered_df) == 30, "Should have 30 days of data for June"
    
    def test_calculate_metrics(self):
        """Test metrics calculation."""
        # Create test data
        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=30, freq='D'),
            'price': [100 + i for i in range(30)],  # Increasing prices
            'volume': [1000000 for _ in range(30)],
            'market_cap': [(100 + i) * 19000000 for i in range(30)],
            'price_change': [0.01 for _ in range(30)]  # 1% daily change
        })
        
        metrics = BitcoinDataLoader.calculate_metrics(df)
        
        # Check if metrics are calculated
        assert 'total_return' in metrics, "Total return should be calculated"
        assert 'max_price' in metrics, "Max price should be calculated"
        assert 'min_price' in metrics, "Min price should be calculated"
        assert 'avg_volume' in metrics, "Average volume should be calculated"
        assert 'volatility' in metrics, "Volatility should be calculated"
        
        # Check metric values
        assert metrics['total_return'] > 0, "Total return should be positive for increasing prices"
        assert metrics['max_price'] == 129, "Max price should be 129"
        assert metrics['min_price'] == 100, "Min price should be 100"
        assert metrics['avg_volume'] == 1000000, "Average volume should be 1,000,000"
    
    def test_calculate_metrics_empty_dataframe(self):
        """Test metrics calculation with empty DataFrame."""
        df = pd.DataFrame()
        metrics = BitcoinDataLoader.calculate_metrics(df)
        
        assert metrics == {}, "Metrics should be empty dict for empty DataFrame"
    
    def test_data_integrity(self):
        """Test data integrity of sample data."""
        df = BitcoinDataLoader.load_sample_data()
        
        # Check for null values
        assert not df.isnull().any().any(), "Data should not contain null values"
        
        # Check price values are positive
        assert all(df['price'] > 0), "All prices should be positive"
        assert all(df['volume'] > 0), "All volumes should be positive"
        assert all(df['market_cap'] > 0), "All market caps should be positive"
        
        # Check date is sorted
        assert df['date'].is_monotonic_increasing, "Dates should be in ascending order"
    
    def test_current_stats_structure(self):
        """Test that current stats returns expected structure."""
        stats = BitcoinDataLoader.get_current_stats()
        
        # Check required keys
        required_keys = [
            'current_price', 'price_change_24h', 'market_cap',
            'total_volume', 'circulating_supply', 'last_updated'
        ]
        
        for key in required_keys:
            assert key in stats, f"Stats should contain '{key}' key"
        
        # Check data types
        assert isinstance(stats['current_price'], (int, float)), "Current price should be numeric"
        assert isinstance(stats['price_change_24h'], (int, float)), "Price change should be numeric"
        assert isinstance(stats['market_cap'], (int, float)), "Market cap should be numeric"


if __name__ == "__main__":
    # Run basic tests
    loader = TestBitcoinDataLoader()
    
    print("Running tests...")
    
    try:
        loader.test_load_sample_data()
        print("✅ test_load_sample_data passed")
    except AssertionError as e:
        print(f"❌ test_load_sample_data failed: {e}")
    
    try:
        loader.test_filter_data_by_date()
        print("✅ test_filter_data_by_date passed")
    except AssertionError as e:
        print(f"❌ test_filter_data_by_date failed: {e}")
    
    try:
        loader.test_calculate_metrics()
        print("✅ test_calculate_metrics passed")
    except AssertionError as e:
        print(f"❌ test_calculate_metrics failed: {e}")
    
    try:
        loader.test_calculate_metrics_empty_dataframe()
        print("✅ test_calculate_metrics_empty_dataframe passed")
    except AssertionError as e:
        print(f"❌ test_calculate_metrics_empty_dataframe failed: {e}")
    
    try:
        loader.test_data_integrity()
        print("✅ test_data_integrity passed")
    except AssertionError as e:
        print(f"❌ test_data_integrity failed: {e}")
    
    try:
        loader.test_current_stats_structure()
        print("✅ test_current_stats_structure passed")
    except AssertionError as e:
        print(f"❌ test_current_stats_structure failed: {e}")
    
    print("All tests completed!")