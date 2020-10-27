import re
import functools
import datetime

def fun(func):
    @functools.wraps(func)
    def proof(*args, **kwargs):
        try:
            func(*args, **kwargs)
            return True
        except:
            return False
    return proof

class users:
    def __init__(self):
        self.mess_id = 0
        self.data_1 = ''
        self.data_2_1 = ''
        self.data_2_2 = ''
        self.data_3 = ''
        self.vibor = []

    '''def __repr__(self):
        return f"{self.data_1} {self.data_2} {self.data_3}"'''
    def reset(self):
        self.data_1 = ''
        self.data_2_1 = ''
        self.data_2_2 = ''
        self.data_3 = ''
    @fun
    def get_data_1(self, dat, id):
        self.mess_id = id
        a = datetime.datetime.strptime(re.findall(r'\d{1,2}:\d{1,2}', dat)[0], '%H:%M').time()
        TimeA = datetime.datetime.combine(datetime.date.today(), a)
        self.data_1 = round((TimeA - datetime.datetime.now()).total_seconds() / 3600)

    @fun
    def get_data_2(self, dat, id):
        self.mess_id = id
        self.data_2_1, self.data_2_2 = self.f_t(re.findall(r'\d{1,2}:\d{1,2}', dat)[0]), self.f_t(re.findall(r'\d{1,2}:\d{1,2}', dat)[1])

    @fun
    def get_data_3(self, dat, id):
        self.mess_id = id
        self.data_3 = int(re.findall(r'\d{1,2}', dat)[0])

    def f_t(self, t):
        b = datetime.datetime.strptime(t, '%H:%M')
        return b.strftime('%H:%M')

    def proof(self):
        if self.data_1 != '' and self.data_2_1 != '' and self.data_3 != '':
            return True
        else: return False