from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from styles import CUSTOM_FONTS, CUSTOM_COLOURS
from tkinter import filedialog as fd
from dataaccess import DBAccess
import io

class ImageCarousel:
    def __init__(self, parent, width=355, height=140, title='Images:', allow_add=True, image_list=None):
        # image_list contains the original sized images and thumbnail list contains resized images
        # This is to prevent loss of resolution that happens when thumbnails are enlarged back to full size
        if image_list:
            self.image_list = image_list
        else:
            self.image_list = []
        self.thumbnail_list = []

        self.width = width
        self.height = height
        self.title = title
        self.allow_add = allow_add
        self.carousel_index = 0

        self.carousel_frame = Frame(parent, width=self.width, height=self.height, bg='white')

        self.carousel_ribbon = Frame(
            self.carousel_frame, width=self.width, height=20, bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )
        self.carousel_ribbon.pack(side='top', anchor='n')
        self.carousel_ribbon.pack_propagate(False)

        self.title_label = Label(
            self.carousel_ribbon, text=self.title, font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
            bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )
        self.title_label.pack(side='left', anchor='w')

        if allow_add:
            self.add_img_label = Label(
                self.carousel_ribbon, text="+", font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"],
                bg=CUSTOM_COLOURS["FORM_BACKGROUND"], padx=5
            )
            self.add_img_label.pack(side='right', anchor="e")
            self.add_img_label.bind("<Button-1>", lambda event: self.add_image())
            self.bind_hover_actions(self.add_img_label)

        self.btn_left = Frame(
            self.carousel_frame, width=20, height=self.height - 20, bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )
        self.btn_left.pack(side='left', anchor='w')
        self.btn_left.pack_propagate(False)
        self.btn_left_label = Label(
            self.btn_left, text='<', bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=self.height - 20
        )
        self.btn_left_label.pack(anchor='center')
        self.bind_hover_actions(self.btn_left_label)
        self.btn_left_label.bind("<Button-1>", lambda event: self.scroll_left())

        self.image_frame = Frame(self.carousel_frame, width=self.width - 40, height=self.height - 20, bg='white')
        self.image_frame.pack(side='left')

        self.btn_right = Frame(
            self.carousel_frame, width=20, height=self.height - 20, bg=CUSTOM_COLOURS["FORM_BACKGROUND"]
        )
        self.btn_right.pack(side='right', anchor='e')
        self.btn_right.pack_propagate(False)
        self.btn_right_label = Label(
            self.btn_right, text='>', bg=CUSTOM_COLOURS["FORM_BACKGROUND"], height=self.height - 20
        )
        self.btn_right_label.pack(anchor='center')
        self.bind_hover_actions(self.btn_right_label)
        self.btn_right_label.bind("<Button-1>", lambda event: self.scroll_right())

        if image_list:
            self.resize_images()
            self.populate_images(self.carousel_index)

    def resize_images(self):
        for i in range(len(self.image_list)):
            # self.image_list[i] = self.image_list[i].resize((80, 80), Image.ANTIALIAS)
            self.thumbnail_list.append(self.image_list[i].resize((80, 80), Image.ANTIALIAS))

    def bind_hover_actions(self, widget):
        widget.bind("<Enter>", lambda event: self.button_hover_enter(widget))
        widget.bind("<Leave>", lambda event: self.button_hover_leave(widget))
        widget['cursor'] = 'hand2'

    def add_image(self, new_img=None):
        if not new_img:
            file_types = (
                ('PNG Images', '*.png')
            )
            new_img = fd.askopenfilename(
                title='Select an image',
                initialdir='/',
                filetypes=[file_types]
            )

        db = DBAccess()
        blob_image = db.convert_to_blob(Image.open(new_img))
        blob_image = Image.open(io.BytesIO(blob_image))
        blob_image_thumbnail = blob_image.resize((80, 80), Image.ANTIALIAS)
        self.image_list.append(blob_image)
        self.thumbnail_list.append(blob_image_thumbnail)

        if len(self.image_list) > 4:
            self.carousel_index = len(self.image_list) - 4

        self.populate_images(self.carousel_index)

    def populate_images(self, index):
        end_index = len(self.image_list)
        if index + 4 <= len(self.image_list):
            end_index = index + 4

        for child in self.image_frame.winfo_children():
            child.destroy()

        visible_images = []
        # db = DBAccess()
        for i in range(index, end_index):
            # visible_images.append(ImageTk.PhotoImage(self.image_list[i]))
            visible_images.append(ImageTk.PhotoImage(self.thumbnail_list[i]))
            image_label = Label(
                self.image_frame, image=visible_images[i - index], highlightthickness=1,
                highlightbackground='black'
            )
            image_label.image = visible_images[i-index]
            image_label.pack(side='left', padx=(12, 5) if i - index == 0 else (5, 5))
            image_label.pack_propagate(False)

            minus_label = Label(image_label, text="-", cursor='hand2')
            minus_label.pack(anchor='nw', side='left')
            minus_label.bind("<Button-1>", lambda event: self.remove_image(i))
            self.bind_hover_actions(minus_label)

    def remove_image(self, i):
        self.thumbnail_list.pop(i)
        self.image_list.pop(i)
        self.populate_images(self.carousel_index)

    def scroll_left(self):
        if self.carousel_index > 0:
            self.carousel_index -= 1
            self.populate_images(self.carousel_index)

    def scroll_right(self):
        if self.carousel_index + 4 < len(self.image_list):
            self.carousel_index += 1
            self.populate_images(self.carousel_index)

    @staticmethod
    def button_hover_enter(widget):
        widget['bg'] = 'white'

    @staticmethod
    def button_hover_leave(widget):
        widget['bg'] = CUSTOM_COLOURS["FORM_BACKGROUND"]

    def pack(self):
        self.carousel_frame.pack()

    def grid(self, row=0, column=0, columnspan=1):
        self.carousel_frame.grid(row=row, column=column, columnspan=columnspan)

    def get_images(self):
        return self.image_list


class CatalogueBrowser:
    def __init__(self, parent, catalogue_items, controller):
        self.controller = controller
        self.catalogue_frame = Frame(parent, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"])
        self.catalogue_frame.grid_propagate(False)
        self.catalogue_frame.grid_columnconfigure(1, weight=1)
        self.catalogue_items = catalogue_items
        self.start_index = 0
        self.end_index = 0
        self.calculate_indexes()

        # Nav buttons
        self.btn_frame = Frame(self.catalogue_frame)
        self.btn_left = ttk.Button(self.btn_frame, text="<<", command=self.btn_left_click)
        self.btn_right = ttk.Button(self.btn_frame, text=">>", command=self.btn_right_click)
        self.update_buttons()

        # Show results
        self.display_results()

    def results_count(self):
        return len(self.controller.names_matched)

    def btn_left_click(self):
        self.start_index -= 6
        self.change_page()

    def btn_right_click(self):
        self.start_index += 6
        self.change_page()

    def change_page(self):
        self.clear_frame()
        self.calculate_indexes()
        self.update_buttons()
        self.display_results()

    def clear_frame(self):
        for child in self.catalogue_frame.winfo_children():
            child.destroy()

    def calculate_indexes(self):
        if self.start_index + 6 < self.results_count():
            self.end_index = self.start_index + 6
        else:
            self.end_index = self.results_count()

    def update_buttons(self):
        self.btn_frame = Frame(self.catalogue_frame)
        self.btn_left = ttk.Button(self.btn_frame, text="<<", command=self.btn_left_click)
        self.btn_right = ttk.Button(self.btn_frame, text=">>", command=self.btn_right_click)
        self.btn_frame.grid(row=0, column=1, padx=(5, 40), pady=5, sticky='e')
        self.btn_right.pack(side='right', anchor='e')
        self.btn_left.pack(side='right', anchor='e')

        if self.results_count() <= 6:
            self.btn_left.pack_forget()
            self.btn_right.pack_forget()
            return

        if self.start_index == 0:
            self.btn_left['state'] = DISABLED
        else:
            self.btn_left['state'] = NORMAL

        if self.results_count() == self.end_index:
            self.btn_right['state'] = DISABLED
        else:
            self.btn_right['state'] = NORMAL

    def display_results(self):
        self.catalogue_items = self.controller.traverse_list(self.start_index, self.end_index)
        list_len = len(self.catalogue_items)
        self.create_search_label(
            f"Displaying {self.start_index + 1} to {self.end_index} of {self.results_count()} results"
        )
        # layout the tiles in two columns
        for i in range(list_len):
            col = 1
            if i % 2 == 0:
                col = 0
            item_tile = self.catalogue_items[i].create_tile(self.catalogue_frame)
            item_tile.grid(row=int(i / 2) + 1, column=col, pady=1, padx=1)

    def create_search_label(self, message):
        label = Label(
            self.catalogue_frame, text=message, bg=CUSTOM_COLOURS["FORM_BACKGROUND_PALE"],
            font=CUSTOM_FONTS["SEARCH_RESULTS_FONT"], justify=LEFT
        )
        label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    def pack(self):
        self.catalogue_frame.pack(side='top', fill='both', expand=True, anchor='n')

