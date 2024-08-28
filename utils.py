import pandas as pd
import plotly.express as px

import streamlit as st
import streamlit_shadcn_ui as ui



class DataLoader:
    """Class to handle data loading and processing."""

    @st.cache_data
    def get_data_from_excel(_self, path: str, sheet_name: str, usecols: str, nrows: int):
        """Loads data from an Excel file and processes it."""
        df = pd.read_excel(
            io=path,
            engine="openpyxl",
            sheet_name=sheet_name,
            skiprows=3,
            usecols=usecols,
            nrows=nrows,
        )
        df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour

        # Convert the 'Date' column to datetime, ensuring day comes first
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        
        # Sort the data by the Date column
        df_sorted = df.sort_values(by='Date')
        
        # Extract Day of the Week for grouping
        df_sorted['DayOfWeek'] = df_sorted['Date'].dt.day_name()
        
        return df_sorted


class SidebarFilter:
    """Class to handle the sidebar filtering options."""

    def __init__(self, df):
        self.df = df

    def filter_data(self):
        """Displays sidebar filters and returns the filtered dataframe."""
        st.sidebar.header("Filter Options:")

        # City Filter
        cities = self.df['City'].unique().tolist()        
        selected_cities = st.sidebar.multiselect(
            "Select City:", options=cities, default=cities
            )

        # Customer Type Filter
        customer_types = self.df['Customer_type'].unique().tolist()
        selected_customer_types = st.sidebar.multiselect(
            "Select Customer Type:", options=customer_types, default=customer_types
            )   

        # Gender Filter
        genders = self.df['Gender'].unique().tolist()
        selected_genders = st.sidebar.multiselect(
            "Select Gender:", options=genders, default=genders
            )


        df_selection = self.df.query(
            "City == @selected_cities & Customer_type == @selected_customer_types & Gender == @selected_genders"
        )

        if df_selection.empty:
            st.warning("No data available based on the current filter settings!")
            st.stop()  # Halts app execution if no data matches the filters

        selected_filters = {
            'cities': selected_cities,
            'customer_types': selected_customer_types,
            'genders': selected_genders,
        }

        return df_selection, selected_filters

PH_ICON="📞"
EM_ICON="📧"
AD_ICON="🏢"

class ContactInfo:

    def __init__(self, selected_filters):
        self.selected_filters=selected_filters

    @staticmethod
    def get_contact_info(city):
        contact_details = {
            "Yangon": {
                "email": "yangon@supermarket.com",
                "phone": "+95 321 456 789",
                "address": "321 YN Street, Yangon, Myanmar"
            },
            "Mandalay": {
                "email": "mandalay@supermarket.com",
                "phone": "+95 123 654 987",
                "address": "123 MY Street, Mandalay, Myanmar"
            },
            "Naypyitaw": {
                "email": "naypyitaw@supermarket.com",
                "phone": "+95 231 456 897",
                "address": "231 NW Street, Naypyitaw, Myanmar"
            }
        }

        default_contact = {
            "email": "contact@supermarket.com",
            "phone": "+95 123 456 789",
            "address": None
        }

        return contact_details.get(city, default_contact)

    def display_contact_info(self):
        selected_cities = self.selected_filters.get('cities', [])

        st.markdown(f"## {PH_ICON} Contact Information")
        if selected_cities:
            for city in selected_cities:

                # Get all contact information in one call
                contact_info = self.get_contact_info(city)
                
                # Display the contact information
                st.markdown(f"### {city}")
                st.write(f"{EM_ICON} **Email**: {contact_info['email']}")
                st.write(f"{PH_ICON} **Phone**: {contact_info['phone']}")
                st.write(f"{AD_ICON} **Address**: {contact_info['address']}")
                st.divider( )
        else:
            st.write("No city selected. Please select at least one city from the sidebar filters.")

class ContactForm:
    def __init__(self, css_file):
        self.css_file = css_file

    def load_custom_css(self):
        """Load custom CSS from the specified file."""
        try:
            with open(self.css_file) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("CSS file not found. Please ensure the path is correct.")

    def display_contact_form(self):
        """Display the contact form and additional instructions."""
        st.markdown("### Reach Out to Us !!")
        st.write("Feel free to contact us with any inquiries or feedback.")

        contact_form = """
        <form action="https://mail.com/BNVAIDYA@EMAIL.COM" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Name" required>
            <input type="email" name="email" placeholder="Email" required>
            <textarea name="message" placeholder="Message"></textarea>
            <button type="submit">Send</button>
        </form>
        """

        st.markdown(contact_form, unsafe_allow_html=True)
        self.load_custom_css()

class Dashboard:
    """Class to generate and display the dashboard."""

    def __init__(self, df_selection):
        self.df_selection = df_selection

    def display_kpis(self):

        """Displays KPIs in the dashboard."""
        total_sales = int(self.df_selection["Total"].sum())
        average_rating = round(self.df_selection["Rating"].mean(), 1)
        star_rating = ":star:" * int(round(average_rating,0))
        average_sale_by_transaction = round(self.df_selection["Total"].mean(), 2)
        gross_income =  round(self.df_selection['gross income'].sum(), 2)


        # Define the maximum rating
        max_rating = 10.0

        left_column, right_column = st.columns(2)

        with left_column:
            st.markdown("<p style='font-size:20px; font-weight:bold; margin-bottom:10px;'>Total Sales:</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:18px; font-weight:bold;'>US $ {total_sales:,}</p>", unsafe_allow_html=True)

        with right_column:
            st.markdown("<p style='font-size:20px; font-weight:bold; margin-bottom:10px;'>Average Sales Per Transaction:</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:18px; font-weight:bold;'>US $ {average_sale_by_transaction}</p>", unsafe_allow_html=True)

        st.markdown("### ")

        left_column, right_column = st.columns(2)

        with left_column:
            st.markdown("<p style='font-size:20px; font-weight:bold; margin-bottom:10px;'>Average Rating:</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:18px; font-weight:bold;'>{average_rating }/{ max_rating}</p>", unsafe_allow_html=True)
            st.markdown(f"{star_rating}")

        with right_column:
            st.markdown("<p style='font-size:20px; font-weight:bold; margin-bottom:10px;'>Gross Income:</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:18px; font-weight:bold;'>US $ {gross_income}</p>", unsafe_allow_html=True)
        
        st.markdown("""---""")


    def display_charts_sales(self):
        """Displays the sales by product line, sales by hour, branch, and payment type charts."""

        # Sales by Product Line Chart
        sales_by_product_line = self.df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total")
        fig_product_sales = px.bar(
            sales_by_product_line,
            x="Total",
            y=sales_by_product_line.index,
            orientation="h",
            title="<b>Sales by Product Line</b>",
            color_discrete_sequence=["#1084B8"] * len(sales_by_product_line),
            template="plotly_white",
        )
        fig_product_sales.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )

        # Sales by Hour Chart
        sales_by_hour = self.df_selection.groupby(by=["hour"])[["Total"]].sum()
        fig_hourly_sales = px.bar(
            sales_by_hour,
            x=sales_by_hour.index,
            y="Total",
            title="<b>Sales by hour</b>",
            color_discrete_sequence=["#1084B8"] * len(sales_by_hour),
            template="plotly_white",
        )
        fig_hourly_sales.update_layout(
            xaxis=dict(tickmode="linear"),
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),
        )

        # Group by Day of the Week and calculate total sales
        sales_by_day = self.df_selection.groupby('DayOfWeek')['Total'].sum().reindex(
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]).reset_index()

        fig_daily_sales = px.bar(
            sales_by_day,
            x='DayOfWeek',
            y='Total',
            title='Total Sales by Day of Week',
            labels={'Total': 'Total Sales (US$)', 'DayOfWeek': 'Day of Week'},
            template='plotly_white'
        )
        fig_daily_sales.update_layout(
            xaxis=dict(tickmode="linear"),
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),
        )

        # Pie Chart for Branch Sales with Separate Slices
        sales_by_branch = self.df_selection.groupby(by=["Branch"])[["Total"]].sum().sort_values(by="Total")
        fig_branch_pie = px.pie(
            self.df_selection, 
            names='Branch', 
            values='Total', 
            title='<b>Sales Distribution by Branch</b>',
            color_discrete_sequence=px.colors.sequential.Greens_r,
            hole=0.1,  # Optional: Creates a donut-style pie chart
        )
        fig_branch_pie.update_traces(
            pull=[0.1 for _ in range(len(sales_by_branch))],  # Pulls each slice away from the center
            textinfo='percent+label'  # Show both the percentage and the label on each slice
        )

        # Pie Chart for Sales by Payment Type 
        sales_by_payment = self.df_selection.groupby(by=["Payment"])[["Total"]].sum().sort_values(by="Total")
        fig_payment_sales = px.pie(
            self.df_selection, 
            names='Payment', 
            values='Total', 
            title='<b>Sales by Payment Type</b>',
            color_discrete_sequence=px.colors.sequential.Reds_r,
            hole=0.15,  # Optional: Creates a donut-style pie chart
        )
        fig_payment_sales.update_traces(
            pull=[0.1 for _ in range(len(sales_by_payment))],  # Pulls each slice away from the center
            textinfo='percent+label'  # Show both the percentage and the label on each slice
        )

        # Pie Chart for Sales by Gender Type 
        sales_by_gender = self.df_selection.groupby('Gender')['Total'].sum().reset_index()
        fig_gender_sales = px.pie(
            sales_by_gender,
            names='Gender',
            values='Total',
            title='Sales Distribution by Gender',
            template='plotly_dark',
            hole=0.4
        )
        fig_gender_sales.update_traces(
            pull=[0.1 for _ in range(len(sales_by_gender))],  # Pulls each slice away from the center
            textinfo='percent+label'  # Show both the percentage and the label on each slice
        )

        # Display charts in columns
        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
        right_column.plotly_chart(fig_product_sales, use_container_width=True)

        st.markdown("""---""")

        # Display pie charts in columns
        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_daily_sales, use_container_width=True)
        right_column.plotly_chart(fig_payment_sales, use_container_width=True)

        st.markdown("""---""")

        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_gender_sales, use_container_width=True)
        right_column.plotly_chart(fig_branch_pie, use_container_width=True)


    def average_rating_by_branch(self):
        st.markdown("### Average Rating by Branch")
        branches = self.df_selection['Branch'].unique()
        cols = st.columns(len(branches))

        for idx, branch in enumerate(branches):
            branch_data = self.df_selection[self.df_selection['Branch'] == branch]
            avg_rating = branch_data['Rating'].mean()
            with cols[idx]:
                ui.metric_card(
                title=branch,
                content=f"{avg_rating:.2f}/10",
                description=None,
                key=f"card{idx}"
            )


    def plot_avg_rating_dayofweek(self):
        avg_rating_dayofweek = self.df_selection.groupby('DayOfWeek')['Rating'].mean().reindex(
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]).reset_index()
        fig = px.line(
            avg_rating_dayofweek,
            x='DayOfWeek',
            y='Rating',
            title='Average Rating by Day of Week',
            labels={'Rating': 'Average Rating', 'DayOfWeek': 'Day of Week'},
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)

    def plot_avg_rating_by_customer_type(self):
        # Group by Customer_type and Gender, and calculate the mean Rating
        avg_rating = self.df_selection.groupby(['Customer_type', 'Gender'])['Rating'].mean().reset_index()

        # Create the plot
        fig = px.bar(
            avg_rating,
            x='Customer_type',
            y='Rating',
            color='Gender',
            barmode='group',
            title='Average Rating by Customer Type and Gender',
            labels={'Rating': 'Average Rating', 'Customer_type': 'Customer Type'},
            template='plotly_white'
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    def rating_vs_product_line(self):
        rating_product = self.df_selection.groupby('Product line')['Rating'].mean().reset_index().sort_values(by='Rating', ascending=False)
        fig = px.bar(
            rating_product,
            x='Rating',
            y='Product line',
            orientation='h',
            title='Average Rating by Product Line',
            labels={'Rating': 'Average Rating', 'Product line': 'Product Line'},
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)


    def transactions_by_branch(self):
        st.markdown("### Transactions by Branch")
        branches = self.df_selection['Branch'].unique()
        cols = st.columns(len(branches))
        for idx, branch in enumerate(branches):
            branch_data = self.df_selection[self.df_selection['Branch'] == branch]
            total_transactions = branch_data['Invoice ID'].nunique()
            with cols[idx]:
                ui.metric_card(
                title=branch,
                content=f"{total_transactions}",
                description=None,
                key=f"card{idx}"
            )


    def plot_transaction_by_dayofweek(self):
        transactions_by_dayofweek = self.df_selection.groupby('DayOfWeek')['Invoice ID'].nunique().reindex(
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]).reset_index()
        
        fig = px.bar(
            transactions_by_dayofweek,
            x='DayOfWeek',
            y='Invoice ID',
            title='Number of Transactions by Day of Week',
            labels={'Invoice ID': 'Number of Transactions', 'DayOfWeek': 'Day of Week'},
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)

    def transactions_vs_product_line(self):
        trans_product = self.df_selection.groupby('Product line')['Invoice ID'].nunique().reset_index().sort_values(by='Invoice ID', ascending=False)
        fig = px.bar(
            trans_product,
            x='Invoice ID',
            y='Product line',
            orientation='h',
            title='Transactions by Product Line',
            labels={'Invoice ID': 'Number of Transactions', 'Product line': 'Product Line'},
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)


    # Display the data for city, and branch in separate columns
    def display_city_branch(self, selected_filters):
        
        selected_cities = selected_filters['cities']

        city_title = ", ".join(selected_cities) if selected_cities else "All Cities"
        st.markdown(f"### Branches for {city_title}")
        cols = st.columns(len(selected_cities))
        
        for idx, city in enumerate(selected_cities):
            branches_in_city = self.df_selection[self.df_selection['City'] == city]['Branch'].unique()        
            with cols[idx]:
                ui.metric_card(
                    title=city,
                    content=f"Branches : {', '.join(branches_in_city) if len(branches_in_city) > 0 else 'No branches available.'}",
                    description=None,
                    key=f"card{idx}"
                )

    # Display the data for city, branch, and description 
    def display_city_and_branch_info(self, selected_filters):
        selected_cities = selected_filters['cities']

        contactinfo = ContactInfo(selected_filters)

        for city in selected_cities:
            branches_in_city = self.df_selection[self.df_selection['City'] == city]['Branch'].unique()

            contact_info = contactinfo.get_contact_info(city)

            st.markdown(f"## {city}")
            st.markdown(f"### Branches in {city}: {', '.join(branches_in_city) if len(branches_in_city) > 0 else 'No branches available.'}")

            # Description
            description = {
                "Yangon": f"{city} is the largest city in Myanmar, known for its vibrant culture and bustling markets. This branch is located at {contact_info['address']}.\
                It opens from 10am to 8pm. And it is opened for loyal members and normal non-members.",
                "Mandalay": f"{city} is a major commercial and educational center in Upper Myanmar. This branch is located at {contact_info['address']}.\
                It opens from 10am to 8pm. And it is opened for loyal members and normal non-members.",
                "Naypyitaw": f"{city} is the capital city of Myanmar, renowned for its extensive parks and government buildings. This branch is located at {contact_info['address']}.\
                It opens from 10am to 8pm. And it is opened for loyal members and normal non-members."
            }.get(city, "No description available for this city.")
            st.markdown(f"{description}")
            st.write("Detailed contact information is given in the Contact page.")
            st.divider()


