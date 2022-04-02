from tkinter import *
from functools import partial
from prettytable import PrettyTable

class Home:
    def table_create(self):
        lst = [("points",self.player.points),("ultimate win #",self.player.num_firsts),("win rate",self.player.top_3_rate)]
        t = Text(self.root)  # Inside text widget we would put our table

        x = PrettyTable()

        x.field_names = ["points", "ultimate win #", "win rate"]

        x.add_row([self.player.points, self.player.num_firsts, self.player.top_3_rate])


        t.insert(INSERT, x)  # Inserting table in text widget
        t.config(state=DISABLED)
        t.place(x=170, y=20, height=200, width=380)
        self.t = t

    def vali_player(self):
        self.play = True
    def vali_host(self):
        self.host = True

    def __init__(self, root, geometry,player):
        self.play = False
        self.host = False
        self.root = root
        self.resety()
        self.geometry = geometry
        self.root.title("Home")
        self.root.geometry(self.geometry)
        self.player = player
        Label(self.root, text="hello " + self.player.name).grid(row=0, column=0)
        Label(self.root, text="your stats:").grid(row=5, column=5)
        self.table_create()
        host = Button(self.root, text="host", command=self.vali_host).grid(row=20, column=20)


        player = Button(self.root, text="play", command=self.vali_player).grid(row=25, column=20)

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

    def resety_texty(self):
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
        self.t.destroy()

