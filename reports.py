from tkinter import *
from styles import CUSTOM_FONTS, CUSTOM_COLOURS

class BestSellers:
    def __init__(self, item_code, item_name, number_items):
        self.item_code = item_code
        self.item_name = item_name
        self.number_items = number_items

    @staticmethod
    def create_header_row(container):
        item_frame = Frame(container, bg='white', height=30, width=900, padx=20)
        item_frame.grid_propagate(False)

        # Item Code
        item_code_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=30, width=100, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        item_code_frame.grid(row=0, column=0)
        item_code_frame.pack_propagate(False)
        item_code_heading = Label(
            item_code_frame, text=f"Item Code", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )
        item_code_heading.pack(side="left")

        # Item Name
        item_name_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=30, width=660, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        item_name_frame.grid(row=0, column=1)
        item_name_frame.pack_propagate(False)
        item_name_heading = Label(
            item_name_frame, text=f"Item Name", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )
        item_name_heading.pack(side="left")

        # Items Sold
        items_sold_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=30, width=100, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        items_sold_frame.grid(row=0, column=2)
        items_sold_frame.pack_propagate(False)
        items_sold_heading = Label(
            items_sold_frame, text=f"Items Sold", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )
        items_sold_heading.pack(side="left")

        return item_frame

    def create_report_item(self, container):
        item_frame = Frame(container, bg='white', height=40, width=900, padx=20)
        item_frame.grid_propagate(False)

        # Item Code
        item_code_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=40, width=100, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        item_code_frame.grid(row=0, column=0)
        item_code_frame.pack_propagate(False)
        item_code_heading = Label(
            item_code_frame, text=f"{self.item_code}", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]
        )
        item_code_heading.pack(side="left")

        # Item Name
        item_name_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=40, width=660, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        item_name_frame.grid(row=0, column=1)
        item_name_frame.pack_propagate(False)
        item_name_heading = Label(
            item_name_frame, text=f"{self.item_name}", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], wraplength=600
        )
        item_name_heading.pack(side="left")

        # Items Sold
        items_sold_frame = Frame(
            item_frame, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"], height=40, width=100, padx=10,
            highlightbackground='black', highlightthickness=1
        )
        items_sold_frame.grid(row=0, column=2)
        items_sold_frame.pack_propagate(False)
        items_sold_heading = Label(
            items_sold_frame, text=f"{self.number_items}", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"]
        )
        items_sold_heading.pack(side="left")

        return item_frame

