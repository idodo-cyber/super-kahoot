import threading
import pickle
from datetime import datetime
from encrypt import *
from game_screen_gamer import *
import socket
class gamer:
    def __init__(self,enc,root,geometry,home_screen):
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
        self.PLAYER_NUM = 3
    def get_addr(self,var):
        if var == 0:
            gmr = gmr_screens(self.root,self.geometry,self.home_screen)
        else:
            CRNT_FRM, ans = opening2(root)
        while True:
            if not gmr.pin == 0:
                break
        print(gmr.pin)
        self.src_enc.send("please")
        self.src_enc.send(gmr.pin)
        pack= self.src_enc.recv(True)
        self.Haddres= pack.pin
        self.src_enc.game_fernet = pack.fernet
        self.gmr = gmr
    def send_answer1(self,ans):
        self.src_sock.send((str(len(ans)) + "_" + ans).encode())
    def cnct_client(self,clnt):
        self.Hsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = clnt
        self.Hsock.connect((self.Haddres, self.MPORT))
        self.henc = game_crypt(self.Hsock, self.src_enc.game_fernet)
        self.pickle_something(self.client)
        if self.henc.recv() == "good":
            self.gmr.waiting()
    def play_game(self):
        ans = ""
        while not ans == "STP":
            ans = self.henc.recv()
            if ans == "STRT":
                self.STRT_TIME = datetime.now()
                self.gmr.answer_screen()
                while True:
                    end_time = datetime.now()
                    time_diff = (end_time - self.STRT_TIME)
                    execution_time = time_diff.total_seconds() * 1000
                    if self.gmr.pressed_click:
                        self.gmr.pressed_click = False
                        answer = self.build_ans(self.gmr.choice)
                        #print(answer)
                        self.henc.send(answer)
                        break
                    elif execution_time > 20000:
                        break
                self.gmr.waiting()
                point = self.henc.recv().split("_")
                self.gmr.reset()
                print(point)
                self.gmr.between(point)
        print("congrats u finished game")
        self.gmr.resety()
        self.gmr.ending(point)
        self.henc.recv()
        print("help please")




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
            print(ans)
        return ans



    def pickle_something(self,somth):
        msg = pickle.dumps(somth)
        self.henc.send(msg)

    def send_answer(self, ans):
        self.henc.send(ans)

    def build_answer(self,ans):  # builds apropriate answer according to protocol
        return str(len(ans)) + "_" + ans

    def build_ans(self,ans):
        start_time = self.STRT_TIME
        end_time = datetime.now()
        time_diff = (end_time - start_time)
        execution_time = time_diff.total_seconds() * 1000
        exe = int(execution_time)
        print(exe)
        ans = self.build_answer(ans + "_" + str(exe))  # builds the answer based on protocol len_ans_time
        return ans




