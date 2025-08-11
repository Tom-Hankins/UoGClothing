import tkinter as tk
class Window(tk.Toplevel):
    open_windows = []

    def __init__(self, window_type, title, size="030x200", resize=True, parent=None):
        super().__init__(parent)
        self.geometry(f"{size}+10+10")
        self.title(title)
        self.resizable(height=resize, width=resize)
        self.iconbitmap("images/tshirt.ico")
        self.window_type = window_type
        Window.open_windows.append(self)

    @staticmethod
    def close_windows(win_type="ALL"):
        for window in Window.open_windows:
            if window.window_type == win_type or win_type == "ALL":
                window.destroy()
                window.update()
