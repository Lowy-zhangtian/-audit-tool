# main.py
import tkinter as tk
from gui.main_window import MainWindow

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("自动凭证复核系统")
        # The geometry will be set by MainWindow, but can be overridden here if needed
        # self.geometry("800x600") 

        self.main_window = MainWindow(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()