# Main Streamlit application file

import streamlit as st

import pandas as pd
import plotly.express as px
from data_processing import load_and_preprocess_data

DATA_PATH = 'data/global_energy_rdd_budget'

st.set_page_config(layout="wide")
st.title("Global Energy RD&D Budget Analysis")

# Load and preprocess data
df = load_and_preprocess_data(DATA_PATH)

if df.empty:
    st.error("Could not load data. Please check the data file and path.")
else:
    st.write("This application analyzes and visualizes public RD&D budgets for energy technologies.")
    # --- Sidebar for Filters ---
    st.sidebar.header("Filter Options")

    # Year selection
    all_years = sorted(df['Year'].unique())
    selected_years = st.sidebar.multiselect("Select Year(s)", all_years, default=all_years)

    # Country selection
    all_countries = sorted(df['Country'].unique())
    selected_countries = st.sidebar.multiselect("Select Country(ies)", all_countries, default=all_countries)

    # Sector selection
    all_sectors = sorted(df['Sector'].unique())
    selected_sectors = st.sidebar.multiselect("Select Sector(s)", all_sectors, default=all_sectors)

    # Filter data based on selections
    filtered_df = df[
        df['Year'].isin(selected_years) &
        df['Country'].isin(selected_countries) &
        df['Sector'].isin(selected_sectors)
    ]

    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        # --- Visualizations ---
        st.subheader("1. Global Energy RD&D Budget Trends Over Time")
        # Group by year and sum budgets
        budget_trend = filtered_df.groupby('Year')['Budget (Million USD)'].sum().reset_index()
        fig_trend = px.line(
            budget_trend,
            x='Year',
            y='Budget (Million USD)',
            title='Total RD&D Budget by Year',
            markers=True
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        st.subheader("2. Sectoral Budget Comparison")
        # Group by sector and sum budgets
        sector_budget = filtered_df.groupby('Sector')['Budget (Million USD)'].sum().reset_index()
        fig_sector = px.bar(
            sector_budget,
            x='Sector',
            y='Budget (Million USD)',
            title='Total RD&D Budget by Sector',
            color='Sector',
            template='plotly_white'
        )
        st.plotly_chart(fig_sector, use_container_width=True)

        st.subheader("3. Country-wise Budget Analysis")
        # Group by country and sum budgets
        country_budget = filtered_df.groupby('Country')['Budget (Million USD)'].sum().reset_index()
        fig_country = px.bar(
            country_budget,
            x='Country',
            y='Budget (Million USD)',
            title='Total RD&D Budget by Country',
            color='Country',
            template='plotly_white'
        )
        st.plotly_chart(fig_country, use_container_width=True)

        st.subheader("Detailed Data Table")
        st.dataframe(filtered_df)


