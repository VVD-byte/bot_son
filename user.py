import re
import functools

def fun(func):
    @functools.wraps(func)
    def proof(self, *args, **kwargs):
        try:
            func(self, dat = args[0])
            return True
        except:
            return False
    return proof

class users:
    def __init__(self):
        self.data_1 = ''
        self.data_2 = ''
        self.data_3 = ''

    def __repr__(self):
        return f"{self.data_1} {self.data_2} {self.data_3}"

    @fun
    def get_data_1(self, dat):
        self.data_1 = re.findall(r'\d\d:\d\d', dat)[0]

    @fun
    def get_data_2(self, dat):
        self.data_2 = re.findall(r'\d\d:\d\d-\d\d:\d\d', dat)[0]

    @fun
    def get_data_3(self, dat):
        self.data_3 = re.findall(r'\d{1,2}', dat)[0]

    def proof(self):
        if self.data_1 != '' and self.data_2 != '' and self.data_3 != '':
            return True
        else: return False