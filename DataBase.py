import sqlite3
from sqlite3 import Error
from user import users
import json
import schedule
from datetime import date, timedelta, datetime
import copy
import re

class DB:
    def __init__(self, cit, stat, delt_time):
        self.cit = cit
        self.stat = stat
        self.delt_time = delt_time
        try:
            self.conn = sqlite3.connect('db', check_same_thread=False)
        except Error:
            print(Error)
        self.cur = self.conn.cursor()

    def get_user_data(self, id):
        self.cur.execute("""SELECT * FROM users WHERE id=?""", (id,))
        return [i for i in self.cur.fetchall()]

    def add_data(self, dat):
        dat = self.pr(dat)
        self.cur.execute("SELECT * FROM users WHERE id=?", (dat.mess_id,))
        if len(self.cur.fetchall()) == 0:
            self.cur.execute("""INSERT INTO users(id, delta_time, start_time, end_time, chast, dat, dat_week) VALUES(?, ?, ?, ?, ?, ?, ?)""", (int(dat.mess_id), int(dat.data_1), dat.data_2_1, dat.data_2_2, int(dat.data_3), str(dat.vibor).replace("'", '"'), str(dat.vibor_week).replace("'", '"')))
            self.conn.commit()
        else:
            self.cur.execute("""UPDATE users SET delta_time=?, start_time=?, end_time=?, chast=?, dat=?, dat_week=? where id=?""", (int(dat.data_1), dat.data_2_1, dat.data_2_2, int(dat.data_3), str(dat.vibor).replace("'", '"'), str(dat.vibor_week).replace("'", '"'), int(dat.mess_id)))
            self.conn.commit()
        schedule.every().day.at(self.delt_time(dat.data_2_2, dat.mess_id, dat.data_1)).tag(dat.mess_id * 10000).do(lambda: self.cit(dat.mess_id))
        schedule.every().day.at(self.time_fiw(self.delt_time(dat.data_2_2, dat.mess_id, dat.data_1))).tag(dat.mess_id * 10000).do(lambda: self.stat(dat.mess_id))
        schedule.every().sunday.at(self.time_fiw(self.delt_time(dat.data_2_2, dat.mess_id, dat.data_1))).tag(dat.mess_id * 10000).do(lambda: self.stat(1, dat.mess_id))

    def all_check_data(self):
        dat = {}
        self.cur.execute("SELECT * FROM users")
        for i in self.cur.fetchall():
            schedule.every().day.at(self.delt_time(i[3], i[0], i[1])).tag(i[0] * 10000).do(lambda: self.cit(i[0]))
            schedule.every().day.at(self.time_fiw(self.delt_time(i[3], i[0], i[1]))).tag(i[0] * 10000).do(lambda: self.stat(i[0]))
            schedule.every().sunday.at(self.time_fiw(self.delt_time(i[3], i[0], i[1]))).tag(i[0] * 10000).do(lambda: self.stat(1, i[0]))
            a = users()
            a.vibor, a.vibor_week, a.mess_id, a.data_1, a.data_2_1, a.data_2_2, a.data_3 = json.loads(i[5]), json.loads(i[6]), i[0], i[1], i[2], i[3], i[4]
            dat[i[0]] = a
        return dat

    def time_fiw(self, t):
        return datetime.strftime((datetime.strptime(t, "%H:%M") + timedelta(minutes = 5)), "%H:%M")

    def pr(self, dat):
        if dat.data_2_1 == '': dat.data_2_1 = '22:30'
        if dat.data_2_2 == '': dat.data_2_2 = '08:30'
        if dat.data_3 == '': dat.data_3 = 2
        return dat

    def stat_all(self):
        dat = []
        self.cur.execute('select count(*) from users;')
        dat.append(self.cur.fetchall()[0][0])
        self.cur.execute("select count(*) from users where dat_week<>'[]';")
        dat.append(self.cur.fetchall()[0][0])
        return dat