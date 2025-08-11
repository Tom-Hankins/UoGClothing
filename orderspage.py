from tkinter import *
from tkinter import ttk
import tkinter as tk
from styles import CUSTOM_FONTS, CUSTOM_COLOURS
from orders import OrderLineItem, OrderSummary
from user import UserProfile
from dataaccess import DBAccess
from qr import Scan

class SearchOrders(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=CUSTOM_COLOURS["FORM_BACKGROUND"])

        frame = Frame(self, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=50)
        frame.pack(side='top', fill=X, anchor='n')
        frame.pack_propagate(False)
        self.controller = controller

        # List scrolling controls
        self.start_index = 0
        self.end_index = 0
        self.order_summaries = []
        self.btn_up = ttk.Button()
        self.btn_down = ttk.Button()

        # Frame to display search results
        self.results_frame = Frame(self, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        self.results_frame.pack(side='top', fill='both', expand=True, anchor='n')
        self.results_frame.pack_propagate(False)
        self.table_frame = None

        # QrScanner Viewer
        self.qr_scanner = None
        self.scanner_frame = Label(self.results_frame)

        if UserProfile.current_user.user_type == "STANDARD":
            # QrScanner Image
            self.scanner_img = PhotoImage(file="images/QRCode50x50.png")
            self.scanner_img_scanning = PhotoImage(file="images/QRCode50x50_SCAN.png")
            self.scanner_img_canvas = Canvas(
                frame, height=50, width=60, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], highlightthickness=0, cursor="hand2"
            )
            self.scanner_img_canvas.pack(anchor='nw', side='right', padx=20)
            self.scanner_img_canvas.create_image(0, 0, image=self.scanner_img, anchor='nw', tags="scan_img")
            self.scanner_img_canvas.bind("<Button-1>", lambda event: self.scan_qr())

            self.search_label = Label(
                frame, text="Search:", bg=CUSTOM_COLOURS["FORM_BACKGROUND"], font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"]
            )
            self.search_label.pack(side='left', padx=(10, 0))
            self.search_field = Entry(frame, width=40)
            self.search_field.pack(side='left', padx=(10, 0))

            self.create_search_label(
                "Search for your orders here.\n\n"
                "Search by order number of click the QrCode button to scan your order QrCode.\n\n"
                "Receipts and Invoices can be downloaded here and returns can be requested by clicking "
                "'Return Status'"
            )

        elif UserProfile.current_user.user_type == "SALES":
            self.search_label = Label(
                frame, text="Search:", bg=CUSTOM_COLOURS["FORM_BACKGROUND"], font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"]
            )
            self.search_label.pack(side='left', padx=(10, 0))

            self.var = StringVar()
            self.search_options = ["Invoice Required", "Invoiced"]
            s = ttk.Style()
            s.configure('TMenubutton', background=CUSTOM_COLOURS["FORM_BACKGROUND"])
            self.search_options_dropdown = ttk.OptionMenu(
                frame, self.var, "Invoice Required", *self.search_options
            )
            self.search_options_dropdown.pack(side='left', anchor='w', pady=(10, 8), padx=0)

            self.create_search_label(
                "Search for customer orders here.\n\n"
                "Invoices can be generated and downloaded by clicking the create invoice button.\n\n"
                "Once an invoice is generated customers can view these through their log-in."
            )

        self.search_button = ttk.Button(frame, text="Search", command=self.search_click)
        self.search_button.pack(side='left', padx=(10, 0))

    def scan_qr(self):
        if not self.qr_scanner:  # Don't run if the scanner is already open
            self.scanner_img_canvas.delete('scan_img')
            self.scanner_img_canvas.create_image(0, 0, image=self.scanner_img_scanning, anchor='nw', tags="scan_img")
            self.scanner_frame = Label(self.results_frame)
            self.scanner_frame.grid(row=0, column=0, padx=5, pady=5, columnspan=2, sticky='NSEW')
            self.qr_scanner = Scan(self.scanner_frame)
            result = self.qr_scanner.get_result()

            # format result of QrScan - If it's a valid QrCode it will return a search result
            if result:
                start = result.find(":") + 1
                end = result.find(",")
                order_num = result[start:end]
                o_num = order_num.strip()
                self.search_field.delete(0, END)
                self.search_field.insert(0, str(o_num))
                self.search_click()

        self.remove_scanner()

    def remove_scanner(self):
        if self.qr_scanner:
            # End the Scan loop and close the scanner
            self.qr_scanner.run_loop = False
            self.qr_scanner.close_scanner()
            # destroy the Scan object
            del self.qr_scanner
            self.qr_scanner = None
            self.scanner_frame.grid_forget()
            self.scanner_img_canvas.delete('scan_img')
            self.scanner_img_canvas.create_image(0, 0, image=self.scanner_img, anchor='nw', tags="scan_img")

    def search_click(self):
        self.remove_scanner()
        self.clear_search()

        if UserProfile.current_user.user_type == "STANDARD":
            db = DBAccess()
            # Query the database for orders that match the order number for the current user
            # This query checks whether the item has a special offer price applied and also checks the price_changes
            # table for historic pricing as historic invoices and orders must display the price the item was when it was
            # ordered
            params = [UserProfile.current_user.user_id, self.search_field.get()]
            sql = """SELECT so.receipt_number, o.order_date, o.qr_code, so.item_code, 
            s.item_name, 
            CASE WHEN pc.valid_to > o.order_date THEN pc.price ELSE
            CASE WHEN s.offer_price > 0 THEN s.offer_price ELSE s.price END END AS price,
            so.return_status, so.stock_order_id, so.return_date, o.order_status
            FROM orders AS o
            JOIN stock_orders AS so
            ON o.receipt_number = so.receipt_number 
            JOIN stock AS s
            ON so.item_code = s.item_code
            LEFT JOIN price_changes AS pc
            ON so.item_code = pc.item_code 
            AND o.order_date BETWEEN pc.valid_to AND pc.valid_from
            WHERE o.user_id = ? AND o.receipt_number = ?"""
            query_result = db.fetch_all_db(sql, params)
            db.close_connection()
            if not query_result:
                self.create_search_label("Order Number Not Found")
                return
            # create object list from search results
            order_details = db.create_object_list(OrderLineItem, query_result)
            order_details[0].order_list = order_details
            self.create_standard_items(order_details)

        if UserProfile.current_user.user_type == "SALES":
            db = DBAccess()
            # Search for all invoices with status of invoice required. These are invoices that need to be dispatched and
            # require the invoice to be raised.
            params = [self.var.get().upper()]
            sql = """SELECT t.receipt_number, t.order_date, t.email_address, SUM(new_price) AS total, 
                     COUNT(new_price) AS items
                     FROM(SELECT so.receipt_number, o.order_date, u.email_address,
                     CASE WHEN pc.valid_to > o.order_date THEN pc.price ELSE
                     CASE WHEN s.offer_price > 0 THEN s.offer_price ELSE s.price END END AS new_price
                     FROM orders AS o
                     JOIN users AS u
                     ON o.user_id = u.user_id
                     JOIN stock_orders AS so
                     ON o.receipt_number = so.receipt_number 
                     JOIN stock AS s
                     ON so.item_code = s.item_code
                     LEFT JOIN price_changes AS pc
                     ON so.item_code = pc.item_code 
                     AND o.order_date BETWEEN pc.valid_to AND pc.valid_from
                     WHERE order_status = ?) t GROUP BY receipt_number;"""
            query_result = db.fetch_all_db(sql, params)

            db.close_connection()
            if not query_result:
                if self.var.get() == "Invoice Required":
                    self.create_search_label("No Outstanding Orders Found")
                else:
                    self.create_search_label("No Orders Found")
                return

            self.order_summaries = db.create_object_list(OrderSummary, query_result)

            self.create_sales_items()

    def create_sales_items(self):
        frame = Frame(self.results_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], width=900, height=30)
        frame.grid(row=0, column=0)
        frame.grid_propagate(False)

        header_row = OrderSummary.create_table_header(self.results_frame, self.var.get().upper())
        header_row.grid(row=1, column=0)

        self.table_frame = Frame(self.results_frame, width=900, height=360, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        self.table_frame.grid(row=2, column=0)

        self.start_index = 0
        self.end_index = len(self.order_summaries)
        if len(self.order_summaries) > 12:
            self.end_index = 12

        self.update_table()

        if len(self.order_summaries) > 12:
            self.btn_up = ttk.Button(self.results_frame, text="↑", command=self.btn_up_click)
            self.btn_down = ttk.Button(self.results_frame, text="↓", command=self.btn_down_click)
            self.btn_down.grid(row=3, column=0, sticky='e', pady=5, padx=(0, 20))

    def update_table(self):
        for i in range(self.start_index, self.end_index):
            row = self.order_summaries[i].create_row(self.table_frame, self, self.var.get().upper())
            row.grid(row=(i + 2), column=0)

    def clear_table_rows(self):
        for child in self.table_frame.winfo_children():
            child.destroy()

    def btn_down_click(self):
        self.start_index += 12
        if self.end_index + 12 > len(self.order_summaries):
            self.end_index = len(self.order_summaries)
            self.btn_down.grid_forget()
        else:
            self.end_index += 12

        if self.start_index == 12:
            self.btn_up.grid(row=0, column=0, sticky='e', padx=(0, 20))

        self.clear_table_rows()
        self.update_table()

    def btn_up_click(self):
        if self.end_index == len(self.order_summaries):
            self.btn_down.grid(row=3, column=0, sticky='e', pady=5, padx=(0, 20))

        self.start_index -= 12
        self.end_index = self.start_index + 12
        if self.start_index == 0:
            self.btn_up.grid_forget()

        self.clear_table_rows()
        self.update_table()

    def create_standard_items(self, order_details):
        page_header = order_details[0].create_page_header(self.results_frame)
        page_header.grid(row=0, column=0)
        header_row = OrderLineItem.create_table_header(self.results_frame)
        header_row.grid(row=1, column=0)

        for i in range(len(order_details)):
            row = order_details[i].create_line_item(self.results_frame)
            row.grid(row=(i+2), column=0)

    def clear_search(self):
        # clears the entire search results frame
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
