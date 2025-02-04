# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 12:58:45 2025

@author: nkgarrit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(page_title="Sample Analysis Dashboard", layout="wide")

# Function to load data
@st.cache_data(ttl=600)  # Cache data for 10 minutes
def load_data():
    try:
        # Replace with your GitHub raw data URL
        url = "https://raw.githubusercontent.com/nkgarrity/streamlit_test/main/data/samples_data.csv"
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load data
df = load_data()

if df is not None:
    # Dashboard title
    st.title("Sample Analysis Dashboard")
    st.write("Comparing yield and disease ratings across samples")
    
    # Sidebar filters
    st.sidebar.header("Filters")
    selected_treatments = st.sidebar.multiselect(
        "Select Treatments",
        options=df['treatment'].unique(),
        default=df['treatment'].unique()
    )
    
    # Filter data based on selection
    filtered_df = df[df['treatment'].isin(selected_treatments)]
    
    # Create two columns for metrics
    col1, col2 = st.columns(2)
    
    with col1:
        # Yield comparison box plot
        fig_yield = px.box(
            filtered_df,
            x='treatment',
            y='yield_bushels',
            color='treatment',
            title='Yield Distribution by Treatment'
        )
        st.plotly_chart(fig_yield, use_container_width=True)
        
        # Add summary statistics
        st.write("### Yield Summary Statistics")
        yield_stats = filtered_df.groupby('treatment')['yield_bushels'].agg([
            'mean', 'std', 'min', 'max'
        ]).round(2)
        st.dataframe(yield_stats)
    
    with col2:
        # Disease rating scatter plot
        fig_disease = px.scatter(
            filtered_df,
            x='sample_id',
            y='disease_rating',
            color='treatment',
            title='Disease Ratings by Sample'
        )
        st.plotly_chart(fig_disease, use_container_width=True)
        
        # Add summary statistics
        st.write("### Disease Rating Summary Statistics")
        disease_stats = filtered_df.groupby('treatment')['disease_rating'].agg([
            'mean', 'std', 'min', 'max'
        ]).round(2)
        st.dataframe(disease_stats)
    
    # Correlation analysis
    st.write("### Correlation Analysis")
    fig_correlation = px.scatter(
        filtered_df,
        x='disease_rating',
        y='yield_bushels',
        color='treatment',
        trendline="ols",
        title='Yield vs Disease Rating'
    )
    st.plotly_chart(fig_correlation, use_container_width=True)
    
    # Raw data table
    st.write("### Raw Data")
    st.dataframe(filtered_df)