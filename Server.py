import socket
import random
import threading
IP = "0.0.0.0"
PORT = 55368
ACTIVEREQ={}
lock = threading.Lock()
import sqlite3
from Player import player
import pickle
from cli_obj import *
def build_answer(ans):#builds apropriate answer according to protocol
    return str(len(ans))+"_"+ans
def send_bytes(s,what):
    send_answer(s,str(len(what)))
    s.send(what)

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
    if bytes == True:
        lens = int(ans)
        ans = sock.recv(lens)
        while not len(ans) == lens:
            ans += sock.recv(lens)
    return ans#recieves the message
def all_mesage_test(sock,bytes = False):#recievs all of the message based on the message length given at the begining of the messsage
    print("3")
    lent = sock.recv(1)
    print("4")
    print(lent)
    print(lent.decode())
    while "_".encode() not in lent:
        lent += sock.recv(1)
    lent = int(lent[:-1])#recives the message length
    print(lent)
    ans = sock.recv(lent)
    while not len(ans) == lent:
        ans += sock.recv(lent)
    print(ans)
    ans = pickle.loads(ans)
    return ans#recieves the message


def pickle_something(somth,s):
    msg = pickle.dumps(somth)
    send_bytes(s, msg)




def update(connection,crsr,dict):
    for i in dict:
        val = dict[i].split("*")
        crsr.execute('SELECT `index` FROM login_info WHERE username = ? ', (i,))
        indx = crsr.fetchall()[0]
        indx = indx[0]
        print(indx)
        crsr.execute("UPDATE clients_info SET points = ?, num_firsts= ?,top_3_rate = ? ,games = ? WHERE  `index` = ?;",(int(val[0]),int(val[1]),int(val[2]),int(val[3]),int(indx),))
        connection.commit()



def sign_in(connection,crsr,name,paswd):
    print("shmoop")
    try:
        crsr.execute('INSERT INTO login_info (username, password)  VALUES (?, ?);',(name, paswd))
        connection.commit()
        return True
    except:
        return False
def create_player(connection,crsr,name):
    crsr.execute('INSERT INTO clients_info (points, num_firsts,top_3_rate,games)  VALUES (0,0 ,0,0);')
    connection.commit()
    clnt = player(crsr, name)
    print(clnt.name)
    return clnt

def login(crsr,name,paswd):
  print(name)
  checkUsername = crsr.execute('SELECT * FROM login_info WHERE username = ? and  password = ? ',(name,paswd))
  data = crsr.fetchall()
  if len(data) == 0:
    print("not connected")
    return False
  else:
    print("coonected")
    clnt = player(crsr,name)
    return clnt


def before_game(c,crsr,connection_login):
    while True:

        print("1")
        txt = all_mesage(c)
        print("2")
        if not txt == "new_sign":
            clnt = login(crsr,txt.split("_")[0],txt.split("_")[1])
            temp = temp_cli(txt.split("_")[0],txt.split("_")[1])
            if not clnt == False:
                send_answer(c,"connected")
                return [clnt,temp]
            send_answer(c, "not_connected")
        else:
            txt = all_mesage(c)
            ans = sign_in(connection_login,crsr,txt.split("_")[0],txt.split("_")[1])
            print(ans)
            if ans == True:
                clnt = create_player(connection_login,crsr,txt.split("_")[0])
                temp = temp_cli(txt.split("_")[0], txt.split("_")[1])
                send_answer(c, "succes")
                print("uploaded succefuly")
                return [clnt,temp]
            send_answer(c, "not_succes")

def handle(c,addr):#understands what client and assigns command accordingly
    connection_login = sqlite3.connect("login.db")
    crsr = connection_login.cursor()
    arr =  before_game(c,crsr,connection_login)
    clnt = arr[0]
    temp = arr[1]
    pickle_something(clnt,c)
    print(clnt.name)
    handle_game(connection_login,crsr,c,addr)
    while True:
        if all_mesage(c) == "REF":
            clnt = login(crsr,temp.name,temp.paswd)
            pickle_something(clnt, c)
            handle_game(connection_login, crsr, c, addr)


def handleactive(connection,crsr,c,addr):#assigns an active client a personalized id,and closes connection when finished
    num = random.randint(100000,999999)
    while num in ACTIVEREQ.values():
        num = random.randint(100000, 999999)
    lock.acquire()
    ACTIVEREQ[addr[0]] = num #assigns the client a personalized number code and lists him as an active client
    lock.release()
    send_answer(c,str((ACTIVEREQ[addr[0]])))#sends the active client his personalized password
    print(ACTIVEREQ)
    #  txt = all_mesage(c)
    plyr_lst = all_mesage_test(c,bytes=True)
    print(plyr_lst)
    update(connection,crsr,plyr_lst)
    return
    #waits until the active client responds(will delete the client from actives even when there is an unexpected disconnection
    if txt == "bye":

        lock.acquire()
        del ACTIVEREQ[addr[0]]  # deletes the host from dictionary thus allowing for the pin to be used
        lock.release()
        print("disconnected client")
    elif txt == "":
        lock.acquire()
        del ACTIVEREQ[addr[0]]  # deletes the host from dictionary thus allowing for the pin to be used
        lock.release()
        print("client disconnected")


def findkey(val):
    key_list = list(ACTIVEREQ.keys())
    print(key_list)
    val_list = list(ACTIVEREQ.values())
    print(val_list)
    return key_list[val_list.index(int(val))]



def handlepasive(c):#sends to the passive client the ip address of the active client with the desired number
    param = all_mesage(c)
    print(param)
    lock.acquire()
    try:

        saddr = findkey(param)#finds the corresponding ip for the num

    except:
        saddr = "no"
    lock.release()
    send_answer(c,saddr)
    print(saddr)









def handle_game(connection,crsr,c,addr):#understands what client and assigns command accordingly
    txt = all_mesage(c)
    if txt == "hello":
        handleactive(connection,crsr,c,addr)
    elif txt == "please":
        handlepasive(c)






def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP,PORT))
    print("server is up and runing")
    while True:
        s.listen()
        c, addr = s.accept()
        thread = threading.Thread(target = handle,args = (c,addr))
        thread.start()


if __name__ == '__main__':
    main()