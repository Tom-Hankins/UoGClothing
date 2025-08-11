from tkinter import *
from tkinter import ttk
import tkinter as tk
from styles import CUSTOM_FONTS, CUSTOM_COLOURS
from user import UserProfile
from dataaccess import DBAccess
from returns import Return

class SearchReturns(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=CUSTOM_COLOURS["FORM_BACKGROUND"])

        frame = Frame(self, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=50)
        frame.pack(side='top', fill=X, anchor='n')
        frame.pack_propagate(False)
        self.controller = controller

        # List scrolling controls
        self.start_index = 0
        self.end_index = 0
        self.return_details = []
        self.btn_up = ttk.Button()
        self.btn_down = ttk.Button()
        self.table_frame = None

        self.search_label = Label(
            frame, text="Return Status:", bg=CUSTOM_COLOURS["FORM_BACKGROUND"], font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"]
        )
        self.search_label.pack(side='left', padx=(10, 0))

        self.var = StringVar()
        self.search_options = ["Pending", "Returned"]
        s = ttk.Style()
        s.configure('TMenubutton', background=CUSTOM_COLOURS["FORM_BACKGROUND"])
        self.search_options_dropdown = ttk.OptionMenu(
            frame, self.var, "Pending", *self.search_options
        )
        self.search_options_dropdown.pack(side='left', anchor='w', pady=(10, 8), padx=0)

        self.search_button = ttk.Button(frame, text="Search", command=self.search_click)
        self.search_button.pack(side='left', padx=(10, 0))

        # Frame to display search results
        self.results_frame = Frame(self, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        self.results_frame.pack(side='top', fill='both', expand=True, anchor='n')
        self.results_frame.pack_propagate(False)

        if UserProfile.current_user.user_type == "STANDARD":
            self.create_search_label(
                "Search for returned items here.\n\nIf you need to return an item, please search for the order on the "
                "orders tab.\nYou can request a return receipt by clicking 'Return Status'"
            )
        else:
            self.create_search_label(
                "Search for returns here.\n\nPending returns can be checked-in and duplicate return receipts can be"
                "downloaded."
            )

    def search_click(self):
        self.clear_search()
        params = [UserProfile.current_user.user_id, self.var.get()]
        sql = """SELECT stock_order_id, so.receipt_number, so.item_code, s.item_name, so.return_status, so.return_date, 
        o.order_date 
        FROM stock_orders AS so 
        JOIN orders AS o ON so.receipt_number = o.receipt_number
        JOIN stock AS s ON so.item_code = s.item_code 
        WHERE o.user_id = ? AND so.return_status = ?"""

        if UserProfile.current_user.user_type == "SALES":
            params = [self.var.get()]
            sql = """SELECT stock_order_id, so.receipt_number, so.item_code, s.item_name, so.return_status, 
            so.return_date, o.order_date 
            FROM stock_orders AS so 
            JOIN orders AS o ON so.receipt_number = o.receipt_number
            JOIN stock AS s ON so.item_code = s.item_code 
            WHERE so.return_status = ?"""

        db = DBAccess()
        query_result = db.fetch_all_db(sql, params)
        db.close_connection()
        if not query_result:
            self.create_search_label(
                "No item have been returned\n\nItems can be returned from the orders page"
            )
            return
        self.return_details = db.create_object_list(Return, query_result)
        self.create_items()

    def create_items(self):
        frame = Frame(self.results_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], width=900, height=30)
        frame.grid(row=0, column=0)
        frame.grid_propagate(False)

        table_header = Return.create_header_row(self.results_frame)
        table_header.grid(row=1, column=0)

        self.table_frame = Frame(self.results_frame, width=900, height=360, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        self.table_frame.grid(row=2, column=0)

        self.start_index = 0
        self.end_index = len(self.return_details)
        if len(self.return_details) > 9:
            self.end_index = 9

        self.update_table()

        if len(self.return_details) > 9:
            self.btn_up = ttk.Button(self.results_frame, text="↑", command=self.btn_up_click)
            self.btn_down = ttk.Button(self.results_frame, text="↓", command=self.btn_down_click)
            self.btn_down.grid(row=3, column=0, sticky='e', pady=5, padx=(0, 20))

    def update_table(self):
        for i in range(self.start_index, self.end_index):
            row = self.return_details[i].create_line_item(self.table_frame, self)
            row.grid(row=(i + 2), column=0)

    def btn_down_click(self):
        self.start_index += 9

        if self.end_index + 9 > len(self.return_details):
            self.end_index = len(self.return_details)
            self.btn_down.grid_forget()
        else:
            self.end_index += 9

        if self.start_index == 9:
            self.btn_up.grid(row=0, column=0, sticky='e', padx=(0, 20))

        self.clear_table_rows()
        self.update_table()

    def btn_up_click(self):
        if self.end_index == len(self.return_details):
            self.btn_down.grid(row=3, column=0, sticky='e', pady=5, padx=(0, 20))

        self.start_index -= 9
        self.end_index = self.start_index + 9
        if self.start_index == 0:
            self.btn_up.grid_forget()

        self.clear_table_rows()
        self.update_table()

    def clear_table_rows(self):
        for child in self.table_frame.winfo_children():
            child.destroy()

    def clear_search(self):
        # clears the entire search results frame
        for child in self.results_frame.winfo_children():
            child.destroy()

    def create_search_label(self, message):
        Label(
            self.results_frame, text=message, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"],
            font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], anchor='w', justify='left'
        ).grid(row=0, column=0, padx=5, pady=5, columnspan=2)

