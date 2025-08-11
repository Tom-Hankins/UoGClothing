from tkinter import *
from tkinter import messagebox
from styles import CUSTOM_FONTS, CUSTOM_COLOURS
from dataaccess import DBAccess
from user import UserProfile
from window import Window
from formatting import uk_datetime, convert_to_db_datetime
import qrcode
from orders import OrderLineItem
from receipt import OrderReceipt


class ShoppingCart:
    def __init__(self, items, parent):
        self.items = items
        self.display_window = None
        self.parent = parent

    def add_item(self, new_item):
        self.items.append(new_item)

    def remove_item(self, item):
        for i in range(len(self.items)):
            if self.items[i].item_code == item.item_code:
                self.items.pop(i)
                return

    def empty_cart(self):
        self.items.clear()
        self.parent.update_cart()

    def count_items(self, item_type):
        # list comprehension, append any items in the shopping cart that match the item_type to the new list
        counted_items = [x for x in self.items if x.item_code == item_type.item_code]
        return len(counted_items)

    def simplify_cart(self):
        simplified_cart = []
        [simplified_cart.append(x) for x in self.items if x not in simplified_cart]
        return simplified_cart

    def count_all(self):
        return len(self.items)

    def calculate_total_price(self):
        total_price = 0
        for item in self.items:
            if item.offer_price:
                total_price += item.offer_price
            else:
                total_price += item.price
        return round(total_price, 2)

    def place_order(self):
        # Confirm the user wants to proceed with their purchase
        if self.count_all() == 0:
            messagebox.showerror("Empty Basket", "You have no items in your basket")
            return

        msg = f"Are you sure?\n" \
              f"You are about to place an order for {self.count_all()} items.\n" \
              f"Total order cost is £{self.calculate_total_price():.2f}"
        if messagebox.askyesno(title="Place Order", message=msg, parent=self.display_window) == 0:
            return

        order_date = convert_to_db_datetime(uk_datetime())

        db = DBAccess()
        # Create entry in orders table
        params = [UserProfile.current_user.user_id, order_date, "INVOICE REQUIRED"]
        sql = """INSERT INTO orders (user_id, order_date, order_status) VALUES (?, ?, ?)"""
        last_row_id = db.insert(sql, params)

        # Add entry for each item into the stock_orders table
        sql = """INSERT INTO stock_orders (receipt_number, item_code) VALUES (?, ?)"""
        for item in self.items:
            params = [last_row_id, item.item_code]
            db.insert(sql, params)

        # Update stock quantities in the stock table
        sql = """UPDATE stock SET quantity = ? WHERE item_code = ?"""
        for item in self.simplify_cart():
            params = [item.quantity - self.count_items(item), item.item_code]
            item.quantity = item.quantity - self.count_items(item)
            db.update(sql, params)

        # Generate QrCode and save it in the database
        # data = f"{last_row_id} : {order_date}"
        data = """{"ORDER_ID": %s, "ORDER_DATE": %s}""" % (last_row_id, order_date)

        # Encoding data using make() function
        img = qrcode.make(data)
        # Saving as an image file
        # img.save('images/QRCODE.png')
        # img = db.convert_to_blob('images/QRCODE.png')
        img = db.convert_to_blob(img)
        params = [img, last_row_id]
        sql = """UPDATE orders SET qr_code = ? WHERE receipt_number = ?"""
        db.update(sql, params)

        # Query the database for orders and create the orders list
        params = [last_row_id]
        sql = """SELECT stock_orders.receipt_number, orders.order_date, orders.qr_code, stock_orders.item_code, 
        stock.item_name, CASE WHEN stock.offer_price > 0 THEN offer_price ELSE stock.price END, 
        stock_orders.return_status, stock_orders.stock_order_id, stock_orders.return_date, orders.order_status
        FROM orders 
        JOIN stock_orders 
        ON orders.receipt_number = stock_orders.receipt_number 
        JOIN stock 
        ON stock_orders.item_code = stock.item_code 
        WHERE orders.receipt_number = ?"""
        query_result = db.fetch_all_db(sql, params)

        # create object list from search results
        order_details = db.create_object_list(OrderLineItem, query_result)
        receipt = OrderReceipt(order_details, "RECEIPT")
        receipt.generate_receipt()

        db.close_connection()

        # Empty basket
        self.empty_cart()

        # Clear Search field and search results
        self.parent.search_field.delete(0, END)
        self.parent.clear_search()

        # Close shopping basket window any other shopping windows that were opened
        Window.close_windows("BROWSE")

    def view_cart(self, container):
        self.display_window = container
        frame = Frame(container, bg=CUSTOM_COLOURS["FORM_BACKGROUND"])
        frame.pack(side='top', fill='both', expand=True)
        # layout the tiles in two columns
        frame.columnconfigure(1, weight=1)
        Label(
            frame, text="Your Items", bg=CUSTOM_COLOURS["FORM_BACKGROUND"],
            font=CUSTOM_FONTS["LARGE_FONT"]
        ).grid(row=0, column=0, padx=5, pady=5, columnspan=2, sticky='w')

        Label(
            frame, text=f"Total: £{self.calculate_total_price():0.2f}", bg=CUSTOM_COLOURS["FORM_BACKGROUND"],
            font=CUSTOM_FONTS["LARGE_FONT"]
        ).grid(row=0, column=1, padx=5, pady=5, columnspan=2, sticky='e')

        order_label = Label(
            frame, text=f"Place Order", bg=CUSTOM_COLOURS["FORM_BACKGROUND"],
            font=CUSTOM_FONTS["LARGE_FONT_UNDERLINE"], fg=CUSTOM_COLOURS["CLICKABLE_LINK"], cursor="hand2"
        )
        order_label.grid(row=1, column=1, padx=5, pady=5, columnspan=2, sticky='ne')
        order_label.bind("<Button-1>", lambda event: self.place_order())

        # Add item tiles to shopping basket view
        if self.items:
            for i in range(len(self.simplify_cart())):
                col = 1
                if i % 2 == 0:
                    col = 0
                item_tile = self.simplify_cart()[i].create_tile(frame)
                item_tile.grid(row=int(i/2) + 2, column=col)
        else:
            # Display nothing in basket
            Label(
                frame, text="Your basket is empty", bg=CUSTOM_COLOURS["FORM_BACKGROUND"],
                font=CUSTOM_FONTS["LARGE_FONT"]
            ).grid(row=0, column=0)
