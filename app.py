"""
Bitcoin Interactive Dashboard
A comprehensive dashboard for Bitcoin price analysis and visualization.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

# Import our custom data loader
from utils.data_loader import BitcoinDataLoader


def configure_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Bitcoin Dashboard",
        page_icon="₿",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def apply_custom_css():
    """Apply custom CSS styling."""
    st.markdown("""
    <style>
    /* Dark theme colors */
    .stApp {
        background-color: #121317;
        color: #FFFFFF;
    }
    
    .metric-card {
        background-color: #1e1e1e;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #4693ce;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #4693ce;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #CCCCCC;
        margin-top: 0.5rem;
    }
    
    .positive {
        color: #00FF88;
    }
    
    .negative {
        color: #FF4444;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1a1a1a;
    }
    
    /* Header styling */
    .dashboard-header {
        background: linear-gradient(90deg, #4693ce 0%, #1e3a8a 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .dashboard-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: white;
    }
    
    .dashboard-subtitle {
        font-size: 1.2rem;
        color: #E0E0E0;
    }
    
    /* Chart container */
    .chart-container {
        background-color: #1a1a1a;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        border: 1px solid #333333;
    }
    </style>
    """, unsafe_allow_html=True)


def create_sidebar():
    """Create and configure the sidebar with filters."""
    st.sidebar.header("📊 Dashboard Controls")
    
    # Date range picker
    st.sidebar.subheader("📅 Date Range")
    max_date = datetime.now().date()
    min_date = max_date - timedelta(days=365)
    
    date_range = st.sidebar.date_input(
        "Select Date Range:",
        value=(max_date - timedelta(days=90), max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Chart type selector
    st.sidebar.subheader("📈 Chart Options")
    chart_types = st.sidebar.multiselect(
        "Select Chart Types:",
        ["Price Chart", "Volume Chart", "Market Cap Chart", "Volatility Chart"],
        default=["Price Chart", "Volume Chart"]
    )
    
    # Technical indicators
    st.sidebar.subheader("🔧 Technical Indicators")
    show_sma = st.sidebar.checkbox("Show Moving Averages", value=True)
    show_volume = st.sidebar.checkbox("Show Volume Overlay", value=False)
    
    # Data refresh
    st.sidebar.subheader("🔄 Data Management")
    if st.sidebar.button("Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    
    # Export data
    st.sidebar.subheader("📥 Export Data")
    
    return date_range, chart_types, show_sma, show_volume


def create_metrics_cards(current_stats, period_metrics):
    """Create KPI metrics cards."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        price_change_class = "positive" if current_stats['price_change_24h'] > 0 else "negative"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${current_stats['current_price']:,.0f}</div>
            <div class="metric-label">Current Price</div>
            <div class="{price_change_class}">
                {current_stats['price_change_24h']:+.2f}% (24h)
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${current_stats['market_cap']/1e9:.1f}B</div>
            <div class="metric-label">Market Cap</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${current_stats['total_volume']/1e9:.1f}B</div>
            <div class="metric-label">24h Volume</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        return_class = "positive" if period_metrics.get('total_return', 0) > 0 else "negative"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value {return_class}">{period_metrics.get('total_return', 0):+.1f}%</div>
            <div class="metric-label">Period Return</div>
        </div>
        """, unsafe_allow_html=True)


def create_price_chart(df, show_sma=True):
    """Create interactive price chart with technical indicators."""
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=('Bitcoin Price', 'Volume'),
        row_width=[0.7, 0.3]
    )
    
    # Price line
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['price'],
            name='Price',
            line=dict(color='#4693ce', width=2),
            hovertemplate='<b>Date:</b> %{x}<br><b>Price:</b> $%{y:,.2f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Moving averages
    if show_sma and 'price_sma_7' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['price_sma_7'],
                name='7-day SMA',
                line=dict(color='#FFA500', width=1, dash='dash'),
                hovertemplate='<b>7-day SMA:</b> $%{y:,.2f}<extra></extra>'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['price_sma_30'],
                name='30-day SMA',
                line=dict(color='#FF6B6B', width=1, dash='dot'),
                hovertemplate='<b>30-day SMA:</b> $%{y:,.2f}<extra></extra>'
            ),
            row=1, col=1
        )
    
    # Volume bars
    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['volume'],
            name='Volume',
            marker_color='rgba(70, 147, 206, 0.6)',
            hovertemplate='<b>Volume:</b> %{y:,.0f}<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title="Bitcoin Price Analysis",
        template="plotly_dark",
        height=600,
        showlegend=True,
        hovermode='x unified'
    )
    
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    
    return fig


def create_market_cap_chart(df):
    """Create market cap chart."""
    fig = px.area(
        df, 
        x='date', 
        y='market_cap',
        title="Bitcoin Market Capitalization",
        labels={'market_cap': 'Market Cap (USD)', 'date': 'Date'}
    )
    
    fig.update_traces(
        fill='tonexty',
        fillcolor='rgba(70, 147, 206, 0.3)',
        line_color='#4693ce'
    )
    
    fig.update_layout(
        template="plotly_dark",
        height=400,
        hovermode='x unified'
    )
    
    return fig


def create_volatility_chart(df):
    """Create volatility analysis chart."""
    if 'volatility' not in df.columns:
        return None
    
    fig = px.line(
        df,
        x='date',
        y='volatility',
        title="Bitcoin Price Volatility (7-day rolling)",
        labels={'volatility': 'Volatility', 'date': 'Date'}
    )
    
    fig.update_traces(line_color='#FF6B6B')
    fig.update_layout(
        template="plotly_dark",
        height=400,
        hovermode='x unified'
    )
    
    return fig


def create_data_table(df):
    """Create interactive data table."""
    display_df = df[['date', 'price', 'volume', 'market_cap', 'price_change']].copy()
    display_df['price'] = display_df['price'].round(2)
    display_df['volume'] = (display_df['volume'] / 1e9).round(2)
    display_df['market_cap'] = (display_df['market_cap'] / 1e9).round(1)
    display_df['price_change'] = (display_df['price_change'] * 100).round(2)
    
    display_df.columns = ['Date', 'Price ($)', 'Volume (B)', 'Market Cap (B)', 'Price Change (%)']
    
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )


def main():
    """Main dashboard function."""
    configure_page()
    apply_custom_css()
    
    # Header
    st.markdown("""
    <div class="dashboard-header">
        <div class="dashboard-title">₿ Bitcoin Dashboard</div>
        <div class="dashboard-subtitle">Real-time Bitcoin price analysis and market insights</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    date_range, chart_types, show_sma, show_volume = create_sidebar()
    
    # Load data
    with st.spinner("Loading Bitcoin data..."):
        try:
            # Determine days based on date range
            if len(date_range) == 2:
                start_date, end_date = date_range
                days = (end_date - start_date).days
            else:
                days = 90
                start_date = datetime.now().date() - timedelta(days=days)
                end_date = datetime.now().date()
            
            # Fetch data
            df = BitcoinDataLoader.fetch_bitcoin_data(days=min(days + 30, 365))
            current_stats = BitcoinDataLoader.get_current_stats()
            
            # Filter data by date range
            df_filtered = BitcoinDataLoader.filter_data_by_date(
                df, 
                datetime.combine(start_date, datetime.min.time()),
                datetime.combine(end_date, datetime.min.time())
            )
            
            # Calculate metrics
            period_metrics = BitcoinDataLoader.calculate_metrics(df_filtered)
            
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return
    
    # Display metrics
    st.subheader("📊 Key Metrics")
    create_metrics_cards(current_stats, period_metrics)
    
    # Charts section
    st.subheader("📈 Price Analysis")
    
    if "Price Chart" in chart_types:
        with st.container():
            fig_price = create_price_chart(df_filtered, show_sma)
            st.plotly_chart(fig_price, use_container_width=True)
    
    # Additional charts in columns
    chart_cols = st.columns(2)
    
    with chart_cols[0]:
        if "Market Cap Chart" in chart_types:
            fig_mcap = create_market_cap_chart(df_filtered)
            st.plotly_chart(fig_mcap, use_container_width=True)
    
    with chart_cols[1]:
        if "Volatility Chart" in chart_types:
            fig_vol = create_volatility_chart(df_filtered)
            if fig_vol:
                st.plotly_chart(fig_vol, use_container_width=True)
    
    # Data table
    st.subheader("📋 Data Table")
    create_data_table(df_filtered)
    
    # Export functionality
    st.subheader("📥 Export Data")
    col1, col2 = st.columns(2)
    
    with col1:
        csv_data = df_filtered.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv_data,
            file_name=f"bitcoin_data_{start_date}_{end_date}.csv",
            mime="text/csv"
        )
    
    with col2:
        json_data = df_filtered.to_json(orient='records', date_format='iso')
        st.download_button(
            label="Download as JSON",
            data=json_data,
            file_name=f"bitcoin_data_{start_date}_{end_date}.json",
            mime="application/json"
        )
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**Data Source:** [CoinGecko API](https://www.coingecko.com/en/api) | "
        "**Last Updated:** " + str(current_stats.get('last_updated', 'Unknown'))[:19].replace('T', ' ')
    )


if __name__ == "__main__":
    main()