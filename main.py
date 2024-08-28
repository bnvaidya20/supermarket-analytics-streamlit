import streamlit as st
from nav_menu import MultiApp


# Constants for styling and page configuration
PAGE_ICON = ":department_store:"
LAYOUT = "wide"


def main():

    # Configuration of Streamlit page
    st.set_page_config(page_title="Supermarket Analytics", page_icon=PAGE_ICON, layout=LAYOUT)

    MultiApp.run() 


if __name__ == "__main__":
    main()

