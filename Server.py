import socket
import random
import threading

IP = "0.0.0.0"
PORT = 55368
ACTIVEREQ = {}
ACTIVEENC = {}
lock = threading.Lock()
import sqlite3
from Player import player
import pickle
from cli_obj import *
from encrypt import *
from hast_pack import *


def connect_client(c):
    enc = crypt(c)
    pickle_something1(enc.publicKey, c)
    enc_key = all_mesage_test(c, False)
    enc.create_aes_server(enc_key)
    return enc


def send_bytes1(s, ans):
    s.send((str(len(ans)) + "_").encode() + ans)


def build_answer(ans):  # builds apropriate answer according to protocol
    return str(len(ans)) + "_" + ans


def send_bytes(s, what):
    send_answer(s, str(len(what)))
    s.send(what)


def send_answer(s, ans):
    s.send((build_answer(ans)).encode())


def all_mesage(sock,
               bytes=False):  # recievs all of the message based on the message length given at the begining of the messsage
    lent = sock.recv(1).decode()
    while "_" not in lent:
        lent += sock.recv(1).decode()
    lent = int(lent[:-1])  # recives the message length
    ans = sock.recv(lent).decode()
    while not len(ans) == lent:
        ans += sock.recv(lent)
    if bytes == True:
        lens = int(ans)
        ans = sock.recv(lens)
        while not len(ans) == lens:
            ans += sock.recv(lens)
    return ans  # recieves the message


def all_mesage_test(sock,
                    pickle=True):  # recievs all of the message based on the message length given at the begining of the messsage

    lent = sock.recv(1)

    while "_".encode() not in lent:
        lent += sock.recv(1)
    lent = int(lent[:-1])  # recives the message length

    ans = sock.recv(lent)
    while not len(ans) == lent:
        ans += sock.recv(lent)

    if pickle:
        ans = pickle.loads(ans)
    return ans  # recieves the message


def pickle_something(somth, s):
    msg = pickle.dumps(somth)
    s.send(msg)


def pickle_something1(somth, s):
    msg = pickle.dumps(somth)
    send_bytes1(s, msg)


def update(connection, crsr, dict):
    for i in dict:
        val = dict[i].split("*")
        crsr.execute('SELECT `index` FROM login_info WHERE username = ? ', (i,))
        indx = crsr.fetchall()[0]
        indx = indx[0]

        crsr.execute("UPDATE clients_info SET points = ?, num_firsts= ?,top_3_rate = ? ,games = ? WHERE  `index` = ?;",
                     (int(val[0]), int(val[1]), float(val[2]), int(val[3]), int(indx),))
        connection.commit()


def sign_in(connection, crsr, name, paswd):

    try:
        crsr.execute('INSERT INTO login_info (username, password)  VALUES (?, ?);', (name, paswd))
        connection.commit()
        return True
    except:
        return False


def create_player(connection, crsr, name):
    crsr.execute('INSERT INTO clients_info (points, num_firsts,top_3_rate,games)  VALUES (0,0 ,0,0);')
    connection.commit()
    clnt = player(crsr, name)

    return clnt


def login(crsr, name, paswd):

    checkUsername = crsr.execute('SELECT * FROM login_info WHERE username = ? and  password = ? ', (name, paswd))
    data = crsr.fetchall()
    if len(data) == 0:

        return False
    else:

        clnt = player(crsr, name)
        return clnt


def get_quiz(crsr, c, clnt):
    while True:
        name = c.recv()
        crsr.execute('SELECT * FROM quizes WHERE  name = ? ', (name,))
        data = crsr.fetchall()

        index = data[0]
        index = index[0]
        limit = data[0]
        limit = limit[2]
        if clnt.comp_limit(limit):

            crsr.execute('SELECT content FROM q_and_a WHERE  `index` = ? ', (index,))
            data = crsr.fetchall()[0]

            data = data[0]
            c.send(data)
            break
        else:

            c.send("no")





def before_game(c, crsr, connection_login):
    while True:

        txt = c.recv()

        if not txt == "new_sign":
            clnt = login(crsr, txt.split("_")[0], txt.split("_")[1])
            temp = temp_cli(txt.split("_")[0], txt.split("_")[1])
            if not clnt == False:
                c.send("connected")
                return [clnt, temp]
            c.send("not_connected")
        else:
            txt = c.recv()
            ans = sign_in(connection_login, crsr, txt.split("_")[0], txt.split("_")[1])

            if ans == True:
                clnt = create_player(connection_login, crsr, txt.split("_")[0])
                temp = temp_cli(txt.split("_")[0], txt.split("_")[1])
                c.send("succes")

                return [clnt, temp]
            c.send("not_succes")


def handle(c, addr):  # understands what client and assigns command accordingly
    enc = connect_client(c)
    connection_login = sqlite3.connect("login.db")
    crsr = connection_login.cursor()
    arr = before_game(enc, crsr, connection_login)
    clnt = arr[0]
    temp = arr[1]
    pickle_something(clnt, enc)

    handle_game(connection_login, crsr, enc, addr, clnt)
    while True:
        if enc.recv() == "REF":

            clnt = login(crsr, temp.name, temp.paswd)
            pickle_something(clnt, enc)
            handle_game(connection_login, crsr, enc, addr, clnt)


def handleactive(connection, crsr, c, addr,
                 clnt):  # assigns an active client a personalized id,and closes connection when finished

    num = random.randint(100000, 999999)
    while num in ACTIVEREQ.values():
        num = random.randint(100000, 999999)
    lock.acquire()
    ACTIVEREQ[addr[0]] = num  # assigns the client a personalized number code and lists him as an active client
    lock.release()
    pack = hpack(ACTIVEREQ[addr[0]])
    lock.acquire()
    ACTIVEENC[addr[0]] = pack.fernet  # assigns the client a personalized encryption object
    lock.release()
    pickle_something(pack, c)
    # send_answer(c,str(()))#sends the active client his personalized password
    #  txt = all_mesage(c)
    try:
        get_quiz(crsr, c, clnt)#tries to find
    except:
        c.send("no")
        while True:
            try:
                get_quiz(crsr, c, clnt)
                break
            except:
                c.send("no")
    plyr_lst = c.recv(True)
    update(connection, crsr, plyr_lst)
    return



def findkey(val):
    key_list = list(ACTIVEREQ.keys())

    val_list = list(ACTIVEREQ.values())
    indx = val_list.index(int(val))

    key_list1 = list(ACTIVEENC.keys())

    val_list1 = list(ACTIVEENC.values())
    return key_list[indx], val_list1[indx]


def handlepasive(c):  # sends to the passive client the ip address of the active client with the desired number
    while True:
        param = c.recv()

        try:

            saddr, fernet = findkey(param)  # finds the corresponding ip for the num
            saddr = hpack(saddr, fernet)
            pickle_something(saddr, c)
            break

        except:
            saddr = "no"
            c.send(saddr)

def get_lists( crsr, c):
    crsr.execute('SELECT name FROM quizes  ',)
    names = crsr.fetchall()
    crsr.execute('SELECT `limit` FROM quizes ', )
    params = crsr.fetchall()
    list_names = []
    list_limit = []
    for i in names:
        list_names.append(i[0])
    for i in params:
        list_limit.append(i[0])
    pickle_something([list_names,list_limit],c)




def add_quiz(connection, crsr, quiz):
    crsr.execute('INSERT INTO quizes (name,"limit")  VALUES (?, ?);', (quiz.name, quiz.limit))
    crsr.execute('INSERT INTO q_and_a (content)  VALUES (?);', (quiz.file_cont,))
    connection.commit()


def handle_quiz(connection, crsr, enc, clnt):
    err = ""
    while True:
        if not err == "":
            quz = enc.recv(True)
        else:
            quz = enc.recv(True)
        if quz == b'home':
            break
        lim = quz.limit
        if not lim == "":

            try:
                lim1 = lim.split("_")
                if not lim1[0] in ["points", "num_firsts", "win_rate"]:
                    err = "limit not valid category"
                    raise
                if not clnt.comp_limit(lim):
                    err = "how can you limit when you arent able yo play...."
                    raise
                if not quiz_exists(quz,crsr):
                    err = "name already taken try again"
                    raise
                enc.send("succes")
                break
            except:
                enc.send(err)

    if quz == b'home':
        return
    add_quiz(connection, crsr, quz)


def quiz_exists(quz,crsr):
    crsr.execute('SELECT * FROM quizes WHERE  name = ? ', (quz.name,))
    data = crsr.fetchall()
    if data == []:
        return True
    return False


def handle_game(connection, crsr, c, addr, clnt):  # understands what client and assigns command accordingly
    txt = c.recv()
    if txt == "hello":
        handleactive(connection, crsr, c, addr, clnt)
    elif txt == "please":
        handlepasive(c)
    elif txt == "quiz":
        handle_quiz(connection, crsr, c, clnt)
    elif txt == "lists":
        get_lists( crsr, c)



def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, PORT))

    while True:
        s.listen()
        c, addr = s.accept()
        thread = threading.Thread(target=handle, args=(c, addr))
        thread.start()


if __name__ == '__main__':
    main()
