class Temp:
    def __init__(self, name, sock):
        self.name = name
        self.value = 0
        self.added_value = 0
        self.socket = sock

    def Get_name(self):
        return self.name

    def Get_value(self):
        return self.value

    def Get_socket(self):
        return self.socket

    def add_value(self, val):
        self.value += val

    def Set_added_value(self, add):
        self.added_value = add

    def strt_classes(self):
        self.socket.sock.settimeout(20)
        self.socket.send("STRT")

    def end_client(self):
        self.socket.send( "bye")

    def stop_client(self):
        self.socket.send( "STP")
    def send_eror(self):
        self.socket.send("ERR")

    def recv_ans(self):
        self.socket.sock.settimeout(20)
        ans = self.socket.recv()

        ans = ans.split("_")
        try:
            return ans[1], ans[2]
        except:
            return ans, ""

    def To_string(self):
        return self.name + ":" + str(self.value)


def all_mesage(sock):  # recievs all of the message based on the message length given at the begining of the messsage
    try:
        sock.settimeout(200000)
        lent = sock.recv(1).decode()
        while "_" not in lent:
            lent += sock.recv(1).decode()

        lent = lent[:-1]  # recives the message length
        ans = sock.recv(int(lent)).decode()

        while not len(ans) == int(lent):
            ans += sock.recv(lent)
    except:
        ans = "OOF"
    return ans  # recieves the message