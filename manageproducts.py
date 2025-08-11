from tkinter import *
from tkinter import ttk
import tkinter as tk
from styles import CUSTOM_FONTS, CUSTOM_COLOURS
from dataaccess import DBAccess
from stockitem import StockItem, ManageItem

class ManageProducts (tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        self.controller = controller
        self.names_matched = []

        self.left_panel = Frame(self, bg='white', width=305)
        self.left_panel.pack(side='left', fill=Y, anchor='w')
        self.left_panel.pack_propagate(False)

        self.actions_frame = Frame(self.left_panel, width=305, height=60, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        self.actions_frame.pack(side='top', fill=X, anchor='n')
        self.actions_frame.grid_propagate(False)

        self.search_label = Label(
            self.actions_frame, text="Search Catalogue:", bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]
        )
        self.search_label.grid(row=0, column=0, sticky='w', padx=5, pady=(5, 2))
        self.search_field = Entry(self.actions_frame, width=35)
        self.search_field.grid(row=1, column=0, padx=5)
        self.search_button = ttk.Button(self.actions_frame, text="Search", command=self.search_click)
        self.search_button.grid(row=1, column=1)

        # Add new item frame
        self.add_new_item_frame = Frame(
            self.left_panel, width=305, height='56', bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], highlightthickness=2,
            highlightbackground=CUSTOM_COLOURS["FORM_BACKGROUND"], pady=1, padx=2
        )
        self.add_new_item_frame.pack(side='top', anchor='n', padx=2)
        self.add_new_item_frame.pack_propagate(False)
        self.add_new_item_frame.bind(
            "<Button-1>", lambda event: self.manage_item(StockItem(items=None, parent=self, img_carousel=True), False)
        )
        self.add_new_item_frame.bind("<Enter>", lambda event: self.button_hover_enter())
        self.add_new_item_frame.bind("<Leave>", lambda event: self.button_hover_leave())

        self.add_item_label = Label(
            self.add_new_item_frame, text="Create New Stock Listing", font=CUSTOM_FONTS["LARGE_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]
        )
        self.add_item_label.pack(anchor=CENTER, pady=15)
        self.add_item_label.bind(
            "<Button-1>", lambda event: self.manage_item(StockItem(items=None, parent=self, img_carousel=True), False)
        )
        self.add_item_label.bind("<Enter>", lambda event: self.button_hover_enter())

        # Frame to display search results
        self.search_results_frame = Frame(self.left_panel, width=305, bg='white')
        self.search_results_frame.pack(side='top', fill=BOTH, expand=True, anchor='n')

        # Frame to add and edit items
        self.management_frame = Frame(self, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        self.management_frame.pack(side='top', fill='both', expand=True, anchor='n', pady=(40, 0))
        self.management_frame.pack_propagate(False)
        self.search_click()

    def button_hover_enter(self):
        self.add_item_label['bg'] = 'white'
        self.add_new_item_frame['bg'] = 'white'

    def button_hover_leave(self):
        self.add_item_label['bg'] = CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]
        self.add_new_item_frame['bg'] = CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]

    def search_click(self):
        self.clear_search()
        # Use input from search entry field as parameter for the sql query to prevent sql injection
        search_term = self.search_field.get()
        if self.search_field.get()[0:3] == "IC-":  # Product code identifier
            search_term = self.search_field.get()[3:]

        params = [search_term, self.search_field.get()]
        # Create a database connection
        db = DBAccess()
        # Check if item code matches user input or item names contain the input
        sql = """SELECT * FROM stock WHERE item_code = ? COLLATE NOCASE OR instr(lower(item_name), lower(?))"""
        self.names_matched = db.fetch_all_db(sql, params)
        # Close the database connection
        db.close_connection()

        # Display results
        if self.names_matched:
            obj_params = self.create_tuple_list(self.names_matched[0:5])
            items = db.create_object_list(StockItem, obj_params)
            self.display_search_results(items)
        else:
            # no matching results
            self.create_search_label("No matching items found")

    def create_tuple_list(self, matches):
        # add additional arguments to the data returned by the search query
        obj_params = []
        for i in matches:
            a = ([], self, )
            b = (*i, [], True, )
            obj_params.append(tuple(a + b))
        return obj_params

    def display_search_results(self, items):
        for item in items:
            item_tile = item.admin_item_tile(self.search_results_frame, self)
            item_tile.pack(pady=2)

    def clear_search(self):
        # clears the entire search results frame
        self.names_matched.clear()
        self.search_results_frame.destroy()
        self.search_results_frame = Frame(self.left_panel, width=305, bg='white')
        self.search_results_frame.pack(side='top', fill=BOTH, expand=True, anchor='n')
        # self.search_results_frame.pack_propagate(False)

    def clear_management_pane(self):
        for child in self.management_frame.winfo_children():
            child.destroy()

    def create_search_label(self, message):
        Label(
            self.search_results_frame, text=message, bg='white',
            font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"]
        ).pack()

    def manage_item(self, stock_item, edit):
        for child in self.management_frame.winfo_children():
            child.destroy()

        # self.create_search_label("Add new item:")
        manage_item = ManageItem(self, stock_item, edit)
        management_frame = manage_item.new_item_tile(self.management_frame)
        management_frame.pack(anchor=CENTER, pady=(50, 0))

