import tkinter as tk
from tkinter import *
from styles import CUSTOM_COLOURS
from loginpage import LoginPage
from menu import MenuBar
from searchproducts import SearchProducts
from orderspage import SearchOrders
from returnspage import SearchReturns
from manageproducts import ManageProducts
from reportspage import ReportsPage
from manageusers import UsersPage

class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # Create a frame on the main page
        # this frame will be used as the main page container
        self.top_frame = Frame(master, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=70)
        self.top_frame.pack(side="top", fill=X)
        self.top_frame.pack_propagate(False)

        self.menu_frame = MenuBar(self.top_frame, self)
        # self.menu_frame.pack(anchor='nw', side='right', fill=BOTH, expand=True) # For testing
        self.menu_frame.grid_propagate(False)
        self.menu_frame.columnconfigure(1, weight=1)

        divider_frame = Frame(master, bg='black', height=1)
        divider_frame.pack(side="top", fill=X)

        self.main_frame = Frame(master, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        self.main_frame.pack(side="bottom", fill="both", expand=True)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Create a list of pages as frames and add each page to the list
        # the second parameter allows each page to access the show_frame method in this class
        self.frames = {}
        available_pages = (LoginPage, )
        for page in available_pages:
            frame = page(self.main_frame, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(LoginPage)

    def after_login(self, user_profile):
        self.frames.clear()
        for child in self.main_frame.winfo_children():
            child.destroy()

        available_pages = ()
        if user_profile.user_type == "STANDARD":
            available_pages = (
                SearchProducts,
                SearchOrders,
                SearchReturns,
                LoginPage
            )
        elif user_profile.user_type == "SALES":
            available_pages = (
                SearchOrders,
                SearchReturns,
                ReportsPage,
                LoginPage
            )
        elif user_profile.user_type == "ADMIN":
            available_pages = (
                ManageProducts,
                LoginPage,
                ReportsPage,
                UsersPage
            )

        for page in available_pages:
            frame = page(self.main_frame, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        if user_profile.user_type == "STANDARD":
            self.show_frame(SearchProducts)
            self.frames[SearchProducts].search_click()
        else:
            self.show_frame(ReportsPage)

        self.show_menu()

    def clear_search(self):
        self.frames[SearchProducts].search_field.delete(0, END)
        self.frames[SearchProducts].clear_search()

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def show_menu(self):
        self.menu_frame.pack(anchor='nw', side='right', fill=BOTH, expand=True)

    def hide_menu(self):
        self.menu_frame.pack_forget()

    def close_scanner(self):
        self.frames[SearchOrders].remove_scanner()

    def log_out(self):
        for page in self.frames:
            if page != LoginPage:
                self.frames[page].destroy()

