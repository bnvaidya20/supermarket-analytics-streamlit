import streamlit as st

from utils import DataLoader, SidebarFilter, Dashboard


TITLE_ICON = ":house:"
HIDE_STREAMLIT_STYLE = """
    <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """


           
def app():

    st.title(f"{TITLE_ICON} Home")

    st.header("Supermarket Analytics Dashboard")
    st.markdown("This dashboard provides key insights into supermarket performance.")
    st.divider()

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

    city_title = ", ".join(selected_cities) if selected_cities else "All Cities"

    st.markdown(f"### KPIs for {city_title}")

    dashboard = Dashboard(df_selection)
    dashboard.display_kpis()

    dashboard.display_city_branch(selected_filters)

    # Hide Streamlit default style
    st.markdown(HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)