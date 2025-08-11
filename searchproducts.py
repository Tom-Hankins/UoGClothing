from tkinter import *
from tkinter import ttk
import tkinter as tk
from styles import CUSTOM_FONTS, CUSTOM_COLOURS
from dataaccess import DBAccess
from stockitem import StockItem
from shoppingcart import ShoppingCart
from window import Window
from customwidgets import CatalogueBrowser

class SearchProducts(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=CUSTOM_COLOURS["FORM_BACKGROUND"])

        self.controller = controller
        frame = Frame(self, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=50)
        frame.pack(side='top', fill=X, anchor='n')
        frame.pack_propagate(False)
        self.search_term = StringVar()
        self.controller = controller
        self.search_label = Label(frame, text="Search:", bg=CUSTOM_COLOURS["FORM_BACKGROUND"])
        self.search_label.pack(side='left', padx=(10, 0))
        self.search_field = Entry(frame, width=40, textvariable=self.search_term)
        self.search_field.pack(side='left', padx=(10, 0))
        self.search_button = ttk.Button(frame, text="Search", command=self.search_click)
        self.search_button.pack(side='left', padx=(10, 0))
        self.names_matched = []

        self.shopping_cart = ShoppingCart([], self)
        self.cart_img = PhotoImage(file="images/shopping_trolley.png")

        # Shopping cart image
        self.canvas = Canvas(
            frame, height=50, width=50, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], highlightthickness=0, cursor="hand2"
        )
        self.canvas.pack(anchor='nw', side='right', padx=20)
        self.canvas.create_image(0, 0, image=self.cart_img, anchor='nw')
        self.canvas.bind("<Button-1>", self.view_cart)
        # Display number of items
        self.items_in_cart = Label(
            frame, text=f"{self.shopping_cart.count_all()}", fg='red', bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )
        self.items_in_cart.place(x=810, y=28)
        # Frame to display search results
        self.results_frame = Frame(self, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        self.results_frame.pack(side='top', fill='both', expand=True, anchor='n')
        self.results_frame.pack_propagate(False)

    def update_cart(self):
        self.items_in_cart['text'] = f"{self.shopping_cart.count_all()}"
        if self.shopping_cart.count_all() > 0:
            self.items_in_cart['fg'] = 'green'
        else:
            self.items_in_cart['fg'] = 'red'

    def view_cart(self, *args):
        view_cart_window = Window("BROWSE", "Shopping Basket", "900x600", False)
        self.shopping_cart.view_cart(view_cart_window)

    def search_click(self):
        self.clear_search()
        # Get user input from search entry field, set this as parameters for the sql query
        # Using parameters in the sql query to prevent sql injection

        search_term = self.search_term.get()
        if self.search_term.get()[0:3] == "IC-":  # Product code identifier
            search_term = self.search_term.get()[3:]

        params = [search_term, self.search_term.get()]
        # Create a database connection
        db = DBAccess()
        # Check if item code matches user input or if any item names contain the user input
        sql = """SELECT * FROM stock 
        WHERE (item_code = ? COLLATE NOCASE AND is_available = 1) 
        OR (instr(lower(item_name), lower(?)) AND is_available = 1)"""
        self.names_matched = db.fetch_all_db(sql, params)
        # Close the database connection
        db.close_connection()

        # Display results
        if self.names_matched:
            # need to only create object for the results that wil be in view
            obj_params = self.create_tuple_list(self.names_matched[0:6])
            matched_names = db.create_object_list(StockItem, obj_params)
            self.create_items(matched_names)
        else:
            # no matching results
            self.create_search_label("There are no results matching your search criteria")

    def create_items(self, catalogue_items):
        browser = CatalogueBrowser(self.results_frame, catalogue_items, self)
        browser.pack()

    def traverse_list(self, start_index, end_index):
        # Originally an object was created at the point of executing the database query for each item returned,
        # this became very slow when more than 10 or so results were returned, so the number of objects created at once
        # is limited to 6 by using this function
        db = DBAccess()
        obj_params = self.create_tuple_list(self.names_matched[start_index:end_index])
        matched_names = db.create_object_list(StockItem, obj_params)
        return matched_names

    def clear_search(self):
        # clears the entire search results frame
        self.names_matched.clear()
        self.results_frame.destroy()
        self.results_frame = Frame(self, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        self.results_frame.pack(side='top', fill='both', expand=True, anchor='n')
        self.results_frame.pack_propagate(False)

    def create_tuple_list(self, matches):
        # adds the shopping cart object and this parent class to each of the search result tuples and appends to a list
        obj_params = []
        for i in matches:
            a = (self.shopping_cart, self, )
            b = (*i, )
            obj_params.append(tuple(a + b))
        return obj_params

    def create_search_label(self, message):
        Label(
            self.results_frame, text=message, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"],
            font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"]
        ).grid(row=0, column=0, padx=5, pady=5, columnspan=2)

