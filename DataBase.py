import sqlite3
from sqlite3 import Error
from user import users
import json
import copy
import re

class DB:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('db', check_same_thread=False)
        except Error:
            print(Error)
        self.cur = self.conn.cursor()

    def add_data(self, dat):
        dat = self.pr(dat)
        self.cur.execute("SELECT * FROM users WHERE id=?", (dat.mess_id,))
        if len(self.cur.fetchall()) == 0:
            self.cur.execute("""INSERT INTO users(id, delta_time, start_time, end_time, chast, dat) VALUES(?, ?, ?, ?, ?, ?)""", (int(dat.mess_id), int(dat.data_1), dat.data_2_1, dat.data_2_2, int(dat.data_3), str(dat.vibor).replace("'", '"')))
            self.conn.commit()
        else:
            self.cur.execute("""UPDATE users SET delta_time=?, start_time=?, end_time=?, chast=?, dat=? where id=?""", (int(dat.data_1), dat.data_2_1, dat.data_2_2, int(dat.data_3), str(dat.vibor).replace("'", '"'), int(dat.mess_id)))
            self.conn.commit()

    def all_check_data(self):
        dat = {}
        self.cur.execute("SELECT * FROM users")
        for i in self.cur.fetchall():
            a = users()
            a.vibor, a.mess_id, a.data_1, a.data_2_1, a.data_2_2, a.data_3 = json.loads(i[5]), i[0], i[1], i[2], i[3], i[4]
            dat[i[0]] = a
        return dat

    def pr(self, dat):
        if dat.data_2_1 == '': dat.data_2_1 = '22:30'
        if dat.data_2_2 == '': dat.data_2_2 = '8:30'
        if dat.data_3 == '': dat.data_3 = 2
        return dat