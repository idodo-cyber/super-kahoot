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
from upload_screen import *
from quiz import *
from encrypt import *
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
            s.send(str(screen1.name) + "_" + str(screen1.passwrd))
            print("2")
            screen1.pressed = False
            screen1.pressed_login2 = False
            ans = s.recv()
            print(ans)
            if ans == "connected":
                print("woodooo")
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
                    s.send("new_sign")  # continue
                    s.send(str(screen1.name) + "_" + str(screen1.passwrd))
                    if s.recv() == "succes":
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
    return s.recv(True)


def build_answer(ans):#builds apropriate answer according to protocol
    return str(len(ans))+"_"+ans





def pickle_something(s, somth):
    msg = pickle.dumps(somth)
    s.send(msg)
    print("sent")





def send_answer(s,ans):
    s.send((build_answer(ans)).encode())

def send_bytes(s,ans):
    s.send((str(len(ans)) + "_" ).encode() + ans)


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

def all_mesage_test(sock, pickled=True):  # recievs all of the message based on the message length given at the begining of the messsage
    print("3")
    lent = sock.recv(1)
    print("4")
    print(lent)
    print(lent.decode())
    while "_".encode() not in lent:
        lent += sock.recv(1)
    lent = int(lent[:-1])  # recives the message length
    print(lent)
    ans = sock.recv(lent)
    while not len(ans) == lent:
        ans += sock.recv(lent)
    print(ans)
    if pickled:
        ans = pickle.loads(ans)
    return ans  # recieves the message


def connect_server(c):
    pubkey = all_mesage_test(c,True)
    enc = crypt(c)
    enc.create_aes_client()
    key_enc = enc.encrypt_rsa_client(enc.aes_key,pubkey)
    send_bytes(c,key_enc)
    return enc


def client(root):
    global CRNT_FRM
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SIP, SPORT))
    enc = connect_server(s)
    before_game(root,enc)
    print("enters game")
    clnt = unpickle_something(enc)
    home_screen = Home(root, "800x300", clnt)
    while True:

        if home_screen.play:
            print("player succes")
            home_screen.play = False
            gmr = gamer(enc,root,"800x300",home_screen)
            gmr.get_addr(0)
            gmr.cnct_client(clnt)
            print(gmr.Haddres)
            gmr.play_game()
            gmr.henc.sock.close()
            enc.send("REF")
            print("sdfsdf")
            clnt = enc.recv(True)
            home_screen = Home(root, "800x300", clnt)

        elif home_screen.host:
            home_screen.host = False
            hst = host(enc,root,"800x300",home_screen)
            print(hst.pin)
            hst.handle_quiz_choice()


            hst.handle_lobby()
            hst.handle_quiz()
            print("1")
            hst.send_clients()

            hst.lobby.reset()
            print("2")
            hst.end_client()
            print("3")
            hst.Mscok.close()
            print("4")
            enc.send("REF")
            print("fdfdgf")
            clnt = enc.recv(True)
            home_screen = Home(root, "800x300", clnt)



        elif home_screen.upload:
            home_screen.upload = False
            print("hihh")
            upld = upld_screen(root,home_screen)
            while True:
                if upld.next:
                    upld.next_stage()
                    upld.next = False
                    while True:
                        if upld.pressed_signup:
                            print(upld.name)
                            print(upld.limit)
                            upld.pressed_signup = False
                            quz = Quiz(upld.name,upld.file_cont)
                            if not upld.limit == "":
                                quz.insert_limit(upld.limit)
                            enc.send("quiz")
                            pickle_something(enc,quz)
                            print("sent quiz")
                            damp = enc.recv()
                            if not damp  == "no":
                                print("succes")
                                break
                            else:
                                print("nope")






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