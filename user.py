from tkinter import *
from tkinter import ttk, messagebox
from styles import CUSTOM_FONTS, CUSTOM_COLOURS
from dataaccess import DBAccess
from security import Security

class User:
    def __init__(self, user_id=0, email_address="TEST", first_name=None, last_name=None, address=None, city=None, postcode=None,
                 password=None, user_type=None, is_disabled=0):
        self.user_id = user_id
        self.email = email_address
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.postcode = postcode
        self.password = password
        self.user_type = user_type
        self.is_disabled = is_disabled

        # Dynamic widget
        self.user_type_label = None

    def create_tile(self, container):
        item_frame = Frame(
            container, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=152, width=448, cursor='hand2', pady=0,
            padx=2, highlightbackground=CUSTOM_COLOURS["FORM_BACKGROUND"], highlightthickness=2
        )
        item_frame.grid_propagate(False)
        item_frame.bind("<Button-1>", self.manage_user)

        user_id_label = Label(
            item_frame, text=f"User ID: {self.user_id}", width=25, bg=CUSTOM_COLOURS["FORM_BACKGROUND"],
            font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], anchor='w')
        user_id_label.grid(row=0, column=0, sticky='w')

        self.user_type_label = Label(
            item_frame, text=f"{self.user_type} USER (ACTIVE)" if self.is_disabled == 0
            else f"{self.user_type} USER (DISABLED)", width=27, bg=CUSTOM_COLOURS["FORM_BACKGROUND"],
            font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], anchor='e', padx=12)
        self.user_type_label.grid(row=0, column=1, sticky='e')

        name_label = Label(
            item_frame, text=f"Name: {self.first_name} {self.last_name}", width=54,
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], anchor='w'
        )
        name_label.grid(row=1, column=0, sticky='w', columnspan=2)

        email_label = Label(
            item_frame, text=f"Email: {self.email}", width=len(self.email) + 7,
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], anchor='w')
        email_label.grid(row=2, column=0, sticky='w', columnspan=2)

        address_label = Label(
            item_frame, text=f"Address: {self.address}", width=54, wraplength=446, justify='left',
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], anchor='w')
        address_label.grid(row=3, column=0, sticky='w', columnspan=2)

        city_label = Label(
            item_frame, text=f"City: {self.city}", width=54,
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], anchor='w')
        city_label.grid(row=4, column=0, sticky='w', columnspan=2)

        postcode_label = Label(
            item_frame, text=f"Postcode: {self.postcode}", width=54,
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], anchor='w')
        postcode_label.grid(row=5, column=0, sticky='w', columnspan=2)

        for child in item_frame.winfo_children():
            child.bind("<Button-1>", self.manage_user)

        return item_frame

    def manage_user(self, *args):
        if self.user_id == UserProfile.current_user.user_id:
            messagebox.showerror("Error", "You cannot disable your own account")
            return

        if self.is_disabled == 0:
            if messagebox.askyesno(
                title=f"Disable User {self.user_id}: {self.first_name} {self.last_name}?",
                message=f"This user account will be disabled and the user will no longer be able to log in"
            ) == 0:
                return
            else:
                self.user_type_label['text'] = f"{self.user_type} USER (DISABLED)"
                self.update_user(1)
        else:
            if messagebox.askyesno(
                title=f"Activate User {self.user_id}: {self.first_name} {self.last_name}?",
                message=f"This user account will be re-activated"
            ) == 0:
                return
            else:
                self.user_type_label['text'] = f"{self.user_type} USER (ACTIVE)"
                self.update_user(0)

    def update_user(self, disabled_status):
        db = DBAccess()
        params = [disabled_status, self.user_id]
        sql = """UPDATE users SET is_disabled = ? WHERE user_id = ?"""
        db.update(sql, params)
        db.close_connection()
        self.is_disabled = disabled_status


class UserProfile:
    current_user = User()

class UserRegistration:
    def __init__(self, controller, mode):
        # StringVars for user registration
        self.email_address = StringVar()
        self.first_name = StringVar()
        self.last_name = StringVar()
        self.address = StringVar()
        self.city = StringVar()
        self.postcode = StringVar()
        self.password = StringVar()
        self.user_type = StringVar()
        self.user_types = ["STANDARD", "SALES", "ADMIN"]
        self.user_type.set(self.user_types[0])

        self.text_box_values = [
            self.email_address,
            self.first_name,
            self.last_name,
            self.address,
            self.city,
            self.postcode,
            self.password
        ]

        self.controller = controller
        self.mode = mode

    def registration_form(self, parent):
        registration_frame = Frame(parent, width=400, height=360, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        registration_frame.pack()
        registration_frame.pack_propagate(False)

        # Title
        title_frame = Frame(registration_frame, width=400, height=30, bg=CUSTOM_COLOURS["FORM_BACKGROUND"])
        title_frame.pack(side='top')
        title_frame.pack_propagate(False)

        title_label = Label(
            title_frame, text="Register New Account", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )

        if self.mode == "STANDARD":
            title_label.pack(anchor=CENTER, expand=True)
        elif self.mode == "ADMIN":
            title_frame.grid_propagate(False)
            title_frame.columnconfigure(1, weight=1)
            title_label = Label(
                title_frame, text="Register New Account", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
                bg=CUSTOM_COLOURS["FORM_BACKGROUND"], anchor='w'
            )

            user_type_dropdown = ttk.OptionMenu(title_frame, self.user_type, "STANDARD", *self.user_types)

            account_type_label = Label(
                title_frame, text="Account Type:", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
                bg=CUSTOM_COLOURS["FORM_BACKGROUND"], anchor='e'
            )

            title_label.grid(row=0, column=0, sticky='w', padx=(10, 0), pady=(5, 0))
            account_type_label.grid(row=0, column=1, sticky='e', padx=(0, 0), pady=(5, 0))
            user_type_dropdown.grid(row=0, column=2, sticky='e', padx=(0, 10), pady=(5, 0))

        # Input Labels
        label_frame = Frame(registration_frame, width=100, height=330, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        label_frame.pack(side='left')
        label_frame.grid_propagate(False)

        label_first_name = Label(label_frame, text="First Name: ")
        label_last_name = Label(label_frame, text="Last Name: ")
        label_address = Label(label_frame, text="Address: ")
        label_city = Label(label_frame, text="City: ")
        label_postcode = Label(label_frame, text="Postcode: ")
        label_email_address = Label(label_frame, text="Email Address: ")
        label_password = Label(label_frame, text="Password: ")

        # Place widgets
        label_first_name.grid(row=0)
        label_last_name.grid(row=1)
        label_address.grid(row=2)
        label_city.grid(row=3)
        label_postcode.grid(row=4)
        label_email_address.grid(row=5)
        label_password.grid(row=6)

        for child in label_frame.winfo_children():
            child.grid_configure(padx=10, pady=10, sticky='e')
            child['bg'] = CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]
        label_first_name.grid_configure(pady=(20, 10))

        # Input fields
        input_frame = Frame(registration_frame, width=300, height=330, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        input_frame.pack(side='left')
        input_frame.grid_propagate(False)

        input_first_name = ttk.Entry(input_frame, textvariable=self.first_name)
        input_last_name = ttk.Entry(input_frame, textvariable=self.last_name)
        input_address = ttk.Entry(input_frame, textvariable=self.address)
        input_city = ttk.Entry(input_frame, textvariable=self.city)
        input_postcode = ttk.Entry(input_frame, textvariable=self.postcode)
        input_email_address = ttk.Entry(input_frame, textvariable=self.email_address)
        input_password = ttk.Entry(input_frame, show="*", textvariable=self.password)

        # Place widgets
        input_first_name.grid(row=0)
        input_last_name.grid(row=1)
        input_address.grid(row=2)
        input_city.grid(row=3)
        input_postcode.grid(row=4)
        input_email_address.grid(row=5)
        input_password.grid(row=6)

        for child in input_frame.winfo_children():
            child.grid_configure(padx=1, pady=10, sticky='e', column=0, columnspan=2)
            child['width'] = 47
        input_first_name.grid_configure(pady=(20, 10))

        cancel_button = ttk.Button(input_frame, text="Cancel", command=lambda: self.close_form(result="CANCEL"))
        register_button = ttk.Button(input_frame, text="Register", command=self.submit_registration)

        cancel_button.grid(row=7, column=0, sticky='w')
        register_button.grid(row=7, column=1, sticky='e')

        return registration_frame

    def close_form(self, result):
        self.clear_text_boxes()
        self.controller.close_registration_form(result)

    def clear_text_boxes(self):
        for textbox in self.text_box_values:
            textbox.set("")

    def submit_registration(self):
        db = DBAccess()

        # Check if email already in use
        sql = "SELECT email_address FROM users WHERE email_address = ?"
        params = [self.email_address.get()]
        if db.fetch_all_db(sql, params):
            messagebox.showerror(
                title="Error",
                message=f"The email address {self.email_address.get()} is already in use",
                parent=self.controller
            )
            return

        # Hash password
        pwd = Security.get_hashed_password(self.password.get())

        # Add User
        sql = """INSERT INTO users 
        (email_address, first_name, last_name, address, city, postcode, password, user_type, is_disabled)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)"""

        params = [
            self.email_address.get(),
            self.first_name.get(),
            self.last_name.get(),
            self.address.get(),
            self.city.get(),
            self.postcode.get(),
            pwd,
            self.user_type.get()
        ]

        for param in self.text_box_values:
            if param.get() == "":
                messagebox.showerror(
                    title="Error",
                    message=f"Please complete the form",
                    parent=self.controller
                )
                return

        # Check email validity
        msg = Security.check_email(self.email_address.get())
        if msg != "":
            messagebox.showerror("Error", msg)
            return

        # Check Password Strength
        msg = Security.check_password_strength(self.password.get())
        if msg != "":
            messagebox.showerror("Weak Password", msg)
            return

        db.insert(sql, params)
        db.close_connection()

        # Option to send email as part of registration (Will require securing of the mailserver smtp password)
        # Probably needs to use RSA keys in order to achieve this.
        """
        welcome_mail = mailservice.SMTP(
            destination_email=self.email_address.get(),
            subject="Welcome to UOG clothing",
            message=f"Dear {self.first_name.get()}\n\n"
                    "Thank you for registering!\n\n"
                    "Your account is now active.\n\n"
                    "Enjoy Shopping!\n\n"
                    "Best Regards\n"
                    "UOG Clothing"
        )
        welcome_mail.send_mail()
        """

        messagebox.showinfo(
            title="Welcome",
            message="Your account has been created, happy shopping!",  # a confirmation email has been sent
            parent=self.controller
        )

        self.close_form(result="OK")

