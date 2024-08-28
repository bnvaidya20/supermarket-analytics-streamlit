import streamlit as st
from utils import DataLoader, SidebarFilter, ContactInfo, ContactForm


T_ICON="📬"
HIDE_STREAMLIT_STYLE = """
    <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """

def app():
    st.title(f"{T_ICON} Contact Us")

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
    _, selected_filters = sidebar_filter.filter_data()

    contactinfo=ContactInfo(selected_filters)


    contactinfo.display_contact_info()

    # Initialize the ContactForm class
    contact_form = ContactForm(css_file="style/style.css")

    # Display the contact form
    contact_form.display_contact_form()

    # Hide Streamlit default style
    st.markdown(HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)


