import pickle
import rsa

from cryptography.fernet import Fernet
import pickle

class hpack:
    def __init__(self,pin,fernet = None):
        if fernet == None:
            self.aes_key = Fernet.generate_key()
            self.fernet = Fernet(self.aes_key)

        else:
            self.fernet = fernet
        self.pin = pin
