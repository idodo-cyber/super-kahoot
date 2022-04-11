import tkinter as tk
from functools import partial
from prettytable import PrettyTable

class hst_screens:
    def __init__(self, root, geometry,pin,home_screen):
        self.root = root
        self.given_pin = 0
        home_screen.resety_texty()
        self.geometry = geometry
        self.root.title("lobby")
        self.root.geometry(self.geometry)
        self.quest_button = False
        f = tk.Frame(root)
        f.place(relx=0, rely=0)
        title = tk.Label(f, text="wating for players....")
        title.config(font=("Ariel", 18))
        title.grid(row=0, column=0, sticky="NW")
        title = tk.Label(f, text="the pin is:")
        title.config(font=("Ariel", 18))
        title.grid(row=1, column=0, sticky="NW")
        title = tk.Label(f, text=pin)
        title.config(font=("Ariel", 18))
        title.grid(row=2, column=0, sticky="NW")
        title = tk.Label(f, text="people who have connected are:")
        title.config(font=("Ariel", 18))
        title.grid(row=3, column=0, sticky="NW")
        self.f = f

        self.cont = False
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

    def question(self, num, question, ans):
        f = tk.Frame(self.root)
        f.place(relx=0, rely=0)
        title = tk.Label(f, text="questin: " + str(num) + "/" + "5")
        title.config(font=("Ariel", 18))
        title.grid(row=0, column=0, sticky="NW")
        title = tk.Label(f, text=question)
        title.config(font=("Ariel", 18))
        title.grid(row=1, column=0, sticky="NW")
        title = tk.Label(f, text="A." + ans[0])
        title.config(font=("Ariel", 18))
        title.grid(row=2, column=0, sticky="NW")
        title = tk.Label(f, text="B." + ans[1])
        title.config(font=("Ariel", 18))
        title.grid(row=3, column=0, sticky="NW")
        title = tk.Label(f, text="C." + ans[2])
        title.config(font=("Ariel", 18))
        title.grid(row=4, column=0, sticky="NW")
        title = tk.Label(f, text="D." + ans[3])
        title.config(font=("Ariel", 18))
        title.grid(row=5, column=0, sticky="NW")
        self.f = f

    def ending(self,cli_arr):
        names = ["first", "second", "third"]
        f = tk.Frame(self.root)
        f.place(relx=0, rely=0)
        title = tk.Label(f, text="THE END!!!!!!")
        title.config(font=("Ariel", 18))
        title.grid(row=1, column=0, sticky="NW")
        n = 0
        n1 = 2
        for i in names:
            if n < len(cli_arr):
                title = tk.Label(f, text=i + ":" + cli_arr[n].name)
                title.config(font=("Ariel", 18))
                title.grid(row=n1, column=0, sticky="NW")
                title = tk.Label(f, text="with:" + str(cli_arr[n].temp.value))
                title.config(font=("Ariel", 18))
                title.grid(row=n1 + 1, column=0, sticky="NW")
                n1 += 2
                n += 1
            else:
                break
        B = tk.Button(f, text="new game", command=self.cont_quest)
        B.config(font=("Ariel", 18))
        B.grid(row=n1 + 1, column=1, sticky="NW")

        self.f =f




    def answer(self, ans,cli_arr):
        names = ["first", "second", "third"]
        f = tk.Frame(self.root)
        f.place(relx=0, rely=0)
        title = tk.Label(f, text="THE ANSWER IS: ")
        title.config(font=("Ariel", 18))
        title.grid(row=1, column=0, sticky="NW")
        title = tk.Label(f, text=ans)
        title.config(font=("Ariel", 18))
        title.grid(row=2, column=0, sticky="NW")
        n = 0
        n1 = 3
        for i in names:
            if n < len(cli_arr):
                title = tk.Label(f, text=i + " " + cli_arr[n].name)
                title.config(font=("Ariel", 18))
                title.grid(row=n1, column=0, sticky="NW")
                n1 += 1
                n += 1
            else:
                break
        B = tk.Button(f, text="continue", command=self.cont_quest)
        B.config(font=("Ariel", 18))
        B.grid(row=5, column=0, sticky="NW")

    def cont_quest(self):
        self.quest_button = True

    def reset(self):
        self.f.destroy()
    def cont_button(self):
        sign_up_button = tk.Button(self.root, text="continue", command=self.cont_func).grid(row=10, column=10)
    def cont_func(self):
        self.cont = True