from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from styles import CUSTOM_FONTS, CUSTOM_COLOURS
from window import Window
from shoppingcart import ShoppingCart
from customwidgets import ImageCarousel
import formatting
import io
from dataaccess import DBAccess

class StockItem(ShoppingCart):
    def __init__(self, items, parent, item_code=0, item_name='', quantity=0, price=0, offer_price=0, is_available=0,
                 images=None, img_carousel=False):
        super().__init__(items, parent)

        if images is None:
            self.images = [None]

        self.img_carousel = img_carousel
        self.item_code = item_code
        self.parent = parent
        self.item_name = item_name
        self.quantity = quantity
        self.price = price
        self.offer_price = offer_price
        self.is_available = is_available
        self.current_image_index = 1

        # Thumbnail is generated in the get_item_images() method
        self.thumbnail_image = None
        self.small_thumbnail = None
        self.offer_banner_img = ImageTk.PhotoImage(Image.open("images/offer_banner.png"))
        self.offer_banner_large_img = ImageTk.PhotoImage(Image.open("images/offer_banner_large.png"))
        self.not_found_img = None
        self.current_image = None
        self.images = self.get_item_images()

        # UI widgets that need to be created and altered dynamically
        self.item_in_cart_label = None
        self.item_quantity_label = None
        self.item_quantity = None
        self.in_basket_label = None
        self.btn_add_to_cart = None
        self.btn_remove_from_cart = None
        self.item_image_label = None

        if not self.img_carousel:
            self.item_image_number_label = None

    def set_mode(self):
        self.img_carousel = True

    def get_item_images(self):
        # Get images
        db = DBAccess()
        params = [self.item_code]
        sql = """SELECT image FROM stock_images WHERE item_code = ?"""
        img_matched = db.fetch_all_db(sql, params)
        # create and return a list of all the images found
        image_list = []

        for i in range(len(img_matched)):
            (img) = img_matched[i]
            img1 = Image.open(io.BytesIO(img[0]))
            img1 = img1.resize((512, 512), Image.ANTIALIAS)
            image_list.append(img1)

            if i == 0:
                self.thumbnail_image = img1.resize((140, 140), Image.ANTIALIAS)
                self.thumbnail_image = ImageTk.PhotoImage(self.thumbnail_image)
                self.small_thumbnail = img1.resize((76, 76), Image.ANTIALIAS)
                self.small_thumbnail = ImageTk.PhotoImage(self.small_thumbnail)
                self.current_image = img1.resize((512, 512), Image.ANTIALIAS)
                self.current_image = ImageTk.PhotoImage(self.current_image)

        # if no images found, create placeholders
        if not image_list:
            self.thumbnail_image = ImageTk.PhotoImage(Image.open("images/not_found.png").resize((140, 140)))
            self.small_thumbnail = ImageTk.PhotoImage(Image.open("images/not_found.png").resize((76, 76)))

        if not image_list and not self.img_carousel:
            blob_image = db.convert_to_blob(Image.open("images/not_found.png"))
            blob_image = Image.open(io.BytesIO(blob_image))
            self.not_found_img = blob_image.resize((512, 512), Image.ANTIALIAS)
            image_list.append(self.not_found_img)
            self.current_image = ImageTk.PhotoImage(self.not_found_img)

        db.close_connection()
        return image_list

    def create_tile(self, container):
        item_frame = Frame(
            container, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=150, width=450, cursor='hand2', pady=1, padx=1
        )
        # item_frame.pack(side='top', anchor='nw')
        # Line above was working when creating tiles from searchproducts.py but failed in shoppingcart.py - WHY????
        item_frame.grid_propagate(False)
        item_frame.bind("<Button-1>", self.item_click)

        item_name = Label(
            item_frame, padx=5,
            text=f"Name: {self.item_name if len(self.item_name) < 28 else self.item_name[0:25].strip() + '...'}",
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"], width=30, font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], anchor='w',
        )
        item_name.grid(row=0, column=0)
        item_name.bind("<Button-1>", self.item_click)

        item_code = Label(
            item_frame, text=f"Item Code: IC-{self.item_code}", bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], width=30,
            font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], anchor='w', padx=5
        )
        item_code.grid(row=1, column=0)
        item_code.bind("<Button-1>", self.item_click)

        self.item_quantity = Label(
            item_frame, text=f"In Stock: {self.quantity - self.items.count_items(self)}",
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], width=30, font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], anchor='w',
            padx=5
        )
        self.item_quantity.grid(row=2, column=0)
        self.item_quantity.bind("<Button-1>", self.item_click)

        item_price = Label(
            item_frame, text=f"£{self.price:.2f}" if not self.offer_price
            else f"Was £{self.price:.2f} Now Only £{self.offer_price:.2f}!",
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], width=30,
            font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], anchor='w', padx=5
        )
        item_price.grid(row=3, column=0)
        item_price.bind("<Button-1>", self.item_click)

        self.in_basket_label = Label(
            item_frame, text=f"Number in Basket: {self.items.count_items(self)}",
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], width=30, font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], anchor='w',
            padx=5
        )
        self.in_basket_label.grid(row=4, column=0)
        self.in_basket_label.bind("<Button-1>", self.item_click)

        item_image_thumbnail = Label(item_frame, image=self.thumbnail_image)
        item_image_thumbnail.grid(row=0, column=1, rowspan=5, pady=4, padx=(10, 0))
        item_image_thumbnail.bind("<Button-1>", self.item_click)

        if self.offer_price:
            item_offer_banner = Label(item_frame, image=self.offer_banner_large_img)
            item_offer_banner.grid(row=0, column=2, rowspan=5)

        # return the item frame, allows overriding the default "item_frame.pack(side='top', anchor='nw')"
        return item_frame

    def admin_item_tile(self, container, parent):
        item_frame = Frame(
            container, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=82, width=300, pady=1, padx=2,
            highlightthickness=2, highlightcolor=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )
        item_frame.grid_propagate(False)

        item_description_frame = Frame(item_frame, width=194, height=48, padx=3)
        item_description_frame.grid(row=0, column=0, columnspan=3)
        item_description_frame.grid_propagate(False)

        item_description_label = Label(
            item_description_frame, font=CUSTOM_FONTS["VERY_SMALL_FONT"] if self.is_available else
            CUSTOM_FONTS["PRODUCT_UNAVAILABLE_FONT"], bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"],
            text=f"{self.item_name if len(self.item_name) < 76 else self.item_name[0:73] + '...'}", wraplength=185,
            justify=LEFT
        )
        item_description_label.grid(row=0, column=0, sticky='w')

        item_code_frame = Frame(item_frame, width=64, height=26, bg='green')
        item_code_frame.grid(row=1, column=0)
        item_code_label = Label(item_code_frame, text=f"IC-{self.item_code}", justify=LEFT)
        item_code_label.pack(expand=True)

        item_price_frame = Frame(item_frame, width=64, height=26, bg='blue')
        item_price_frame.grid(row=1, column=1)
        item_price_label = Label(
            item_price_frame, text=f"£{self.price:.2f}" if not self.offer_price else f"£{self.offer_price:.2f}",
            justify=CENTER
        )
        item_price_label.pack(expand=True)

        item_qty_frame = Frame(item_frame, width=64, height=26, bg='yellow')
        item_qty_frame.grid(row=1, column=2)
        item_qty_frame.grid(row=1, column=2)
        item_qty_label = Label(item_qty_frame, text=f"{self.quantity}", justify=RIGHT)
        item_qty_label.pack(expand=True)

        item_image_frame = Frame(item_frame, width=76, height=76, bg='red', highlightthickness=0)
        item_image_frame.grid(row=0, column=3, rowspan=2, padx=0, sticky='n')
        item_frame.rowconfigure(1, weight=1)
        item_frame.columnconfigure(4, weight=1)

        item_image_label = Label(item_image_frame, image=self.small_thumbnail, highlightthickness=0, pady=0)
        item_image_label.image = self.small_thumbnail
        item_image_label.pack(side='top', pady=0)

        if self.offer_price:
            offer_price_label = Label(
                item_frame, width=24, height=76, highlightthickness=0, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"],
                image=self.offer_banner_img
            )
            offer_price_label.image = self.offer_banner_img
            offer_price_label.grid(row=0, column=4, rowspan=2, sticky='e')

        self.bind_click(
            [item_frame,
             item_description_frame,
             item_description_label,
             item_code_frame,
             item_code_label,
             item_price_frame,
             item_price_label,
             item_qty_frame,
             item_qty_label,
             item_image_frame,
             item_image_label
             ], parent
        )

        # Price, Qty, Available, Offer, Code
        return item_frame

    def bind_click(self, widgets, parent):
        for widget in widgets:
            widget.bind("<Button-1>", lambda event: self.edit_item(parent))
            widget['cursor'] = 'hand2'
            widget['bg'] = CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]

    def edit_item(self, parent):
        parent.manage_item(self, True)

    def item_click(self, *args):
        view_item_window = Window("BROWSE", "View Item", "516x662", False)
        self.create_item_window_layout(view_item_window)

    def create_item_window_layout(self, container):
        item_frame = Frame(container, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], pady=0, padx=0)
        item_frame.pack(side='top', fill=BOTH, expand=True)
        item_frame.grid_propagate(False)

        top_left_frame = Frame(item_frame, width=96, height=54, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        top_left_frame.grid(row=0, column=0, sticky="nsew")
        top_left_frame.grid_propagate(False)
        item_code_label = Label(
            top_left_frame, text=f"IC-{self.item_code}", font=CUSTOM_FONTS["SMALL_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]
        )
        self.item_quantity_label = Label(
            top_left_frame, text=f"{self.quantity - self.items.count_items(self)} Available",
            font=CUSTOM_FONTS["SMALL_FONT"], bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]
        )
        item_code_label.grid(row=0, column=0, sticky='w', pady=(4, 2), padx=(4, 0))
        self.item_quantity_label.grid(row=1, column=0, sticky='w', pady=(2, 4), padx=(4, 0))

        top_middle_frame = Frame(item_frame, width=320, height=54, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        top_middle_frame.grid(row=0, column=1, sticky="nsew")
        top_middle_frame.pack_propagate(False)
        item_name_label = Label(
            top_middle_frame, text=f"{self.item_name if len(self.item_name) < 66 else self.item_name[0:63] + '...'}",
            font=CUSTOM_FONTS["LARGE_FONT"], bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], wraplength=320
        )
        item_name_label.place(x=160, y=27, anchor='center')

        top_right_frame = Frame(item_frame, width=96, height=54, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        top_right_frame.grid(row=0, column=2, sticky="nsew")
        top_right_frame.grid_propagate(False)
        top_right_frame.columnconfigure(0, weight=1)
        item_price_label = Label(
            top_right_frame, text=f"£{self.price:.2f}" if not self.offer_price else f"£{self.offer_price:.2f}",
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]
        )
        item_price_label.grid(row=0, column=0, sticky='e', pady=(4, 2), padx=(0, 4))
        self.item_in_cart_label = Label(
            top_right_frame, text=f"In Basket: {self.items.count_items(self)}", fg=CUSTOM_COLOURS["CLICKABLE_LINK"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], font=CUSTOM_FONTS["SMALL_FONT_UNDERLINE"], cursor="hand2"
        )
        self.item_in_cart_label.grid(row=1, column=0, sticky='e', pady=(2, 4), padx=(0, 4))
        self.item_in_cart_label.bind("<Button-1>", self.parent.view_cart)

        self.item_image_label = Label(item_frame, image=self.current_image)
        self.item_image_label.grid(row=2, column=0, columnspan=3)

        bottom_left_frame = Frame(item_frame, width=96, height=54, bg=CUSTOM_COLOURS["FORM_BACKGROUND"])
        bottom_left_frame.grid(row=3, column=0, sticky="nsew")
        bottom_left_frame.pack_propagate(False)
        btn_image_back = ttk.Button(bottom_left_frame, text="<<", command=self.image_back)
        btn_image_back.place(x=48, y=27, anchor='center')

        bottom_middle_frame = Frame(item_frame, width=320, height=54, bg=CUSTOM_COLOURS["FORM_BACKGROUND"])
        bottom_middle_frame.grid(row=3, column=1, sticky="nsew")
        bottom_middle_frame.pack_propagate(False)
        self.item_image_number_label = Label(
            bottom_middle_frame, text=f"Image {self.current_image_index} of {len(self.images)}",
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )
        self.item_image_number_label.place(x=160, y=27, anchor='center')

        bottom_right_frame = Frame(item_frame, width=96, height=54, bg=CUSTOM_COLOURS["FORM_BACKGROUND"])
        bottom_right_frame.grid(row=3, column=2, sticky="nsew")
        bottom_right_frame.pack_propagate(False)
        btn_image_forward = ttk.Button(bottom_right_frame, text=">>", command=self.image_forward)
        btn_image_forward.place(x=48, y=27, anchor='center')

        btn_frame = Frame(item_frame, width=512, height=54, bg=CUSTOM_COLOURS["FORM_BACKGROUND"])
        btn_frame.grid(row=4, column=0, columnspan=3)

        self.btn_add_to_cart = ttk.Button(btn_frame, text="Add to Basket", command=self.add_to_cart, state=NORMAL)
        self.btn_add_to_cart.pack(side='left')
        self.btn_remove_from_cart = ttk.Button(
            btn_frame, text="Remove", command=self.remove_from_cart, state=NORMAL
        )
        self.btn_remove_from_cart.pack(side='left')

        self.set_button_states()

        return item_frame

    def set_button_states(self):
        if not self.check_stock():
            self.btn_add_to_cart['state'] = DISABLED
        else:
            self.btn_add_to_cart['state'] = NORMAL

        if self.items.count_items(self) == 0:
            self.btn_remove_from_cart['state'] = DISABLED
        else:
            self.btn_remove_from_cart['state'] = NORMAL

    def add_to_cart(self):
        if self.check_stock():
            self.items.add_item(self)
            self.update_cart()
            self.set_button_states()

    def remove_from_cart(self):
        self.items.remove_item(self)
        self.set_button_states()
        self.update_cart()

    def update_cart(self):
        self.parent.update_cart()
        self.item_in_cart_label['text'] = f"In Basket: {self.items.count_items(self)}"
        self.item_quantity_label['text'] = f"{self.quantity - self.items.count_items(self)} Available"
        self.item_quantity['text'] = f"In Stock: {self.quantity - self.items.count_items(self)}"
        self.in_basket_label['text'] = f"Number in Basket: {self.items.count_items(self)}"

    def image_forward(self):
        self.current_image_index += 1
        if self.current_image_index > len(self.images):
            self.current_image_index = 1
        self.update_image()

    def image_back(self):
        self.current_image_index -= 1
        if self.current_image_index < 1:
            self.current_image_index = len(self.images)
        self.update_image()

    def update_image(self):
        self.current_image = self.images[self.current_image_index - 1]
        self.current_image = ImageTk.PhotoImage(self.current_image)

        self.item_image_label['image'] = self.current_image
        self.item_image_number_label['text'] = f"Image {self.current_image_index} of {len(self.images)}"

    def check_stock(self):
        if self.quantity - self.items.count_items(self) > 0:
            return True
        else:
            return False

class ManageItem:
    def __init__(self, parent, info=None, edit=False):
        if info:
            self.info = info
        else:
            self.info = StockItem(items=None, parent=parent)

        self.image_list = []
        self.edit = edit

        # Dynamic form components
        self.item_name_input = None
        self.item_qty_input = None
        self.item_price_input = None
        self.offer_price_input = None
        self.offer_price_checkbox = None
        self.offer_price_check = BooleanVar()
        self.delete_checkbox = None
        self.delete_check = BooleanVar()
        if self.edit:
            self.delete_check = not self.info.is_available
        else:
            self.delete_check = False

        self.item_images_frame = None
        self.carousel = None

    def new_item_tile(self, container):
        item_frame = Frame(container, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=320, width=450, pady=1, padx=1)
        item_frame.grid_propagate(False)
        item_frame.grid_rowconfigure(6, weight=1)

        # Name
        item_name_lbl = Label(
            item_frame, text=f"Name:", bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], width=9, anchor='w', padx=5,
            font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"]
        )
        item_name_lbl.grid(row=0, column=0)
        self.item_name_input = Entry(item_frame, width=59)
        self.item_name_input.grid(row=0, column=1, columnspan=2, pady=5)
        self.item_name_input.insert(END, self.info.item_name)

        # Quantity
        item_quantity_lbl = Label(
            item_frame, text=f"In Stock:", bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], width=9,
            font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], anchor='w', padx=5
        )
        item_quantity_lbl.grid(row=1, column=0)
        self.item_qty_input = Entry(item_frame,  width=10)
        self.item_qty_input.grid(row=1, column=1, sticky='w', pady=5)
        self.item_qty_input.insert(END, str(self.info.quantity))

        # Price
        item_price_lbl = Label(
            item_frame, text=f"Price: £", bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], width=9,
            font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], anchor='w', padx=5
        )
        item_price_lbl.grid(row=2, column=0)
        self.item_price_input = Entry(item_frame, width=10)
        self.item_price_input.grid(row=2, column=1, sticky='w', pady=5)
        self.item_price_input.insert(END, str(self.info.price))

        # Offer Price
        offer_price_lbl = Label(
            item_frame, text=f"Price: £", bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], width=9,
            font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], anchor='w', padx=5
        )
        offer_price_lbl.grid(row=3, column=0)
        self.offer_price_input = Entry(item_frame, width=10)
        self.offer_price_input.grid(row=3, column=1, sticky='w', pady=5)
        self.offer_price_checkbox = Checkbutton(
            item_frame, text="On Offer", variable=self.offer_price_check, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"],
            font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], command=lambda: self.offer_clicked()
        )
        self.offer_price_checkbox.deselect()
        self.offer_price_checkbox.grid(row=3, column=2, sticky='e', pady=5)

        # Item Available
        available_lbl = Label(
            item_frame, text=f"Delete:", bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], width=9,
            font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], anchor='w', padx=5, height=1
        )
        if self.edit:
            available_lbl.grid(row=5, column=0)
        self.delete_checkbox = Checkbutton(
            item_frame, variable=self.delete_check, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"],
            font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], command=lambda: self.delete_clicked()
        )
        if self.edit:
            self.delete_checkbox.grid(row=5, column=1, sticky='w', pady=5)

        self.item_images_frame = Frame(item_frame, width=440, height=120, bg="yellow")
        self.item_images_frame.grid(row=4, column=0, columnspan=3)
        self.item_images_frame.pack_propagate(False)

        self.carousel = ImageCarousel(self.item_images_frame, width=440, image_list=self.info.images)
        self.carousel.pack()

        # Confirm Button
        add_item_btn = ttk.Button(item_frame, text="Update" if self.edit else "Add", command=self.confirm_add)
        add_item_btn.grid(row=6, column=2, sticky='se')

        # Cancel Button
        cancel_button = ttk.Button(item_frame, text="Cancel", command=self.cancel_action)
        cancel_button.grid(row=6, column=0, sticky='sw')

        self.set_checkboxes()

        return item_frame

    def set_checkboxes(self):
        # Set whether item is deleted
        if self.info.is_available or self.edit == False:
            self.delete_checkbox.deselect()
        else:
            self.delete_checkbox.select()

        # set offer price
        if self.info.offer_price:
            self.offer_price_input.insert(END, str(self.info.offer_price))
        else:
            self.offer_price_input.insert(END, "0.00")
            self.offer_price_input['state'] = DISABLED

        if self.info.offer_price:
            if self.info.offer_price > 0:
                self.offer_price_input['state'] = NORMAL
                self.item_price_input['state'] = DISABLED
                self.offer_price_checkbox.select()
            else:
                self.offer_price_checkbox.deselect()
        else:
            self.offer_price_checkbox.deselect()

    def delete_clicked(self):
        self.delete_check = not self.delete_check

    def offer_clicked(self):
        if self.offer_price_check.get():
            self.offer_price_input['state'] = NORMAL
            self.item_price_input['state'] = DISABLED
        else:
            self.offer_price_input['state'] = DISABLED
            self.item_price_input['state'] = NORMAL

    def cancel_action(self):
        self.info.parent.clear_management_pane()

    def confirm_add(self):
        # Insert item into stock
        db = DBAccess()

        msg = ""
        offer_price = 0.00
        if self.offer_price_check.get():
            offer_price = self.offer_price_input.get()
            if not self.offer_price_input.get().isdecimal():
                msg += "Special Offer Price must be a whole or decimal number\n"

        if not self.item_qty_input.get().isdigit():
            msg += "Item Quantity must be a whole number\n"
        if not self.item_price_input.get().isdecimal():
            msg += "Item Price must be a whole or decimal number\n"

        if msg != "":
            messagebox.showerror("Form Error", msg)
            return

        if self.edit:
            sql = """UPDATE stock 
            SET item_name = ?, quantity = ?, price = ?, is_available = ?, offer_price = ? 
            WHERE item_code = ?"""
            params = [
                self.item_name_input.get(),
                self.item_qty_input.get(),
                self.item_price_input.get(),
                not self.delete_check,
                offer_price,
                self.info.item_code
            ]
            db.update(sql, params)

            sql = """DELETE from stock_images WHERE item_code = ?"""
            params = [self.info.item_code]
            db.delete(sql, params)

            # Insert item images into database
            self.image_list = self.carousel.get_images()
            for i in range(len(self.image_list)):
                blob_image = db.convert_to_blob(self.image_list[i])
                sql = """INSERT INTO stock_images (item_code, image) VALUES (?, ?)"""
                params = [self.info.item_code, blob_image]
                db.insert(sql, params)

            # Manage price changes

            # Find most recent price change (if there is one)
            sql = """SELECT MAX(valid_to) FROM price_changes WHERE item_code = ?"""
            params = [self.info.item_code]
            last_change_date = db.fetch_one_db(sql, params)
            if last_change_date[0] is None:
                last_change_date = "01/01/2000 00:00:00"
            else:
                last_change_date = last_change_date[0]

            # Regular price > Regular price (Use regular price)
            if (self.item_price_input.get() != str(self.info.price)) \
                    and not self.info.offer_price and not self.offer_price_check.get():
                sql = "INSERT into price_changes (item_code, price, valid_to, valid_from) VALUES (?, ?, ?, ?)"
                params = [self.info.item_code, self.info.price, formatting.uk_datetime(), last_change_date]
                db.insert(sql, params)

            # Regular price > Offer price (Use regular price)
            if not self.info.offer_price and self.offer_price_check.get() and self.offer_price_input.get():
                sql = "INSERT into price_changes (item_code, price, valid_to, valid_from) VALUES (?, ?, ?, ?)"
                params = [self.info.item_code, self.info.price, formatting.uk_datetime(), last_change_date]
                db.insert(sql, params)

            # Offer price > Regular price (Use offer price)
            if self.info.offer_price and not self.offer_price_check.get():
                sql = "INSERT into price_changes (item_code, price, valid_to, valid_from) VALUES (?, ?, ?, ?)"
                params = [self.info.item_code, self.info.offer_price, formatting.uk_datetime(), last_change_date]
                db.insert(sql, params)

            # Offer price > Offer price (Use offer price)
            if self.offer_price_check.get() and self.info.offer_price \
                    and (self.info.offer_price != self.offer_price_input.get()):
                sql = "INSERT into price_changes (item_code, price, valid_to, valid_from) VALUES (?, ?, ?, ?)"
                params = [self.info.item_code, self.info.offer_price, formatting.uk_datetime(), last_change_date]
                db.insert(sql, params)

        else:
            sql = """INSERT into stock (item_name, quantity, price, is_available, offer_price) VALUES (?, ?, ?, ?, ?)"""
            params = [
                self.item_name_input.get(),
                self.item_qty_input.get(),
                self.item_price_input.get(),
                not self.delete_check,
                offer_price
            ]
            self.info.item_code = db.insert(sql, params)

            # Insert item images into database
            self.image_list = self.carousel.get_images()
            for i in range(len(self.image_list)):
                blob_image = db.convert_to_blob(self.image_list[i])
                sql = """INSERT INTO stock_images (item_code, image) VALUES (?, ?)"""
                params = [self.info.item_code, blob_image]
                db.insert(sql, params)

        db.close_connection()

        self.info.parent.clear_management_pane()
        self.info.parent.clear_search()
        self.info.parent.search_field.delete(0, END)
        self.info.parent.search_field.insert(END, self.info.item_code)
        self.info.parent.search_click()


