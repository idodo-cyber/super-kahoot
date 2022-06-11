from tkinter import *
from functools import partial

class choice:
    def __init__(self,root,geometry,home_screen):
        self.root = root
        self.pressed = False
        self.geometry = geometry
        home_screen.resety_texty()
        self.root.title("begining")
        self.root.geometry(self.geometry)
        usernameLabel = Label(self.root, text="quiz name").grid(row=0, column=0)
        self.given_name = StringVar()
        usernameEntry = Entry(self.root, textvariable=self.given_name).grid(row=0, column=1)
        usernameLabel = Label(self.root, text="number of players").grid(row=0, column=2)
        self.given_num = StringVar()
        usernameEntry = Entry(self.root, textvariable=self.given_num).grid(row=0, column=3)

        # password label and password entry box
        validate_login1 = partial(self.validate_signup1, self.given_name,self.given_num)
        loginButton = Button(self.root, text="enter", command=validate_login1).grid(row=6, column=0)



    def validate_signup1(self, username1,num):
        self.name = username1.get()
        self.num = num.get()
        self.pressed = True

        return




    def not_good(self):
        self.resety()
        self.root.title("begining")
        self.root.geometry(self.geometry)
        usernameLabel = Label(self.root, text="quiz name").grid(row=0, column=0)
        self.given_name = StringVar()
        usernameEntry = Entry(self.root, textvariable=self.given_name).grid(row=0, column=1)

        # password label and password entry box
        validate_login1 = partial(self.validate_signup1, self.given_name)
        usernameLabel = Label(self.root, text="number of players").grid(row=0, column=2)
        self.given_num = StringVar()
        usernameEntry = Entry(self.root, textvariable=self.given_num).grid(row=0, column=3)

        # password label and password entry box
        validate_login1 = partial(self.validate_signup1, self.given_name, self.given_num)

        loginButton = Button(self.root, text="enter", command=validate_login1).grid(row=6, column=0)
        not_good = Label(self.root, text="could not access quiz").grid(row=10, column=5)

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
