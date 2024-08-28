from streamlit_option_menu import option_menu
import home, about, sales, rating, transaction, contact



class MultiApp:

    def __init__(self):
        self.apps=[]

    def add_app(self, title, function):
        self.apps.append({
            "title":title,
            "function": function
        })

    def run():
        app = option_menu(
        menu_title=None, 
        options=["Home", "About", "Sales", "Rating", "Transactions", "Contact"], 
        icons=["house-fill", "chat-fill", "cash", "star", "list", "envelope"],  
        menu_icon="cast",
        default_index=0, 
        orientation="horizontal",
        styles={"container": {"padding":"5!important", "background-color": 'blue'},
                "icon": {"color":"white", "font-size": "20px"},
                "nav-link": {"color":"white", "font-size":"18px", "text-align":"center"},
                "nav-link-selected": {"background-color": "#02ab21"},}
    )

        if app == "Home":
            home.app()
        if app == "About":
            about.app()        
        if app == "Sales":
            sales.app()            
        if app == "Rating":
            rating.app()  
        if app == "Transactions":
            transaction.app()   
        if app == "Contact":
            contact.app() 