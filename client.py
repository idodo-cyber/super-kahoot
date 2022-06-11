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
from list_quizes import *
from Server_crash import *
import sys

SIP = sys.argv[1]
#SIP ="192.168.43.32"
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
    while True:
        if screen1.pressed_login2:

            s.send(str(screen1.name) + "_" + str(screen1.passwrd))

            screen1.pressed = False
            screen1.pressed_login2 = False
            ans = s.recv()

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

                    screen1.pressed_signup = False
                    s.send("new_sign")  # continue
                    s.send(str(screen1.name) + "_" + str(screen1.passwrd))
                    if s.recv() == "succes":

                        stat = True
                        break
                    else:
                        screen1.taken_sign_up()

            if stat:
                break







def unpickle_something(s):
    return s.recv(True)


def build_answer(ans):#builds apropriate answer according to protocol
    return str(len(ans))+"_"+ans





def pickle_something(s, somth):
    msg = pickle.dumps(somth)
    s.send(msg)






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


    return ans#recieves the message

def all_mesage_test(sock, pickled=True):  # recievs all of the message based on the message length given at the begining of the messsage

    lent = sock.recv(1)



    while "_".encode() not in lent:
        lent += sock.recv(1)
    lent = int(lent[:-1])  # recives the message length

    ans = sock.recv(lent)
    while not len(ans) == lent:
        ans += sock.recv(lent)

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
    try:
        global CRNT_FRM
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SIP, SPORT))
        enc = connect_server(s)
        before_game(root,enc)


        while True:
            clnt = enc.recv(True)
            home_screen = Home(root, "800x300", clnt)
            while True:
                if home_screen.play:

                    home_screen.play = False
                    gmr = gamer(enc,root,"800x300",home_screen)
                    gmr.get_addr(0)
                    gmr.cnct_client(clnt)

                    try:
                        gmr.play_game()

                    except ValueError:
                        gmr.henc.sock.close()
                    except:
                        gmr.gmr.error()
                        while True:
                            if gmr.gmr.home:
                                break

                    gmr.henc.sock.close()
                    enc.send("REF")
                    break



                elif home_screen.host:
                    home_screen.host = False
                    hst = host(enc,root,"800x300",home_screen)

                    hst.handle_quiz_choice()


                    hst.handle_lobby()
                    try:
                        hst.handle_quiz()

                        try:
                            hst.send_clients()
                        except Exception as ex:

                            template = "An exception of type {0} occurred. Arguments:\n{1!r}"

                            message = template.format(type(ex).__name__, ex.args)

                            print(message)
                            hst.end_client(ERR = True)
                        hst.lobby.reset()

                        hst.end_client()
                    except Exception as ex:

                        template = "An exception of type {0} occurred. Arguments:\n{1!r}"

                        message = template.format(type(ex).__name__, ex.args)

                        print(message)
                        hst.lobby.no_player()
                        while True:
                            if hst.lobby.home:
                                hst.send_clients()
                                break




                    hst.Mscok.close()

                    enc.send("REF")
                    break





                elif home_screen.upload:
                    var = False
                    home_screen.upload = False
                    upld = upld_screen(root,home_screen)
                    while True:

                        if upld.next :
                            upld.next_stage()
                            upld.next = False
                            while True:
                                if not upld.nextq:
                                    upld.resety()
                                    upld = upld_screen(root, home_screen)
                                    upld.add_eror()
                                    break
                                if upld.pressed_signup:
                                    upld.pressed_signup = False
                                    quz = Quiz(upld.name,upld.file_cont)

                                    if not upld.limit == "":
                                        quz.insert_limit(upld.limit)
                                    if not var:
                                        enc.send("quiz")
                                    pickle_something(enc,quz)

                                    damp = enc.recv()
                                    if  damp  == "succes":
                                        upld.home = True
                                        break
                                    else:
                                        var = True

                                        upld.wrong_quiz(damp)
                                elif upld.home:

                                    break

                        elif upld.home:
                            upld.home = False
                            enc.send("home")
                            break


                    enc.send("REF")
                    break
                elif home_screen.listq:
                    home_screen.listq = False
                    enc.send("lists")
                    lists = enc.recv(True)

                    lstq = list_q(root,lists[0],lists[1],home_screen)
                    while True:
                        if lstq.home:
                            lstq.home = False
                            enc.send("REF")
                            break
                    break










    except Exception as ex:


        template = "An exception of type {0} occurred. Arguments:\n{1!r}"

        message = template.format(type(ex).__name__, ex.args)

        print(message)
        crsh_screen = crsh_srvr(root)























if __name__ == '__main__':
    try:
        root = tk.Tk()
        thread = threading.Thread(target=client, args=(root,),daemon=True)  # creates new thread for client
        thread.start()
        root.mainloop()
    except:
        quit()