import streamlit as st
from utils import DataLoader, SidebarFilter, Dashboard

TITLE_ICON = ":star:"
HIDE_STREAMLIT_STYLE = """
    <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """


def app():
    st.title(f"{TITLE_ICON} Rating")

    st.header("Customer Satisfaction Analysis")

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
    df_selection, _ = sidebar_filter.filter_data()

    dashboard = Dashboard(df_selection)

    dashboard.average_rating_by_branch()

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
         dashboard.plot_avg_rating_by_customer_type()
    with col2:
         dashboard.rating_vs_product_line()

    # Hide Streamlit default style
    st.markdown(HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)
    


