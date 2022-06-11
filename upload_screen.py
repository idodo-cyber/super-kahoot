import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from functools import partial
class upld_screen:
    def __init__(self, root,home_screen):
        self.root = root
        self.pressed_signup = False
        self.home = False
        self.nextq  = ""
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
        b2 = tk.Button(self.root, text='return home',
                       width=20, command=self.home_ret)
        b2.grid(row=3, column=1)


    def home_ret(self):
        self.home = True


    def upload_file(self):
        file = filedialog.askopenfilename()
        self.file_name = file
        fob = open(file, 'r')
        self.file_cont = fob.read()
        self.next = True

        self.nextq = self.check_file()


       


    def add_eror(self):
        Label(self.root, text="file does not fit in appropriate format").grid(row=4, column=0)


    def check_file(self):
        try:
            with open('test.txt', 'r+') as file:
                file.write(self.file_cont)
                first_lines = "".join([file.readline() for _ in range(5)]).split("\n")
                num = 1
                quest = first_lines[0]
                arr1 = self.split_lines(first_lines[1:])


                if "@_end_@" not in self.file_cont:
                    raise
                while not "@_end_@" in first_lines:
                    for i in first_lines[1:-1]:
                        if "_T" in i or "_F" in i:
                            ans = i.split("_")
                        else:
                            raise
                    first_lines = "".join([file.readline() for _ in range(5)]).split("\n")

                    if not "@_end_@" in first_lines:
                        num += 1
                        quest = first_lines[0]
                        arr1 = self.split_lines(first_lines[1:])
            return True
        except:
            return False

    def split_lines(self, frst):
        arr = []
        l = 0
        for i in frst:
            var = i.split("_")
            arr.append(var[0])
            l += 1
        return arr


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



    def wrong_quiz(self,msg):
        self.next_stage()
        Label(self.root, text=msg).grid(row=4, column=0)



    def next_stage(self):
        self.resety()
        voop = self.file_name.split("/")[-1]
        Label(self.root, text="file uploaded: " + voop).grid(row=20, column=5)
        usernameLabel = Label(self.root, text="quiz Name").grid(row=5, column=0)
        self.given_username = StringVar()
        usernameEntry = Entry(self.root, textvariable=self.given_username).grid(row=5, column=1)

        # password label and password entry box
        passwordLabel = Label(self.root, text="limit").grid(row=8, column=0)
        self.given_password = StringVar()
        passwordEntry = Entry(self.root, textvariable=self.given_password).grid(row=8, column=1)
        validate_login1 = partial(self.validateLogin, self.given_username, self.given_password)
        loginButton = Button(self.root, text="send", command=validate_login1).grid(row=10, column=0)
        b2 = tk.Button(self.root, text='return home',
                       width=20, command=self.home_ret)
        b2.grid(row=3, column=1)


    def validateLogin(self, name,limit):
        self.name = name.get()
        self.limit = limit.get()
        self.pressed_signup = True




