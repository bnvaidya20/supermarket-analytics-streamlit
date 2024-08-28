import streamlit as st
from utils import DataLoader, SidebarFilter, Dashboard


# Constants for styling and page configuration
TITLE_ICON = "💰"
HIDE_STREAMLIT_STYLE = """
    <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """


def app():

    # Load data
    data_loader = DataLoader()
    df = data_loader.get_data_from_excel(
        path="data\supermarkt_sales.xlsx",
        sheet_name="Sales",
        usecols="B:R",
        nrows=1000,
        )

    # Sidebar filters
    sidebar_filter = SidebarFilter(df)
    df_selection, selected_filters = sidebar_filter.filter_data()

    selected_cities = selected_filters['cities']

    # Dynamically set the page title based on the selected cities
    city_title = ", ".join(selected_cities) if selected_cities else "All Cities"
    st.title(f"{TITLE_ICON} Sales  Dashboard")
    st.header(f"Sales Analysis for {city_title}")

    # Display dashboard
    dashboard = Dashboard(df_selection)
    dashboard.display_charts_sales()

    # Hide Streamlit default style
    st.markdown(HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)