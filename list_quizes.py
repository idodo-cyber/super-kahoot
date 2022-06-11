from tkinter import *
from functools import partial

class list_q:
    def __init__(self,root,list_quiz,list_params,home_screen):
        home_screen.resety_texty()
        self.home = False
        self.root = root
        self.lst1 = list_quiz
        self.lst2 = list_params
        b1 = Button(self.root, text='return home', width=20, command=self.valid_home).grid(row=0, column=3)


        self.scrollbar = Scrollbar(self.root, orient='vertical')
        self.list1 = Listbox(self.root,width=self.max_width(self.lst1), yscrollcommand=self.yscroll1)
        self.list1.grid(row = 1, column = 0,ipady = 50)
        self.list2 = Listbox(self.root,width=self.max_width(self.lst2), yscrollcommand=self.yscroll2)
        self.list2.grid(row = 1, column = 1,ipady = 50)
        self.scrollbar.config(command=self.yview)
        self.scrollbar.grid(row = 1, column = 2,ipady=100)
        for values in range(len(self.lst1)):
            self.list1.insert(END, self.lst1[values]  )
            self.list2.insert(END, self.lst2[values]  )


        lbl = Label( text="quizes", anchor="w", font=("Helvetica", "24"))
        lbl.grid(row = 0, column = 0)
        lbl2 = Label( text="limits", anchor="w", font=("Helvetica", "24"))
        lbl2.grid(row = 0, column = 1)


    def valid_home(self):
        self.home = True

    def yscroll1(self, *args):
        if self.list2.yview() != self.list1.yview():
            self.list2.yview_moveto(args[0])
        self.scrollbar.set(*args)

    def yscroll2(self, *args):
        if self.list1.yview() != self.list2.yview():
            self.list1.yview_moveto(args[0])
        self.scrollbar.set(*args)

    def yview(self, *args):
        self.list1.yview(*args)
        self.list2.yview(*args)
    def max_width(self,list_items):
        len_max = 0
        for m in list_items:
            if len(m) > len_max:
                len_max = len(m)
        return len_max

