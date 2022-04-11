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
        self.games =data[4]
        self.temp = None
        print(data)

    def update(self,indx):
        self.points = self.points + self.temp.value
        self.games = self.games+1
        if indx  == 0:
            self.num_firsts = self.num_firsts +1
        if indx<3:
                self.top_3_rate = (self.top_3_rate + 1)


    def to_string(self):
        return str(self.points) + "*" + str(self.num_firsts) + "*" + str(self.top_3_rate) + "*" + str(self.games)


