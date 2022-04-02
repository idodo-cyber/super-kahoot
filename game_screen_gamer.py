import tkinter as tk
from functools import partial
class gmr_screens:
    def __init__(self, root, geometry,home_screen):
        self.root = root
        home_screen.resety_texty()
        self.geometry = geometry
        self.pin =0
        self.root.title("lobby")
        self.root.geometry(self.geometry)
        self.pressed_click = False
        f = tk.Frame(root)
        f.place(relx=0, rely=0)
        n = 0
        pinlabel = tk.Label(self.root, text="Password").grid(row=n + 1, column=0)
        self.given_pin = tk.StringVar()
        pinentry = tk.Entry(self.root, textvariable=self.given_pin).grid(row=n + 1, column=1)
        validate_pin1 = partial(self.validate_pin,self.given_pin)
        loginButton = tk.Button(self.root, text="pin", command=validate_pin1).grid(row=6, column=0)
        self.f = f


    def validate_pin(self, pin1):
        self.pin = pin1.get()
        return

    def reset(self):
        self.f.destroy()

    def waiting(self):
        self.resety()
        self.f = tk.Frame(self.root)
        self.f.place(relx=0, rely=0)
        title = tk.Label(self.f, text="please wait for other players")
        title.config(font=("Ariel", 18))
        title.grid(row=0, column=0, sticky="NW")

    def answer_screen(self):
        global CRNT_FRM
        self.reset()
        f = tk.Frame(self.root)
        f.place(relx=0, rely=0)
        click_A = partial(self.validate_click, "A")
        click_B = partial(self.validate_click, "B")
        click_C = partial(self.validate_click, "C")
        click_D = partial(self.validate_click, "D")
        title = tk.Label(f, text="what is the answer?:")
        title.config(font=("Ariel", 18))
        title.grid(row=1, column=0, sticky="NW")
        B = tk.Button(f, text="A", command=click_A)
        B.config(font=("Ariel", 18))
        B.grid(row=2, column=0, sticky="NW")
        B = tk.Button(f, text="B", command=click_B)
        B.config(font=("Ariel", 18))
        B.grid(row=3, column=0, sticky="NW")
        B = tk.Button(f, text="C", command=click_C)
        B.config(font=("Ariel", 18))
        B.grid(row=4, column=0, sticky="NW")
        B = tk.Button(f, text="D", command=click_D)
        B.config(font=("Ariel", 18))
        B.grid(row=5, column=0, sticky="NW")
        self.f = f

    def between(self, arr):
        global CRNT_FRM
        f = tk.Frame(self.root)
        f.place(relx=0, rely=0)
        print(arr[1])
        if not arr[2] == "0":
            title = tk.Label(f, text="congrats!!!!")
            title.config(font=("Ariel", 18))
            title.grid(row=1, column=0, sticky="NW")
        else:
            title = tk.Label(f, text="fail")
            title.config(font=("Ariel", 18))
            title.grid(row=1, column=0, sticky="NW")
        title = tk.Label(f, text="you gained: " + arr[2])
        title.config(font=("Ariel", 18))
        title.grid(row=2, column=0, sticky="NW")
        title = tk.Label(f, text="total points: " + arr[1])
        title.config(font=("Ariel", 18))
        title.grid(row=3, column=0, sticky="NW")
        title = tk.Label(f, text="your place:" + arr[3])
        title.config(font=("Ariel", 18))
        title.grid(row=4, column=0, sticky="NW")

        self.f = f

    def validate_click(self,letter):
        self.choice = letter
        self.pressed_click = True
        return

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
