import tkinter as tk
from tkinter import *
from tkinter import ttk
from dataaccess import DBAccess
from styles import CUSTOM_FONTS, CUSTOM_COLOURS
from user import User, UserProfile, UserRegistration
from security import Security

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])

        self.controller = controller
        self.registration_frame = None
        self.registration = UserRegistration(self, "STANDARD")

        self.login_frame = Frame(self, width=350, height=50, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        self.login_frame.place(relx=0.5, rely=0.3, anchor=CENTER)

        # define widgets
        self.sign_up_label = Label(
            self, text="No Account? Click here to register!", bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"],
            font=CUSTOM_FONTS["SEARCH_RESULTS_FONT_LINK"], fg=CUSTOM_COLOURS["CLICKABLE_LINK"], cursor="hand2",
        )
        self.sign_up_label.bind("<Button-1>", lambda event: self.register_new_user())
        self.username = ttk.Entry(self.login_frame)
        self.password = ttk.Entry(self.login_frame, show='*')
        self.login_button = ttk.Button(self.login_frame, text="Login", command=lambda: self.login(self.controller))

        self.display_login()

        self.incorrect_details = Label(self, text="", bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], fg='red')
        self.incorrect_details.pack(side='bottom', anchor='e', padx=10, pady=10)
        self.sign_up_label.pack(side='top', anchor='e', padx=10, pady=10)

    def display_login(self):
        self.login_frame = Frame(self, width=400, height=50, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        self.login_frame.place(relx=0.5, rely=0.35, anchor=CENTER)

        title_frame = Frame(
            self.login_frame, width=400, height=30, bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )
        title_frame.pack_propagate(False)

        title_label = Label(
            title_frame, text="User Login", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )

        username_label = Label(
            self.login_frame, text="Email Address:", bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], anchor='e'
        )
        password_label = Label(
            self.login_frame, text="Password:", bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], anchor='e'
        )
        self.username = ttk.Entry(self.login_frame, width=50)
        self.password = ttk.Entry(self.login_frame, width=50, show='*')
        self.login_button = ttk.Button(self.login_frame, text="Login", command=lambda: self.login(self.controller))

        # place widgets
        title_label.pack(expand=True, fill=BOTH)
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 79))
        username_label.grid(row=1, column=0, pady=3, padx=3, sticky='e', )
        password_label.grid(row=2, column=0, pady=3, padx=3, sticky='e')
        self.username.grid(row=1, column=1, pady=3, padx=3)
        self.password.grid(row=2, column=1, pady=3, padx=3)
        self.login_button.grid(row=3, column=0, columnspan=2, padx=3, pady=3, sticky='e')

    def register_new_user(self):
        self.registration_frame = Frame(self, width=400, height=360, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        self.registration_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.registration_frame.pack_propagate(False)

        self.registration.registration_form(self.registration_frame)

    def close_registration_form(self, *args):
        for child in self.registration_frame.winfo_children():
            child.destroy()
        self.display_login()

    def login(self, controller):
        # Query the database for matching username
        db = DBAccess()
        params = [self.username.get()]
        sql = """SELECT user_id, email_address, first_name, last_name, address, city, 
                 postcode, password, user_type, is_disabled
                 FROM users WHERE email_address = ? COLLATE NOCASE"""
        query_result = db.fetch_all_db(sql, params)
        db.close_connection()

        if query_result:
            UserProfile.current_user = db.create_object(User, (query_result[0]))
        else:
            self.invalid_login("Incorrect Username or Password")
            return

        if not Security.check_password(self.password.get(), UserProfile.current_user.password):
            self.invalid_login("Incorrect Username or Password")
            return
        else:
            if UserProfile.current_user.is_disabled == 1:
                self.invalid_login("Account is deactivated - Please contact support")
                return
            self.valid_login()

    def valid_login(self):
        self.incorrect_details['text'] = "Login Successful"
        self.incorrect_details['fg'] = "green"
        self.username.delete(0, END)
        self.password.delete(0, END)
        self.master.update()
        self.master.after(500, self.clear_text())
        self.clear_text()

        self.controller.after_login(UserProfile.current_user)
        self.controller.menu_frame.after_login()

        # self.master.after(500, self.controller.show_frame(SearchProducts))

    def invalid_login(self, message):
        self.incorrect_details['text'] = message  # "Incorrect Username or Password"
        self.incorrect_details['fg'] = "red"
        self.master.after(1500, self.clear_text)
        current_user = None

    def clear_text(self):
        self.incorrect_details['text'] = ""

