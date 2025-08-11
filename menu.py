from tkinter import *
import tkinter as tk
from tkinter import messagebox
from styles import CUSTOM_FONTS, CUSTOM_COLOURS
from loginpage import LoginPage
from user import UserProfile
from orderspage import SearchOrders
from searchproducts import SearchProducts
from returnspage import SearchReturns
from manageproducts import ManageProducts
from reportspage import ReportsPage
from manageusers import UsersPage
from window import Window

class MenuBar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=70, pady=1)

        self.controller = controller
        self.logout_img = PhotoImage(file="images/button_icons/logout64x64.png")
        self.returns_img = PhotoImage(file="images/button_icons/returns64x64.png")
        self.orders_img = PhotoImage(file="images/button_icons/orders64x64.png")
        self.catalogue_img = PhotoImage(file="images/button_icons/catalogue64x64.png")
        self.manage_catalogue_img = PhotoImage(file="images/button_icons/manage_catalogue64x64.png")
        self.reports_img = PhotoImage(file="images/button_icons/sales_data64x64.png")
        self.stock_reports_img = PhotoImage(file="images/button_icons/stock_info64x64.png")
        self.user_img = PhotoImage(file="images/button_icons/manage_users64x64.png")

        self.welcome_frame = Frame(self, height=68, width=300, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], padx=10)
        self.welcome_frame.grid(row=0, column=0, sticky='w')
        self.welcome_frame.pack_propagate(False)

        self.nav_frame = Frame(self, height=68, width=600, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], padx=10)
        self.nav_frame.grid(row=0, column=1, sticky='e')
        self.nav_frame.pack_propagate(False)

        self.welcome_label = Label(
            self.welcome_frame, text=f"Welcome: {UserProfile.current_user.first_name}",
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"], font=CUSTOM_FONTS["LARGE_FONT"]
        )
        self.welcome_label.pack(side='left', anchor="e")

        # Dynamic button widgets
        self.logout_canvas = None
        self.browse_canvas = None
        self.returns_canvas = None
        self.orders_canvas = None
        self.manage_canvas = None
        self.users_canvas = None
        self.reports_canvas = None
        self.active_button = None

    def after_login(self):
        self.logout_canvas = self.new_canvas(False)
        self.logout_canvas.pack(anchor='e', side='right')
        self.logout_canvas.create_image(2, 2, image=self.logout_img, anchor='nw')
        self.logout_canvas.bind("<Button-1>", lambda event: self.log_out(self.controller))
        self.bind_hover_actions(self.logout_canvas)

        # USER LEVEL ACCESS BUTTONS
        if UserProfile.current_user.user_type == "STANDARD":
            # Search Catalogue
            self.browse_canvas = self.new_canvas(True)
            self.browse_canvas.pack(anchor='e', side='right', padx=(0, 5))
            self.browse_canvas.create_image(2, 2, image=self.catalogue_img, anchor='nw')
            self.browse_canvas.bind(
                "<Button-1>", lambda event: self.load_page(self.controller, self.browse_canvas, SearchProducts))
            self.bind_hover_actions(self.browse_canvas)

            # Set the active button
            self.active_button = self.browse_canvas

        if UserProfile.current_user.user_type == "STANDARD" or UserProfile.current_user.user_type == "SALES":
            # Returns
            self.returns_canvas = self.new_canvas(False)
            self.returns_canvas.pack(anchor='e', side='right', padx=(0, 5))
            self.returns_canvas.create_image(2, 2, image=self.returns_img, anchor='nw')
            self.returns_canvas.bind(
                "<Button-1>", lambda event: self.load_page(self.controller, self.returns_canvas, SearchReturns))
            self.bind_hover_actions(self.returns_canvas)

            # Orders
            self.orders_canvas = self.new_canvas(False)
            self.orders_canvas.pack(anchor='e', side='right', padx=(0, 5))
            self.orders_canvas.create_image(2, 2, image=self.orders_img, anchor='nw')
            self.orders_canvas.bind(
                "<Button-1>", lambda event: self.load_page(self.controller, self.orders_canvas, SearchOrders))
            self.bind_hover_actions(self.orders_canvas)

        # ADMIN LEVEL ACCESS BUTTONS
        if UserProfile.current_user.user_type == "ADMIN":
            # Manage Catalogue
            self.manage_canvas = self.new_canvas(False)
            self.manage_canvas.pack(anchor='e', side='right', padx=(0, 5))
            self.manage_canvas.create_image(2, 2, image=self.manage_catalogue_img, anchor='nw')
            self.manage_canvas.bind(
                "<Button-1>", lambda event: self.load_page(self.controller, self.manage_canvas, ManageProducts))
            self.bind_hover_actions(self.manage_canvas)

            # Manage Users
            self.users_canvas = self.new_canvas(False)
            self.users_canvas.pack(anchor='e', side='right', padx=(0, 5))
            self.users_canvas.create_image(2, 2, image=self.user_img, anchor='nw')
            self.users_canvas.bind(
                "<Button-1>", lambda event: self.load_page(self.controller, self.users_canvas, UsersPage))
            self.bind_hover_actions(self.users_canvas)

        if UserProfile.current_user.user_type == "ADMIN" or UserProfile.current_user.user_type == "SALES":
            # Sales Data
            self.reports_canvas = self.new_canvas(True)
            self.reports_canvas.pack(anchor='e', side='right', padx=(0, 5))
            self.reports_canvas.create_image(
                2, 2, anchor='nw',
                image=self.reports_img if UserProfile.current_user.user_type == "ADMIN" else self.stock_reports_img
            )
            self.reports_canvas.bind(
               "<Button-1>", lambda event: self.load_page(self.controller, self.reports_canvas, ReportsPage))
            self.bind_hover_actions(self.reports_canvas)
            # Set active button
            self.active_button = self.reports_canvas

        self.update_widgets()

    def new_canvas(self, is_active):
        return Canvas(
            self.nav_frame, height=64, width=64, bg='white' if is_active else CUSTOM_COLOURS["FORM_BACKGROUND"],
            highlightthickness=2, highlightbackground=CUSTOM_COLOURS["BUTTON_BORDER"],
            cursor="hand2")

    def bind_hover_actions(self, widget):
        widget.bind("<Enter>", lambda event: self.button_hover_enter(widget))
        widget.bind("<Leave>", lambda event: self.button_hover_leave(widget))

    def button_hover_enter(self, widget):
        widget['bg'] = "white"

    def button_hover_leave(self, widget):
        if self.active_button != widget:
            widget['bg'] = CUSTOM_COLOURS["FORM_BACKGROUND"]

    def load_page(self, controller, widget, page):
        if self.active_button == self.orders_canvas:
            self.controller.close_scanner()

        if self.active_button != widget:
            self.active_button['bg'] = CUSTOM_COLOURS["FORM_BACKGROUND"]
            self.active_button = widget
            controller.show_frame(page)

    def log_out(self, controller):
        if messagebox.askyesno(
                title="You will be logged out", message="Do you wish to log out?", parent=self.controller) == 0:
            return
        # Close all open windows
        Window.close_windows()
        controller.hide_menu()

        for child in self.nav_frame.winfo_children():
            child.pack_forget()

        if UserProfile.current_user.user_type == "STANDARD":
            self.controller.clear_search()

        self.load_page(controller, self.browse_canvas, LoginPage)
        self.controller.log_out()

    def update_widgets(self):
        self.welcome_label['text'] = f"Welcome: {UserProfile.current_user.first_name}"
        self.active_button['bg'] = 'white'
