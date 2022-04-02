import sqlite3
class player:
    def __init__(self,crsr,name):
        self.name = name
        crsr.execute('SELECT * FROM login_info WHERE username = ? ', (name,))
        data = crsr.fetchall()
        data = data[0]
        self.index = data[2]
        print(self.index)
        crsr.execute('SELECT * FROM clients_info WHERE `index` = ?',(self.index,))
        data = crsr.fetchall()
        data = data[0]
        self.points = data[1]
        self.num_firsts = data[2]
        self.top_3_rate = data[3]
        print(data)

