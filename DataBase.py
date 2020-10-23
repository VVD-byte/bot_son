import sqlite3
from sqlite3 import Error
import re

class DB:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('db')
        except Error:
            print(Error)
        self.cur = self.conn.cursor()

    def add_data(self):
        pass    