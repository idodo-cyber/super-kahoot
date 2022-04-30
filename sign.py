from tkinter import *
from functools import partial

class Sign:

    def validateLogin(self, username1,password):
        self.name = username1.get()
        self.passwrd = password.get()
        self.pressed_login2 = True
        #print("hello")
        return
    def sign_up_cmnd(self):
        self.pressed_signup1 = True

    def login_wrong(self):
        self.resety()
        self.login()
        not_good = Label(self.root, text="incorret. please try again").grid(row=10, column=5)




    def validate_signup1(self, username1,password):
        self.name = username1.get()
        self.passwrd = password.get()
        self.pressed_signup = True
        return

    def sign_up(self):
        self.root.title("sign_up")
        self.root.geometry(self.geometry)
        usernameLabel = Label(self.root, text="User Name").grid(row=0, column=0)
        self.given_username = StringVar()
        usernameEntry = Entry(self.root, textvariable=self.given_username).grid(row=0, column=1)

        # password label and password entry box
        passwordLabel = Label(self.root, text="Password").grid(row=1, column=0)
        self.given_password = StringVar()
        passwordEntry = Entry(self.root, textvariable=self.given_password, show='*').grid(row=1, column=1)
        validateLogin1 = partial(self.validate_signup1, self.given_username, self.given_password)
        loginButton = Button(self.root, text="sign up", command=validateLogin1).grid(row=4, column=0)


    def taken_sign_up(self):
        self.resety()
        self.sign_up()
        not_good = Label(self.root, text="name already taken try another").grid(row=20, column=5)


    def login(self):
        self.resety()
        self.root.title("login")
        self.root.geometry(self.geometry)
        usernameLabel = Label(self.root, text="User Name").grid(row=0, column=0)
        self.given_username = StringVar()
        usernameEntry = Entry(self.root, textvariable=self.given_username).grid(row=0, column=1)

        # password label and password entry box
        passwordLabel = Label(self.root, text="Password").grid(row=1, column=0)
        self.given_password = StringVar()
        passwordEntry = Entry(self.root, textvariable=self.given_password, show='*').grid(row=1, column=1)
        validate_login1 = partial(self.validateLogin, self.given_username, self.given_password)
        loginButton = Button(self.root, text="Login", command=validate_login1).grid(row=6, column=0)

    def __init__(self,root,geometry):
        self.root = root
        self.pressed_login = False
        self.pressed_signup = False
        self.pressed_login2 = False
        self.pressed_login1 = False
        self.pressed_signup1 = False
        self.geometry = geometry
        self.root.title("begining")
        self.root.geometry(self.geometry)
        usernameLabel = Label(self.root, text="User Name").grid(row=0, column=0)
        self.given_username = StringVar()
        usernameEntry = Entry(self.root, textvariable=self.given_username).grid(row=0, column=1)

        # password label and password entry box
        passwordLabel = Label(self.root, text="Password").grid(row=1, column=0)
        self.given_password = StringVar()
        passwordEntry = Entry(self.root, textvariable=self.given_password, show='*').grid(row=1, column=1)
        validate_login1 = partial(self.validateLogin, self.given_username, self.given_password)
        loginButton = Button(self.root, text="Login", command=validate_login1).grid(row=6, column=0)
        sign_up_button = Button(self.root, text="sign up", command=self.sign_up_cmnd).grid(row=4, column=0)

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

