import tkinter as tk


class crsh_srvr:
    def __init__(self, root):
        self.root = root
        self.resety()

        self.root.title("EROR")
        self.root.geometry("800x300")
        f = tk.Frame(root)
        f.place(relx=0, rely=0)
        title = tk.Label(f, text="SERVER CRASHED")
        title.config(font=("Ariel", 18))
        title.grid(row=0, column=0, sticky="NW")
        title = tk.Label(f, text="try closing the game and try again later")
        title.config(font=("Ariel", 18))
        title.grid(row=1, column=0, sticky="NW")
    def resety(self):
        def all_children(window):
            _list = window.winfo_children()

            for item in _list:
                if item.winfo_children():
                    _list.extend(item.winfo_children())

            return _list

        widget_list = all_children(self.root)
        for item in widget_list:
            try:
                item.grid_forget()
            except AttributeError:
                pass
