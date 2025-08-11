from styles import CUSTOM_FONTS, CUSTOM_COLOURS
from tkinter import *
from receipt import OrderReceipt, ReturnReceipt
from dataaccess import DBAccess
from tkinter import messagebox, ttk
import formatting

class Order:
    def __init__(self, receipt_number, order_date, qr_code):
        self.receipt_number = receipt_number
        self.order_date = order_date
        self.qr_code = qr_code

class OrderSummary:
    def __init__(self, receipt_number, order_date, email_address, total, items):
        self.receipt_number = receipt_number
        self.order_date = formatting.convert_from_db_datetime(order_date)
        self.email_address = email_address
        self.total = round(total, 2)
        self.items = items

    @staticmethod
    def create_table_header(container, table_type="INVOICE REQUIRED"):
        header_frame = Frame(
            container, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=41, width=900, pady=1, padx=20
        )
        header_frame.grid_propagate(False)

        # Item Code
        receipt_num_frame = Frame(
            header_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=40, width=80, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        receipt_num_frame.grid(row=0, column=0)
        receipt_num_frame.pack_propagate(False)
        receipt_num_label = Label(
            receipt_num_frame, text=f"Receipt Number", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"], anchor='w', justify='left', wraplength=80
        )
        receipt_num_label.pack(side="left")

        # Date
        date_frame = Frame(
            header_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=40, width=180, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        date_frame.grid(row=0, column=1)
        date_frame.pack_propagate(False)
        date_label = Label(
            date_frame, text=f"Order Placed", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )
        date_label.pack(expand=True)

        # Email Address
        email_frame = Frame(
            header_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=40, highlightbackground='black',
            highlightthickness=1, width=350 if table_type == "INVOICE REQUIRED" else 430, padx=10

        )
        email_frame.grid(row=0, column=2)
        email_frame.pack_propagate(False)
        email_label = Label(
            email_frame, text=f"Email Address", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"], border=True, borderwidth=1
        )
        email_label.pack(expand=True)

        # Total
        total_frame = Frame(
            header_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=40, width=100, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        total_frame.grid(row=0, column=3)
        total_frame.pack_propagate(False)
        total_label = Label(
            total_frame, text=f"Order Total", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"], border=True, borderwidth=1, anchor='w', justify='left', wraplength=100
        )
        total_label.pack(side="left")

        # items
        items_frame = Frame(
            header_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=40, width=70, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        items_frame.grid(row=0, column=4)
        items_frame.pack_propagate(False)
        items_label = Label(
            items_frame, text=f"Items", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"], border=True, borderwidth=1, anchor='w', justify='left', wraplength=100
        )
        items_label.pack(side="left")

        # Create Invoice
        if table_type == "INVOICE REQUIRED":
            create_invoice_frame = Frame(
                header_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=40, width=80, padx=10,
                highlightbackground='black', highlightthickness=1
            )
            create_invoice_frame.grid(row=0, column=5)
            create_invoice_frame.pack_propagate(False)

            create_invoice_label = Label(
                create_invoice_frame, text=f"Create Invoice", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
                bg=CUSTOM_COLOURS["FORM_BACKGROUND"], border=True, borderwidth=1, anchor='w', justify='left', wraplength=80
            )
            create_invoice_label.pack(side="left")

        return header_frame

    def create_row(self, container, controller, table_type="INVOICE REQUIRED"):
        row_frame = Frame(
            container, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=31, width=900, pady=1, padx=20
        )
        row_frame.grid_propagate(False)

        # Item Code
        receipt_num_frame = Frame(
            row_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=30, width=80, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        receipt_num_frame.grid(row=0, column=0)
        receipt_num_frame.pack_propagate(False)
        receipt_num_label = Label(
            receipt_num_frame, text=f"{self.receipt_number}", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"], anchor='w'
        )
        receipt_num_label.pack(expand=True)

        # Date
        date_frame = Frame(
            row_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=30, width=180, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        date_frame.grid(row=0, column=1)
        date_frame.pack_propagate(False)
        date_label = Label(
            date_frame, text=f"{self.order_date}", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )
        date_label.pack(expand=True)

        # Email Address
        email_frame = Frame(
            row_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=30, highlightbackground='black',
            highlightthickness=1, width=350 if table_type == "INVOICE REQUIRED" else 430, padx=10
        )
        email_frame.grid(row=0, column=2)
        email_frame.pack_propagate(False)
        email_label = Label(
            email_frame, text=f"{self.email_address}", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"], border=True, borderwidth=1
        )
        email_label.pack(side='left')

        # Total
        total_frame = Frame(
            row_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=30, width=100, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        total_frame.grid(row=0, column=3)
        total_frame.pack_propagate(False)
        total_label = Label(
            total_frame, text=f"£{round(self.total, 2):.2f}", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"], border=True, borderwidth=1, anchor='w', justify='left', wraplength=100
        )
        total_label.pack(side="left")

        # items
        items_frame = Frame(
            row_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=30, width=70, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        items_frame.grid(row=0, column=4)
        items_frame.pack_propagate(False)
        items_label = Label(
            items_frame, text=f"{self.items}", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"], border=True, borderwidth=1, anchor='w', justify='left', wraplength=100
        )
        items_label.pack(side="left")

        if table_type == "INVOICE REQUIRED":
            # Create Invoice
            create_invoice_frame = Frame(
                row_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=30, width=80, padx=10,
                highlightbackground='black', highlightthickness=1
            )
            create_invoice_frame.grid(row=0, column=5)
            create_invoice_frame.pack_propagate(False)

            create_invoice_btn = ttk.Button(
                create_invoice_frame, text="Create", command=lambda: self.create_invoice(controller)
            )
            create_invoice_btn.pack(pady=2)

        return row_frame

    def create_invoice(self, controller):
        if messagebox.askyesno("Create Invoice?", "Please confirm goods have been dispatched.") == 0:
            return

        db = DBAccess()
        params = [self.receipt_number]

        sql = """UPDATE orders SET order_status = "INVOICED" WHERE receipt_number = ?"""
        db.update(sql, params)

        sql = """SELECT so.receipt_number, o.order_date, o.qr_code, so.item_code, s.item_name, 
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
                 WHERE so.receipt_number = ?"""

        query_result = db.fetch_all_db(sql, params)
        invoice_details = db.create_object_list(OrderLineItem, query_result)
        receipt = OrderReceipt(invoice_details, "INVOICE")
        receipt.generate_receipt()

        db.close_connection()
        controller.search_click()

class OrderLineItem(Order):
    def __init__(self, receipt_number, order_date, qr_code, item_code, item_name, price, return_status, stock_order_id,
                 return_date, order_status):
        super().__init__(receipt_number, order_date, qr_code)
        self.stock_order_id = stock_order_id
        self.return_date = return_date
        self.receipt_number = receipt_number
        self.order_date = order_date
        self.order_status = order_status
        self.return_status = return_status
        self.qr_code = qr_code
        self.item_code = item_code
        self.item_name = item_name
        self.price = price
        self.order_list = []

        # UI widgets that need to be created and altered dynamically
        self.item_return_label = None

    def create_page_header(self, container):
        item_frame = Frame(
            container, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=50, width=900, pady=1, padx=1
        )
        item_frame.pack_propagate(False)

        order_number_label = Label(
            item_frame, text=f"Order Number: {self.receipt_number}", font=CUSTOM_FONTS["LARGE_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]
        )
        order_number_label.pack(side="left", padx=(20, 0))

        receipt_label = Label(
            item_frame, text=f"Receipt", font=CUSTOM_FONTS["LARGE_FONT_UNDERLINE"],
            fg=CUSTOM_COLOURS["CLICKABLE_LINK"], bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], cursor='hand2'
        )
        receipt_label.pack(side="left", padx=(20, 0))
        receipt_label.bind("<Button-1>", lambda event: self.item_click("RECEIPT"))

        spacer_frame = Frame(item_frame, width=100, height=50, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        spacer_frame.pack(side='left')

        if self.order_status == "INVOICED":
            invoice_label = Label(
                spacer_frame, text=f"Invoice", font=CUSTOM_FONTS["LARGE_FONT_UNDERLINE"],
                fg=CUSTOM_COLOURS["CLICKABLE_LINK"], bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], cursor='hand2'
            )
            invoice_label.pack(side="left", padx=(20, 0))
            invoice_label.bind("<Button-1>", lambda event: self.item_click("INVOICE"))

        order_date_label = Label(
            item_frame,
            text=f"Order Date: {formatting.convert_from_db_datetime(self.order_date)[0:10]} @ "
                 f"{formatting.convert_from_db_datetime(self.order_date)[11:]}",
            font=CUSTOM_FONTS["LARGE_FONT"], bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]
        )
        order_date_label.pack(side="right", padx=(0, 20))

        return item_frame

    @staticmethod
    def create_table_header(container):
        item_frame = Frame(
            container, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=31, width=900, pady=1, padx=20
        )
        item_frame.grid_propagate(False)

        # Item Code
        item_code_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=30, width=90, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        item_code_frame.grid(row=0, column=0)
        item_code_frame.pack_propagate(False)
        item_code_label = Label(
            item_code_frame, text=f"Item Code", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )
        item_code_label.pack(side="left")

        # Item Name
        item_name_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=30, width=510, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        item_name_frame.grid(row=0, column=1)
        item_name_frame.pack_propagate(False)
        item_name_label = Label(
            item_name_frame, text=f"Description", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )
        item_name_label.pack(side="left")

        # Item Price
        item_price_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=30, width=90, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        item_price_frame.grid(row=0, column=2)
        item_price_frame.pack_propagate(False)
        item_price_label = Label(
            item_price_frame, text=f"Price", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"], border=True, borderwidth=1
        )
        item_price_label.pack(side="left")

        # Return
        item_return_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=30, width=170, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        item_return_frame.grid(row=0, column=3)
        item_return_frame.pack_propagate(False)
        item_return_label = Label(
            item_return_frame, text=f"Return Status", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"], border=True, borderwidth=1
        )
        item_return_label.pack(side="left")

        return item_frame

    def create_line_item(self, container):
        item_frame = Frame(
            container, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=30, width=900, padx=20
        )
        item_frame.grid_propagate(False)

        # Item Code
        item_code_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=30, width=90, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        item_code_frame.grid(row=0, column=0)
        item_code_frame.pack_propagate(False)
        item_code_label = Label(
            item_code_frame, text=f"{self.item_code}", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]
        )
        item_code_label.pack(side="left")

        # Item Name
        item_name_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=30, width=510, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        item_name_frame.grid(row=0, column=1)
        item_name_frame.pack_propagate(False)
        item_name_label = Label(
            item_name_frame, text=f"{self.item_name[0:70]}", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]
        )
        item_name_label.pack(side="left")

        # Item Price
        item_price_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=30, width=90, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        item_price_frame.grid(row=0, column=2)
        item_price_frame.pack_propagate(False)
        item_price_label = Label(
            item_price_frame, text=f"£{self.price:.2f}", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]
        )
        item_price_label.pack(side="left")

        # Return
        item_return_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=30, width=170, padx=10,
            highlightbackground='black', highlightthickness=1,
            cursor="hand2" if self.return_status != 'Returned' else "arrow"
        )
        item_return_frame.grid(row=0, column=3)
        item_return_frame.pack_propagate(False)
        item_return_frame.bind("<Button-1>", lambda event: self.return_click())

        self.item_return_label = Label(
            item_return_frame, text=f"{'-' if not self.return_status else self.return_status + '-' + self.return_date}",
            font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], border=True,
            borderwidth=1
        )
        self.item_return_label.pack(side="left")
        self.item_return_label.bind("<Button-1>", lambda event: self.return_click())

        return item_frame

    def return_click(self):
        # Returned items cannot be changed
        if self.return_status == 'Returned':
            return

        # Confirm user wishes to proceed with the return / cancellation of return
        if self.return_status == 'Pending':
            if messagebox.askyesno(
                    title="Confirmation",
                    message="Please confirm that you wish to cancel returning this item.",
                    parent=None
            ) == 0:
                return
            else:
                self.cancel_return()
        else:
            if messagebox.askyesno(
                    title="Confirmation",
                    message="Please confirm that you wish to return this item.",
                    parent=None
            ) == 0:
                return
            else:
                self.return_item()

    def cancel_return(self):
        # Send confirmation of cancellation

        # Update Database to set the return status to pending
        db = DBAccess()
        params = ("", "", self.stock_order_id)
        sql = "UPDATE stock_orders SET return_status = ?, return_date = ? WHERE stock_order_id = ?"
        db.update(sql, params)
        db.close_connection()

        # Refresh the label and update the object
        self.item_return_label['text'] = "Return Cancelled"
        self.return_status = ''
        self.return_date = ''

    def return_item(self):
        # Update Database to set the return status to pending
        db = DBAccess()
        return_date = formatting.uk_date()
        params = ("Pending", return_date, self.stock_order_id)
        sql = "UPDATE stock_orders SET return_status = ?, return_date = ? WHERE stock_order_id = ?"
        db.update(sql, params)
        db.close_connection()

        # Refresh the label and update the object
        self.item_return_label['text'] = f"Pending-{return_date}"
        self.return_status = 'Pending'
        self.return_date = return_date

        # Generate a return receipt with tear off section on the bottom (to include with return parcel)
        receipt = ReturnReceipt(self)
        receipt.generate_receipt()

    def item_click(self, pdf_type):
        receipt = OrderReceipt(self.order_list, pdf_type)
        receipt.generate_receipt()


