import streamlit as st
from utils import DataLoader, SidebarFilter, Dashboard

T_ICON="ℹ️"
H_ICON="📍"
HIDE_STREAMLIT_STYLE = """
    <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """


def app():
    st.title(f"{T_ICON} About")

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

    st.header(f"{H_ICON} City and Branch Information:")

    dashboard = Dashboard(df_selection)

    dashboard.display_city_and_branch_info(selected_filters)

    # Hide Streamlit default style
    st.markdown(HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)



    



   



