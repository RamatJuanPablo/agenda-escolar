import tkinter as tk
from agendaescolar.ui import AgendaEscolarUI
from agendaescolar.storage import Storage

def main():
    storage = Storage()
    root = tk.Tk()
    app = AgendaEscolarUI(root, storage)
    root.mainloop()

if __name__ == "__main__":
    main()