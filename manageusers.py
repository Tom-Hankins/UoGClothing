import tkinter as tk
from tkinter import *
from tkinter import ttk
from styles import CUSTOM_FONTS, CUSTOM_COLOURS
from dataaccess import DBAccess
from customwidgets import CatalogueBrowser
from user import User, UserRegistration
from window import Window

class UsersPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        self.controller = controller
        self.names_matched = []

        # define widgets
        frame = Frame(self, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=50)
        frame.pack(side='top', fill=X, anchor='n')
        frame.pack_propagate(False)
        self.controller = controller
        self.search_label = Label(frame, text="Search:", bg=CUSTOM_COLOURS["FORM_BACKGROUND"])
        self.search_label.pack(side='left', padx=(10, 0))
        self.search_field = Entry(frame, width=40)
        self.search_field.pack(side='left', padx=(10, 0))
        self.search_button = ttk.Button(frame, text="Search", command=self.get_users)
        self.search_button.pack(side='left', padx=(10, 0))

        self.add_new_button = ttk.Button(frame, text="Add New User", command=self.add_new_user)
        self.add_new_button.pack(side='right', padx=(0, 10))

        self.results_frame = Frame(self, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        self.results_frame.pack(side='top', fill='both', expand=True, anchor='n')
        self.results_frame.pack_propagate(False)

        self.create_search_label(
            "Search for and add users here.\n\n"
            "User accounts can be disabled and enabled by clicking the displayed user profile."
        )

    def add_new_user(self):
        add_user_window = Window("USER REGISTRATION", "Add New User", "400x360", False)
        registration = UserRegistration(self, "ADMIN")
        registration.registration_form(add_user_window)

    # This closes all windows, to support multiple windows without closing all will need to add an index to
    # the window in order to track it and close the relevant window
    def close_registration_form(self, result):
        Window.close_windows("USER REGISTRATION")
        if result == "OK":
            self.get_users()

    def get_users(self):
        self.clear_search()
        # Get user input from search entry field, set this as parameters for the sql query
        # Using parameters in the sql query to prevent sql injection
        params = [self.search_field.get(), self.search_field.get(), self.search_field.get()]
        # Create a database connection
        db = DBAccess()
        # Check if item code matches user input or if any item names contain the user input
        sql = """SELECT user_id, email_address, first_name, last_name, address, 
                 city, postcode, password, user_type, is_disabled 
                 FROM users 
                 WHERE instr(lower(email_address), lower(?)) 
                 OR instr(lower(first_name), lower(?))
                 OR instr(lower(last_name), lower(?))
                 """
        self.names_matched = db.fetch_all_db(sql, params)
        # Close the database connection
        db.close_connection()

        # Display results
        if self.names_matched:
            # need to only create object for the results that wil be in view
            matched_names = db.create_object_list(User, self.names_matched[0:6])
            self.create_items(matched_names)
        else:
            # no matching results
            self.create_search_label("There are no results matching your search criteria")
            pass

    def create_items(self, catalogue_items):
        browser = CatalogueBrowser(self.results_frame, catalogue_items, self)
        browser.pack()

    def traverse_list(self, start_index, end_index):
        db = DBAccess()
        matched_names = db.create_object_list(User, self.names_matched[start_index:end_index])
        return matched_names

    def clear_search(self):
        # clears the entire search results frame
        self.names_matched.clear()
        self.results_frame.destroy()
        self.results_frame = Frame(self, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        self.results_frame.pack(side='top', fill='both', expand=True, anchor='n')
        self.results_frame.pack_propagate(False)

    def create_search_label(self, message):
        label = Label(
            self.results_frame, text=message, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"],
            font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], anchor='w', justify='left'
        )
        label.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
