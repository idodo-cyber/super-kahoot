from Temporery import *
import socket
import threading
import pickle
from game_screen_host import *
from quiz_choice import *
from encrypt import *
class host:
    def __init__(self,enc,root,geometry,home_screen):
        self.lock = threading.Lock()
        self.home_screen = home_screen
        self.root = root
        self.geometry = geometry
        self.src_enc = enc
        self.SPORT = 55368
        self.MPORT = 53476
        self.PROG1 = 0
        self.CHOICE = 0
        self.IP = "0.0.0.0"
        self.CLINET_ARR = []
        self.lock = threading.Lock()
        self.ANS_WORTH = 100
        self.ANS_TIME = 60000
        self.CNCT = 0
        self.PROG = 0
        self.QUESTNUM = 5
        self.STAT = 0
        self.PLAYER_NUM = 2
        self.get_pin()  # gets pin






    def get_pin(self):  # recieves game pin from server
        self.src_enc.send(("hello").encode())
        msg = self.src_enc.recv(True)
        self.pin = msg.pin
        self.src_enc.game_fernet = msg.fernet

    def handle_quiz_choice(self):
        chs = choice(self.root, self.geometry,self.home_screen)
        while True:
            while True:
                if chs.pressed:
                    chs.pressed = False
                    break
            self.src_enc.send(chs.name)
            content = self.src_enc.recv()
            if not content == "no":
                # Reading from file
                with open("demo_quiz", "w") as file1:
                    # Writing data to a file
                    file1.write(content)
                    self.PLAYER_NUM = int(chs.num)
                    break
            else:
                chs.not_good()



    def handle_lobby(self):
        self.lobby = hst_screens(self.root, self.geometry,self.pin,self.home_screen)
        self.Mscok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Mscok.bind((self.IP, self.MPORT))
        var = 0
        arr = []  # creates an array for the threads for each client
        while var < self.PLAYER_NUM:  # two clients needs to change to infinit aith timeouts
            self.Mscok.listen()
            c, addr = self.Mscok.accept()
            c = game_crypt(c,self.src_enc.game_fernet)
            thread = threading.Thread(target=self.connect_client, args=(c, self.root, self.pin))  # creates new thread for client
            thread.start()
            arr.append(thread)
            var += 1
        for i in arr:
            i.join()  # waits until all clients are connected an set
        while True:
            if self.lobby.cont:
                break




    def send_to_player(self,plyr,msg):
        plyr.temp.socket.send(msg)

    def pickle_something(self, somth):
        msg = pickle.dumps(somth)
        #self.src_sock.send(str(len(msg)).encode())
        self.src_enc.send(msg)


    def build_answer(self,ans):  # builds apropriate answer according to protocol
        return str(len(ans)) + "_" + ans

    def send_bytes(self, what):
        self.send_answer(str(len(what)))
        self.src_sock.send(what)

    def send_answer(self, ans):
        self.src_sock.send((self.build_answer(ans)).encode('utf-8').strip())


    def connect_client(self,c, root, pin):  # connects client and sets him up with the clients nickname
        global CRNT_FRM
        clnt = c.recv(pickled=True)
        clnt.temp = Temp(clnt.name, c)
        self.lock.acquire()
        self.CLINET_ARR.append(clnt)
        self.lock.release()
        c.send("good")

        self.lobby.update_lobby(self.CLINET_ARR,self.PLAYER_NUM)
        #reset(CRNT_FRM)
        #CRNT_FRM = opening2(root, pin)
        #lock.release()

    def handle_quiz(self):
        global CRNT_FRM
        global PROG
        global PLAYER_NUM
        with open("demo_quiz") as file:
            first_lines = "".join([file.readline() for _ in range(5)]).split("\n")
            num = 1
            quest = first_lines[0]
            arr1 = self.split_lines(first_lines[1:])
            self.lobby.reset()
            self.lobby.question( num, quest, arr1)

            while not "@_end_@" in first_lines:
                for i in first_lines:
                    if "_T" in i:
                        ans = i.split("_")
                        arr = []
                        for cli in self.CLINET_ARR:
                            thread = threading.Thread(target=self.handle_ans,
                                                      args=(ans[1], cli.temp))  # creates new thread for client
                            thread.start()
                            arr.append(thread)
                        for thr in arr:
                            thr.join()  # waits until all clients are finished
                        self.CLINET_ARR.sort(key=lambda x: x.temp.value, reverse=True)  # sorts the clients based on their value
                        for i in self.CLINET_ARR:
                            try:
                                voop = str(i.temp.value)+ "_" + str(i.temp.added_value) + "_" + str(self.CLINET_ARR.index(i) + 1)

                                self.send_to_player(i,self.build_answer(voop))
                                    # sends the value,added value and place of client to client to the client
                            except:
                                self.PLAYER_NUM = self.PLAYER_NUM - 1
                                self.CLINET_ARR.remove(i)
                                if self.PLAYER_NUM == 0:
                                    raise

                self.lobby.reset()
                self.lobby.answer(ans[1],self.CLINET_ARR)
                while True:
                    if self.lobby.quest_button == True:
                        self.lobby.quest_button = False
                        break
                first_lines = "".join([file.readline() for _ in range(5)]).split("\n")

                if not "@_end_@" in first_lines:
                    num += 1
                    quest = first_lines[0]
                    arr1 = self.split_lines(first_lines[1:])
                    self.lobby.resety()
                    CRNT_FRM = self.lobby.question( num, quest, arr1)



    def end_client(self,ERR = False):
        for i in self.CLINET_ARR:
            i.temp.stop_client()
        self.lobby.resety()
        self.lobby.ending(self.CLINET_ARR)
        while True:
            if self.lobby.quest_button:
                self.lobby.quest_button = False
                for i in self.CLINET_ARR:
                    if not ERR:
                        i.temp.end_client()
                        i.temp.socket.sock.close()
                    else:
                        i.temp.send_eror()
                        i.temp.socket.sock.close()
                break



    def split_lines(self,frst):
        arr = []
        l = 0
        for i in frst:
            var = i.split("_")
            arr.append(var[0])
            l += 1
        return arr

    def send_clients(self):
        self.dict_clients()
        self.pickle_something(self.out_dict)




    def dict_clients(self):
        self.out_dict = {}
        n=0
        for i in self.CLINET_ARR:

            i.update(n)

            self.out_dict[i.name] = i.to_string()
            n=n+1








    def handle_ans(self,true, cli):  # handles the given ans and adds points accordingly
        global lock
        global PLAYER_NUM
        try:
            cli.strt_classes()  # sends start message to client
            ans,time = cli.recv_ans()

            # recieves answer and time it tokk to answer from client
            if ans == true:  # if answer is correct adds the corresponding value
                val = 1 - (int(time) / self.ANS_TIME / 2)
                val = int(val * self.ANS_WORTH)
            else:
                val = 0
            cli.add_value(val)
            cli.Set_added_value(val)
        except:
            cli.add_value(0)
            cli.Set_added_value(0)

    def all_mesage(self,sock,bytes=False):  # recievs all of the message based on the message length given at the begining of the messsage
        lent = sock.recv(1).decode()
        while "_" not in lent:
            lent += sock.recv(1).decode()
        lent = int(lent[:-1])  # recives the message length
        ans = sock.recv(lent).decode()
        while not len(ans) == lent:
            ans += sock.recv(lent)
        if bytes:
            lens = int(ans)
            ans = sock.recv(4096)
            while not len(ans) == lens:
                ans += sock.recv(4096)

            ans = pickle.loads(ans)


        return ans  # recieves the message
    def build_answer(self,ans):  # builds apropriate answer according to protocol
        return str(len(ans)) + "_" + ans