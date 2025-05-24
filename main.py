import tkinter as tk
from app import App
from windows import set_dpi_awareness

set_dpi_awareness

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
