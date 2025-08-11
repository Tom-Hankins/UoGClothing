import tkinter as tk
from homepage import MainFrame

class App (tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UoG Clothing Ltd.")
        self.geometry("900x620")
        self.iconbitmap(r"images/tshirt.ico")
        self.resizable(False, False)

if __name__ == '__main__':
    app = App()
    MainFrame(app)
    app.mainloop()


