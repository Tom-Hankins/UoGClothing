from styles import CUSTOM_FONTS, CUSTOM_COLOURS
from tkinter import *
from tkinter import ttk, messagebox
from user import UserProfile
import formatting as fm
from dataaccess import DBAccess
from receipt import ReturnReceipt

class Return:
    def __init__(self, stock_order_id, receipt_number, item_code, item_name, return_status, return_date, order_date):
        self.stock_order_id = stock_order_id
        self.order_number = receipt_number
        self.item_code = item_code
        self.item_name = item_name
        self.return_status = return_status
        self.return_date = return_date
        self.order_date = order_date

    @staticmethod
    def create_header_row(container):
        item_frame = Frame(
            container, bg='white', height=60, width=900, padx=20
        )
        item_frame.grid_propagate(False)

        # Returns Number (RMA)
        return_id_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=60, width=90, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        return_id_frame.grid(row=0, column=0)
        return_id_frame.pack_propagate(False)
        return_id_label = Label(
            return_id_frame, text=f"Returns Number", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"], wraplength=100, anchor='w'
        )
        return_id_label.pack(side="left")

        # Order Number
        order_number_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=60, width=90, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        order_number_frame.grid(row=0, column=1)
        order_number_frame.pack_propagate(False)
        order_number_label = Label(
            order_number_frame, text=f"Order Number", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"], wraplength=85, anchor='w', justify='left'
        )
        order_number_label.pack(side="left")

        # Item Code
        item_code_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=60, width=80, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        item_code_frame.grid(row=0, column=2)
        item_code_frame.pack_propagate(False)
        item_code_label = Label(
            item_code_frame, text=f"Item Code", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"], wraplength=65, anchor='w', justify='left'
        )
        item_code_label.pack(side="left")

        # Item Name
        item_name_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=60, width=300, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        item_name_frame.grid(row=0, column=3)
        item_name_frame.pack_propagate(False)
        item_name_label = Label(
            item_name_frame, text=f"Description", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )
        item_name_label.pack(expand=True)

        # Order Date
        order_date_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=60, width=100, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        order_date_frame.grid(row=0, column=4)
        order_date_frame.pack_propagate(False)
        order_date_label = Label(
            order_date_frame, text=f"Order Date", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"], wraplength=100
        )
        order_date_label.pack(side="left")

        # Return Date
        return_date_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=60, width=100, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        return_date_frame.grid(row=0, column=5)
        return_date_frame.pack_propagate(False)
        return_date_label = Label(
            return_date_frame, text=f"Return Date", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"], wraplength=100
        )
        return_date_label.pack(side="left")

        # Returns Status
        return_status_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=60, width=100, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        return_status_frame.grid(row=0, column=6)
        return_status_frame.pack_propagate(False)
        return_status_label = Label(
            return_status_frame, text=f"Status", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )
        return_status_label.pack(expand=True)

        return item_frame

    def create_line_item(self, container, controller):
        item_frame = Frame(
            container, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=40, width=900, padx=20
        )
        item_frame.grid_propagate(False)

        # Returns Number (RMA)
        return_id_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=40, width=90, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        return_id_frame.grid(row=0, column=0)
        return_id_frame.pack_propagate(False)

        return_id_label = Label(
            return_id_frame, text=f"{self.stock_order_id}", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]
        )
        if self.return_status == "Pending":
            return_id_label = Label(
                return_id_frame, text=f"{self.stock_order_id}", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT_LINK"],
                fg=CUSTOM_COLOURS["CLICKABLE_LINK"], bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], cursor='hand2'
            )
            return_id_label.bind("<Button 1>", self.return_click)
        return_id_label.pack(side="left")

        # Order Number
        order_number_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=40, width=90, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        order_number_frame.grid(row=0, column=1)
        order_number_frame.pack_propagate(False)
        order_number_label = Label(
            order_number_frame, text=f"{self.order_number}", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]
        )
        order_number_label.pack(side="left")

        # Item Code
        item_code_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=40, width=80, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        item_code_frame.grid(row=0, column=2)
        item_code_frame.pack_propagate(False)
        item_code_label = Label(
            item_code_frame, text=f"{self.item_code}", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]
        )
        item_code_label.pack(side="left")

        # Item Name
        item_name_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=40, width=300, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        item_name_frame.grid(row=0, column=3)
        item_name_frame.pack_propagate(False)
        item_name_label = Label(
            item_name_frame, text=f"{self.item_name[0:80]}", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], wraplength=285, anchor='w', justify='left'
        )
        item_name_label.pack(side="left")

        # Order Date
        order_date_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=40, width=100, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        order_date_frame.grid(row=0, column=4)
        order_date_frame.pack_propagate(False)
        order_date_label = Label(
            order_date_frame,
            text=f"{fm.db_datetime_to_date_only(self.order_date)}",
            font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]
        )
        order_date_label.pack(side="left")

        # Return Date
        return_date_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=40, width=100, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        return_date_frame.grid(row=0, column=5)
        return_date_frame.pack_propagate(False)
        return_date_label = Label(
            return_date_frame, text=f"{self.return_date}", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]
        )
        return_date_label.pack(side="left")

        # Returns Status
        return_status_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=40, width=100, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        return_status_frame.grid(row=0, column=6)
        return_status_frame.pack_propagate(False)

        if UserProfile.current_user.user_type == "STANDARD" or self.return_status == "Returned":
            return_status_label = Label(
                return_status_frame, text=f"{self.return_status}", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
                bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]
            )
            return_status_label.pack(side="left")
        else:
            return_button = ttk.Button(
                return_status_frame, text="Return Item", command=lambda: self.return_item(controller)
            )
            return_button.pack(expand=True)

        return item_frame

    def return_click(self, *args):
        receipt = ReturnReceipt(self)
        receipt.generate_receipt()

    def return_item(self, controller):
        if messagebox.askyesno(
                "Return Item?", "The item will be returned to stock\n\nConfirm item has been returned?") == 0:
            return
        db = DBAccess()
        params = [self.stock_order_id]
        sql = """UPDATE stock_orders SET return_status = 'Returned' WHERE stock_order_id = ?"""
        db.update(sql, params)

        params = [self.item_code]
        sql = """SELECT quantity FROM stock WHERE item_code = ?"""
        query_result = db.fetch_one_db(sql, params)
        qty = query_result[0] + 1

        params = [qty, self.item_code]
        sql = """UPDATE stock SET quantity = ? WHERE item_code = ?"""
        db.update(sql, params)

        db.close_connection()
        controller.search_click()



