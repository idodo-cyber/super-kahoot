import tkinter as tk
from functools import partial
from prettytable import PrettyTable

class hst_screens:
    def __init__(self, root, geometry,pin,home_screen):
        self.root = root
        self.given_pin = 0
        self.home = False
        home_screen.resety_texty()
        self.geometry = geometry
        self.root.title("lobby")
        self.root.geometry(self.geometry)
        self.quest_button = False
        self.ref = False
        self.pin = pin
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
        ref_button = tk.Button(f, text="REFRESH", command=self.refresh)
        ref_button.config(font=("Ariel", 18))
        ref_button.grid(row=5, column=5, sticky="NW")
        self.f = f


        self.cont = False



    def no_player(self):

            self.resety()
            f = tk.Frame(self.root)
            f.place(relx=0, rely=0)
            title = tk.Label(f, text="all players have disconnected")
            title.config(font=("Ariel", 18))
            title.grid(row=0, column=0, sticky="NW")
            title = tk.Label(f, text="the game is over :(")
            title.config(font=("Ariel", 18))
            title.grid(row=1, column=0, sticky="NW")
            title = tk.Label(f, text="you can return to home screen if you'd like")
            title.config(font=("Ariel", 18))
            title.grid(row=3, column=0, sticky="NW")
            ref_button = tk.Button(f, text="return home", command=self.home_ret)
            ref_button.config(font=("Ariel", 18))
            ref_button.grid(row=5, column=5, sticky="NW")

    def home_ret(self):
        self.home = True





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

    def refresh(self):
        self.ref = True


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



    def refresh(self):
        self.ref  = True



    def update_lobby(self,arr,max):
        self.resety()
        title = tk.Label(self.f, text="wating for players....")
        title.config(font=("Ariel", 18))
        title.grid(row=0, column=0, sticky="NW")
        title = tk.Label(self.f, text="the pin is:")
        title.config(font=("Ariel", 18))
        title.grid(row=1, column=0, sticky="NW")
        title = tk.Label(self.f, text=self.pin)
        title.config(font=("Ariel", 18))
        title.grid(row=2, column=0, sticky="NW")
        title = tk.Label(self.f, text="people who have connected are:")
        title.config(font=("Ariel", 18))
        title.grid(row=3, column=0, sticky="NW")
        
        n = 0
        n1 = 6
        for i in arr:
            if n < len(arr):
                title = tk.Label(self.f, text=i.name)
                title.config(font=("Ariel", 18))
                title.grid(row=n1, column=0, sticky="NW")
                n1 += 1

            else:
                break


        if len(arr) == max:
            self.cont_button(n1)



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
        B.grid(row=n1+1, column=0, sticky="NW")

    def cont_quest(self):
        self.quest_button = True

    def reset(self):
        self.f.destroy()
    def cont_button(self,n):
        sign_up_button = tk.Button(self.f, text="continue", command=self.cont_func)
        sign_up_button.config(font=("Ariel", 18))
        sign_up_button.grid(row=n+1, column=0, sticky="NW")
    def cont_func(self):
        self.cont = True