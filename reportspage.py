import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from dataaccess import DBAccess
import formatting
from reports import *
from styles import CUSTOM_FONTS, CUSTOM_COLOURS
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandastable import Table as PTable, TableModel
from user import UserProfile

class ReportData:
    def __init__(self, df, report_title, chart_heading, graph_data, graph_labels, filename, graph_data_2=None):
        self.df = df
        self.report_title = report_title
        self.chart_heading = chart_heading
        self.graph_data = graph_data
        self.graph_data_2 = graph_data_2
        self.graph_labels = graph_labels
        self.filename = filename


class ReportsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        self.controller = controller
        self.search_limit = 5
        self.report_data = None

        self.top_frame = Frame(self, height=50, bg=CUSTOM_COLOURS["FORM_BACKGROUND"])
        self.top_frame.pack(side='top', fill=X, anchor='n')
        self.top_frame.pack_propagate(False)

        # MAIN REPORT TYPE
        report_name_label = Label(
            self.top_frame, text="Report Type:", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )

        report_name_label.pack(side='left', anchor='w', pady=10, padx=(10, 0))

        # StringVar to store selected dropdown item
        self.var = StringVar()
        # StringVar for Sub-Types
        self.opt_var = StringVar()

        # Menu options
        self.report_name_list = ["Sales", "Stock"]

        # Sub-Type Categories
        self.stock_options = [
            "Current Special Offers",
            "Low Stock",
            "Stock Levels"
        ]
        self.sales_options = [
            "Best-Sellers (Amount)",
            "Best-Sellers (Value)",
            "Sales Per User"
        ]

        # Sub-Type in view
        self.report_options = self.sales_options  # ["Best-Sellers (Amount)","Best-Sellers (Value)","Sales Per User"]

        if UserProfile.current_user.user_type == "SALES":
            self.report_name_list = ["Stock"]
            self.stock_options = ["Stock Levels"]
            self.report_options = self.stock_options
            self.var.set(self.report_name_list[0])
            self.opt_var.set(self.report_options[0])

        s = ttk.Style()
        s.configure('TMenubutton', background=CUSTOM_COLOURS["FORM_BACKGROUND"])
        self.report_type_dropdown = ttk.OptionMenu(self.top_frame, self.var, "Please Select", *self.report_name_list)
        self.report_type_dropdown.pack(side='left', anchor='w', pady=(10, 8), padx=0)
        self.var.trace('w', self.report_type_changed)

        # REPORT SUB-TYPE
        self.report_options_label = Label(
            self.top_frame, text="Sub-Type:", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )

        # define widgets

        self.report_options_dropdown = ttk.OptionMenu(
            self.top_frame, self.opt_var, "Best Sellers (Amount)", *self.report_options
        )
        self.opt_var.set(self.report_options[0])
        self.opt_var.trace('w', lambda x, y, z: self.sub_type_changed())

        # SEARCH LIMITS
        self.report_limit_label = Label(
            self.top_frame, text="Show Top:", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )

        # StringVar for Search Limit
        self.limit_var = StringVar()
        # define widgets
        self.stock_limits = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.top_limits = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "MAX"]
        self.limit_options = self.top_limits

        self.limit_dropdown = ttk.OptionMenu(self.top_frame, self.limit_var, "5", *self.limit_options)
        self.limit_var.set(self.limit_options[4])
        self.limit_var.trace('w', self.limit_changed)

        # DATE PICKERS
        self.date_from = DateEntry(self.top_frame, selectmode='day', locale='en_UK', date_pattern='dd/mm/yyyy')
        self.date_from.set_date('01/11/2022')
        self.date_to = DateEntry(self.top_frame, selectmode='day', locale='en_UK', date_pattern='dd/mm/yyyy')

        self.search_button = ttk.Button(self.top_frame, text="Generate Report", command=self.search_click)
        self.search_button.pack(side='right', anchor='e', pady=10, padx=10)

        self.results_frame = Frame(self, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        self.results_frame.pack(side='top', fill='both', expand=True, anchor='n')
        self.results_frame.pack_propagate(False)

        # Dynamic Widgets
        self.report_image = PhotoImage(file="images/button_icons/sales_data32x32.png")
        self.pie_report_image = PhotoImage(file="images/button_icons/pie_chart32x32.png")
        self.csv_export_image = PhotoImage(file="images/button_icons/csv32x32.png")
        self.toolbar_frame = Frame(self.results_frame, bg='white', height=50, width=900)
        self.barchart_label = Label(self.toolbar_frame, width=32, height=32, image=self.report_image)
        self.piechart_label = Label(self.toolbar_frame, width=32, height=32, image=self.pie_report_image)
        self.csv_label = Label(self.toolbar_frame, width=32, height=32, image=self.csv_export_image)

        self.discontinued_check = BooleanVar()
        self.discontinued_checkbox = Checkbutton(
            self.top_frame, text="Include Discontinued Products", variable=self.discontinued_check,
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"], font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"]
        )
        self.discontinued_checkbox.deselect()

        self.create_search_label(
            "Generate reports here.\n\n"
            "Use the options to configure the report types."
        )

    def limit_changed(self, *args):
        if self.limit_var.get() == "MAX":
            self.search_limit = -1
        else:
            self.search_limit = int(self.limit_var.get())

    def sub_type_changed(self):
        if self.opt_var.get() == "Low Stock":
            self.limit_options = self.stock_limits
            self.limit_dropdown = ttk.OptionMenu(self.top_frame, self.limit_var, "5", *self.limit_options)
            self.limit_var.set(self.limit_options[4])
            self.report_limit_label['text'] = "Low Stock Level:"
            self.report_limit_label.pack(side='left', anchor='w', pady=10, padx=(10, 0))
            self.limit_dropdown.pack(side='left', anchor='w', pady=(10, 8), padx=0)

        if self.opt_var.get() not in ["Low Stock", "Sales Per User", "Best-Sellers (Value)", "Best-Sellers (Amount)"]:
            self.report_limit_label.pack_forget()
            self.limit_dropdown.pack_forget()

    def report_type_changed(self, *args):
        self.discontinued_checkbox.pack_forget()
        self.report_options_label.pack_forget()
        self.report_options_dropdown.pack_forget()
        self.report_limit_label.pack_forget()
        self.limit_dropdown.pack_forget()
        self.date_from.pack_forget()
        self.date_to.pack_forget()
        self.update()

        if self.var.get() == "Sales":
            # Update dropdowns
            self.report_options = self.sales_options
            self.report_options_dropdown = ttk.OptionMenu(
                self.top_frame, self.opt_var, "Best Sellers (Amount)", *self.report_options
            )
            self.opt_var.set(self.report_options[0])

            # Customise widgets
            self.date_from.pack(side='left', anchor='w', pady=10, padx=5)
            self.date_to.pack(side='left', anchor='w', pady=10, padx=(5, 0))
            self.report_options_label.pack(side='left', anchor='w', pady=10, padx=(10, 0))
            self.report_options_dropdown.pack(side='left', anchor='w', pady=(10, 8), padx=0)

            self.limit_options = self.top_limits
            self.limit_dropdown = ttk.OptionMenu(self.top_frame, self.limit_var, "5", *self.limit_options)
            self.limit_var.set(self.limit_options[4])
            self.report_limit_label['text'] = "Show Top:"
            self.report_limit_label.pack(side='left', anchor='w', pady=10, padx=(10, 0))
            self.limit_dropdown.pack(side='left', anchor='w', pady=(10, 8), padx=0)

        elif self.var.get() == "Stock":
            # Update dropdowns
            self.report_options = self.stock_options
            self.report_options_dropdown = ttk.OptionMenu(
                self.top_frame, self.opt_var, "Best Sellers (Amount)", *self.report_options
            )
            self.opt_var.set(self.report_options[0])

            # Customise widgets
            self.report_options_label.pack(side='left', anchor='w', pady=10, padx=(10, 0))
            self.report_options_dropdown.pack(side='left', anchor='w', pady=(10, 8), padx=0)
            self.discontinued_checkbox.pack(side='left', anchor='w', pady=(10, 8), padx=0)

    def clear_results(self):
        for child in self.results_frame.winfo_children():
            child.destroy()

    def search_click(self):
        self.clear_results()
        match self.var.get():
            case "Sales":
                self.sales_reports()
            case "Stock":
                self.stock_reports()
            case _:
                self.create_search_label("Please select a report type")

    def custom_reports(self):
        df = None
        if self.opt_var.get() == "Stock":
            self.discontinued_check.set(True)
            df = self.get_stock_data()
        else:
            df = self.get_sales_data()

        self.report_data = ReportData(
            df=df,
            report_title=f"CUSTOM REPORT",
            chart_heading="CUSTOM REPORT",
            graph_data=None,
            graph_labels=None,
            filename=f"Custom_Report_{formatting.uk_datetime_filename()}"
        )
        message = f"Custom Report"

        self.create_datatable(True)
        self.create_report_toolbar(message)

    def stock_reports(self):
        df = self.get_stock_data()
        if df.empty:
            self.create_search_label("No sales found for selected dates")
            return

        message = ""
        match self.opt_var.get():
            case "Low Stock":
                df_low_stock = df[df['quantity'] < self.search_limit]
                self.report_data = ReportData(
                    df=df_low_stock.sort_values(by='quantity', ascending=True),
                    report_title=f"LOW STOCK LEVELS < {self.search_limit} ITEMS IN STOCK:",
                    chart_heading="LOW STOCK",
                    graph_data="quantity",
                    graph_labels="item_name",
                    filename=f"Low_Stock_Report_{formatting.uk_datetime_filename()}"
                )
                message = f"Stock levels < {self.search_limit} items"
            case "Current Special Offers":
                df_current_offers = df[df['offer_price'] > 0]
                self.report_data = ReportData(
                    df=df_current_offers.sort_values(by='offer_price', ascending=True),
                    report_title=f"Items Currently on Special Offer",
                    chart_heading="LOW STOCK",
                    graph_data="price",
                    graph_data_2='offer_price',
                    graph_labels="item_name",
                    filename=f"Current_Special_Offers_{formatting.uk_datetime_filename()}"
                )
                message = "Items Currently on Special Offer"
            case "Stock Levels":
                df_stock_levels = df
                self.report_data = ReportData(
                    df=df_stock_levels.sort_values(by='item_code', ascending=True),
                    report_title=f"ALL STOCK ITEMS",
                    chart_heading="STOCK QUANTITY",
                    graph_data="quantity",
                    graph_labels="item_name",
                    filename=f"Stock_Levels_{formatting.uk_datetime_filename()}"
                )
                message = f"Current Stock Levels"

        self.create_datatable(False)
        self.create_report_toolbar(message)

    def sales_reports(self):
        df = self.get_sales_data()
        if df.empty:
            self.create_search_label("No sales found for selected dates")
            return

        units = ""
        message = f"Total Sales From: {formatting.convert_from_db_date(str(self.date_from.get_date()))} " \
                  f"To: {formatting.convert_from_db_date(str(self.date_to.get_date()))}"

        if self.opt_var.get() == "Best-Sellers (Amount)" or self.opt_var.get() == "Best-Sellers (Value)":
            df_best_sellers = df
            df_best_sellers['items_sold'] = df.groupby('item_name')['item_name'].transform('count')
            df_best_sellers = df_best_sellers.groupby(['item_name', 'items_sold'], as_index=False)[['price']].sum()
            df_best_sellers.rename(columns={'price': 'total_value'}, inplace=True)
            df_best_sellers = df_best_sellers.iloc[0:self.search_limit]

            if self.opt_var.get() == "Best-Sellers (Amount)":
                total_units = df_best_sellers[['items_sold']].sum()
                units = f"{int(total_units)}"
                self.report_data = ReportData(
                    df=df_best_sellers.sort_values(by='items_sold', ascending=False),
                    report_title=message,
                    chart_heading=f"TOTAL UNITS SOLD {int(total_units)}",
                    graph_data="items_sold",
                    graph_labels="item_name",
                    filename=f"Best_Sellers_{formatting.uk_datetime_filename()}"
                )

            elif self.opt_var.get() == "Best-Sellers (Value)":
                total_price = df[['price']].sum()
                units = f"£{float(total_price):.2f}"
                self.report_data = ReportData(
                    df=df_best_sellers.sort_values(by='total_value', ascending=False),
                    report_title=message,
                    chart_heading=f"TOTAL VALUE OF SALES (£{float(total_price):.2f})",
                    graph_data="total_value",
                    graph_labels="item_name",
                    filename=f"Best_Sellers_{formatting.uk_datetime_filename()}"
                )

        elif self.opt_var.get() == "Sales Per User":
            df_total_per_user = df
            df_total_per_user = df_total_per_user.groupby(['email_address'], as_index=False)[['price']].sum()
            df_total_per_user.rename(columns={'price': 'total_spend'}, inplace=True)
            df_total_per_user = df_total_per_user.iloc[0:self.search_limit]
            self.report_data = ReportData(
                df=df_total_per_user,
                report_title=message,
                chart_heading="SPEND PER USER:",
                graph_data="total_spend",
                graph_labels="email_address",
                filename=f"Sales_per_User_{formatting.uk_datetime_filename()}"
            )

        message = f"{units} {message}"

        self.create_datatable(False)
        self.create_report_toolbar(message)

    def create_datatable(self, toolbar):
        frame = Frame(self.results_frame, width=900, height=453)
        frame.grid(row=1, column=0)
        frame.grid_propagate(False)

        pt = PTable(frame, dataframe=self.report_data.df, maxcellwidth=400, showtoolbar=toolbar, showstatusbar=True)
        pt.show()

    def create_search_label(self, message):
        results_Label = Label(
            self.results_frame, text=message, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"],
            font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], anchor='w', justify='left'
        )
        results_Label.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

    def create_report_toolbar(self, message):
        self.toolbar_frame = Frame(self.results_frame, bg='white', height=50, width=900)
        self.toolbar_frame.grid_propagate(False)
        self.toolbar_frame.grid(row=0, column=0, pady=5)

        message_label = Label(self.toolbar_frame, text=message, bg='white', font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"])
        message_label.pack(side='left', padx=20, anchor='w')

        if self.opt_var.get() not in ["Stock Levels", "Stock", "Sales"]:
            self.barchart_label = Label(self.toolbar_frame, width=32, height=32, image=self.report_image, cursor='hand2')
            self.barchart_label.pack(side='right', padx=20, anchor='e')
            self.barchart_label.bind("<Button-1>", lambda event: self.view_details("bar"))

        if self.opt_var.get() not in ["Low Stock", "Current Special Offers", "Stock Levels", "Stock", "Sales"]:
            self.piechart_label = Label(
                self.toolbar_frame, width=32, height=32, image=self.pie_report_image, cursor='hand2'
            )
            self.piechart_label.pack(side='right', padx=20, anchor='e')
            self.piechart_label.bind("<Button-1>", lambda event: self.view_details("pie"))

        self.csv_label = Label(
            self.toolbar_frame, width=32, height=32, image=self.csv_export_image, cursor='hand2'
        )
        self.csv_label.pack(side='right', padx=20, anchor='e')
        self.csv_label.bind("<Button-1>", lambda event: self.view_details("csv"))

    def view_details(self, chart_type):
        if chart_type == 'pie':
            self.pie_chart(wedge_display='numbers')
        elif chart_type == 'bar':
            self.bar_chart()
        elif chart_type == 'csv':
            self.report_data.df.to_csv(f"reports//{self.report_data.filename}.csv", index=False)
            messagebox.showinfo(
                title="Report Saved",
                message=f"Saved to: reports\\{self.report_data.filename}.csv",
                parent=self.controller
            )

    def pie_chart(self, wedge_display=""):

        df_pie = self.report_data.df

        total = df_pie[[self.report_data.graph_data]].sum()
        labels = df_pie[self.report_data.graph_labels]
        sizes = df_pie[self.report_data.graph_data]

        # Explodes the first wedge
        explode = np.zeros(labels.count())
        explode[0] = 0.1

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 5))
        fig.canvas.manager.set_window_title(self.report_data.report_title)

        pie = ax1.pie(
            sizes,
            explode=explode,
            labels=None,
            # autopct='%1.2f%%' if wedge_display == 'percentage' else lambda x: f"{float(x * total / 100):.2f}",
            autopct=lambda x: f"{float(x * total / 100):.2f}",
            shadow=False,
            startangle=90
        )

        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax2.axis("off")

        ax2.legend(pie[0], labels, loc='best')
        ax1.set_title(self.report_data.chart_heading)
        plt.suptitle(self.report_data.report_title)

        plt.show()

    def bar_chart(self):
        df_bar = self.report_data.df

        fig, ax = plt.subplots(figsize=(8, 5))
        fig.canvas.manager.set_window_title(self.report_data.report_title)

        indexes = list(df_bar[self.report_data.graph_labels])
        y_pos = np.arange(len(indexes))

        ax.barh(y_pos, df_bar[self.report_data.graph_data], align='center')
        if self.report_data.graph_data_2:
            # There must be a better way of doing this...
            bar1 = df_bar.columns[df_bar.columns.get_loc(self.report_data.graph_data)]
            bar2 = df_bar.columns[df_bar.columns.get_loc(self.report_data.graph_data_2)]
            ax.barh(y_pos, df_bar[self.report_data.graph_data_2], align='center')
            ax.legend([bar1, bar2])

        ax.set_yticks(y_pos, labels=indexes)
        ax.set_xlabel(self.report_data.graph_data)

        plt.suptitle(self.report_data.report_title)
        plt.tight_layout()
        plt.show()

        # ax = df_bar.plot.barh(rot=0, x='item_name', y=bar_type)

    def get_sales_data(self):
        db = DBAccess()
        # Return all sales between selected dates
        params = [self.date_from.get_date(), self.date_to.get_date() + datetime.timedelta(days=1)]
        sql = pd.read_sql_query(
            """SELECT so.receipt_number, o.order_date, so.item_code, 
            s.item_name, u.email_address, 
            CASE WHEN pc.valid_to > o.order_date THEN pc.price ELSE
            CASE WHEN s.offer_price > 0 THEN s.offer_price ELSE s.price END END AS price,
            so.return_status, so.stock_order_id, so.return_date
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
            WHERE datetime(o.order_date) BETWEEN datetime(?) AND datetime(?)""",
            db.conn, params=params)

        df = pd.DataFrame(
            sql, columns=[
                'receipt_number',
                'order_date',
                'item_code',
                'item_name',
                'email_address',
                'price',
                'return_status',
                'stock_order_id',
                'return_date'
            ])
        db.close_connection()
        return df

    def get_stock_data(self):
        db = DBAccess()
        # Return all sales between selected dates
        sql = pd.read_sql_query(
            """SELECT item_code, item_name, quantity, price, offer_price, is_available 
               FROM stock""",
            db.conn)

        df = pd.DataFrame(
            sql, columns=[
                'item_code',
                'item_name',
                'quantity',
                'price',
                'offer_price',
                'is_available'
            ])
        db.close_connection()

        if not self.discontinued_check.get():
            df = df[df['is_available'] == 1]
            del df['is_available']

        return df
