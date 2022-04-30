import rsa

from cryptography.fernet import Fernet
import pickle

class crypt:
    def __init__(self,c):
        self.publicKey, self.privateKey = rsa.newkeys(512)
        self.sock = c
    def create_aes_client(self):
        self.aes_key = Fernet.generate_key()
        self.fernet = Fernet(self.aes_key)
    def encrypt_message(self,message):
        try:
            return self.fernet.encrypt(message.encode())
        except:
            return self.fernet.encrypt(message)
    def decrypt_message(self,message):
        return self.fernet.decrypt(message)
    def encrypt_rsa(self,message):
       return rsa.encrypt(message.encode(),self.publicKey)
    def decrypt_rsa(self,message):
        return rsa.decrypt(message, self.privateKey).decode()
    def encrypt_rsa_client(self,message,pubkey):
       try:
        return rsa.encrypt(message.encode(),pubkey)
       except:
           return rsa.encrypt(message, pubkey)

    def create_aes_server(self,message):
        self.aes_key = self.decrypt_rsa(message)
        self.fernet = Fernet(self.aes_key)
    def send(self,message):
        message = self.encrypt_message(message)
        leng = len(message)
        self.sock.send((str(leng) + "_").encode() + message)

    def recv(self,pickled=False):  # recievs all of the message based on the message length given at the begining of the messsage
        print("3")
        lent = self.sock.recv(1)
        print("4")
        print(lent)
        print(lent.decode())
        while "_".encode() not in lent:
            lent += self.sock.recv(1)
        lent = int(lent[:-1])  # recives the message length
        print(lent)
        ans = self.sock.recv(lent)
        while not len(ans) == lent:
            ans += self.sock.recv(lent)
        print(ans)
        while True:
            if pickled:
                #try:
                    msg =  self.decrypt_message(ans)
                    msg = pickle.loads(msg)
                    return msg
                #except:
                    pickled = False
            else:
                ans = self.decrypt_message(ans).decode()
                break
        return ans  # recieves the message






class game_crypt(crypt):
    def __init__(self, c, fernet):
        #super().__init__(c)
        self.fernet = fernet
        self.sock = c

