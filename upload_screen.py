import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from functools import partial
class upld_screen:
    def __init__(self, root,home_screen):
        self.root = root
        self.pressed_signup = False
        home_screen.resety_texty()
        self.next = False
         # Size of the window
        self.root.title('upload')
        my_font1 = ('times', 18, 'bold')
        l1 = tk.Label(self.root, text='Upload File & read', width=30, font=my_font1)
        l1.grid(row=1, column=1)
        b1 = tk.Button(self.root, text='Upload File',
                       width=20, command=self.upload_file)
        b1.grid(row=2, column=1)

    def upload_file(self):
        file = filedialog.askopenfilename()
        self.file_name = file
        fob = open(file, 'r')
        self.file_cont = fob.read()
        print(fob.read())
        self.next = True
        # file = filedialog.askopenfile()
        #print(file.read())

    def next_stage(self):
        voop = self.file_name.split("/")[-1]
        Label(self.root, text="file uploaded: " + voop).grid(row=20, column=5)
        usernameLabel = Label(self.root, text="quiz Name").grid(row=5, column=0)
        self.given_username = StringVar()
        usernameEntry = Entry(self.root, textvariable=self.given_username).grid(row=5, column=1)

        # password label and password entry box
        passwordLabel = Label(self.root, text="limit").grid(row=8, column=0)
        self.given_password = StringVar()
        passwordEntry = Entry(self.root, textvariable=self.given_password, show='*').grid(row=8, column=1)
        validate_login1 = partial(self.validateLogin, self.given_username, self.given_password)
        loginButton = Button(self.root, text="send", command=validate_login1).grid(row=10, column=0)


    def validateLogin(self, name,limit):
        self.name = name.get()
        self.limit = limit.get()
        self.pressed_signup = True




