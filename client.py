import socket
import datetime
import tkinter as tk
import threading
from sign import Sign
import pickle
from Player import player
from Home import *
from Host import *
from Gamer import *
SIP = "127.0.0.1"
SPORT = 55368
MPORT = 53476
PROG = 0
CHOICE = 0
IP = "0.0.0.0"
CLINET_ARR = []
lock = threading.Lock()
ANS_WORTH = 100
ANS_TIME = 60000
CNCT = 0
PROG = 0
QUESTNUM = 5


def before_game(root,s):
    screen1 = Sign(root, '400x150')
    print("hello")
    stat = False
    while True:
        if screen1.pressed_login2:
            print("1")
            send_answer(s, str(screen1.name) + "_" + str(screen1.passwrd))
            print("2")
            screen1.pressed = False
            screen1.pressed_login2 = False
            ans = all_mesage(s)
            print(ans)
            if ans == "connected":
                break
            screen1.login_wrong()
            while True:
                if screen1.pressed_login2:
                    break
        elif screen1.pressed_signup1:
            screen1.resety()
            screen1.sign_up()
            while True:
                if screen1.pressed_signup:
                    print("help")
                    screen1.pressed_signup = False
                    send_answer(s, "new_sign")  # continue
                    send_answer(s, str(screen1.name) + "_" + str(screen1.passwrd))
                    if all_mesage(s) == "succes":
                        print("succefully signed up")
                        stat = True
                        break
                    else:
                        screen1.taken_sign_up()
                        print("name already taken try again")
            if stat:
                break


            print("we did it")

    print("out")


def unpickle_something(s):
    return all_mesage(s,True)


def build_answer(ans):#builds apropriate answer according to protocol
    return str(len(ans))+"_"+ans



def send_answer(s,ans):
    s.send((build_answer(ans)).encode())


def all_mesage(sock,bytes = False):#recievs all of the message based on the message length given at the begining of the messsage
    lent = sock.recv(1).decode()
    while "_" not in lent:
        lent += sock.recv(1).decode()
    lent = int(lent[:-1])#recives the message length
    ans = sock.recv(lent).decode()
    while not len(ans) == lent:
        ans += sock.recv(lent)
    if bytes:
        lens = int(ans)
        ans = sock.recv(4096)
        while not len(ans) == lens:
            ans += sock.recv(4096)

        ans = pickle.loads(ans)
        print(ans)

    return ans#recieves the message


def client(root):
    global CRNT_FRM
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SIP, SPORT))
    before_game(root,s)
    print("enters game")
    clnt = unpickle_something(s)
    home_screen = Home(root,"800x300",clnt)
    while True:
        if home_screen.play:
            print("player succes")
            home_screen.player = False
            gmr = gamer(s,root,"800x300",home_screen)
            gmr.get_addr(0)
            gmr.cnct_client(clnt)
            print(gmr.Haddres)
            gmr.play_game()

            break
        elif home_screen.host:
            home_screen.host = False
            hst = host(s,root,"800x300",home_screen)
            print(hst.pin)
            hst.handle_lobby()
            hst.handle_quiz()
            break

    print("1")
    print("hkfd")
    print("2")



















if __name__ == '__main__':
    try:
        root = tk.Tk()
        thread = threading.Thread(target=client, args=(root,),daemon=True)  # creates new thread for client
        thread.start()
        root.mainloop()
    except:
        quit()