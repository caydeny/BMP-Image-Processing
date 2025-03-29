import tkinter as tk
from gui import GUI

if __name__ == "__main__":
    root = tk.Tk()
    root.title("BMP Processor")
    app = GUI(root)
    root.mainloop()