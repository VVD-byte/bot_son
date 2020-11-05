# -*- coding: utf-8 -*-
from config import bot, keyboard1, keyboard2, keyboard3, keyboard4, keyboard5, token
import re
from DataBase import DB
import json
import threading
import schedule
import time as ti
from datetime import datetime, timedelta, date
import xlrd
import requests
import random
import os
import logging

from user import users

logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def e(func):
    def wop(message):
        try:
            logging.info(message.text)
            func(message)
        except:
            logging.info("ERROR")
            del user_dat[message.chat.id].vibor[-1]
            all(message)

    return wop

wb = xlrd.open_workbook('./cit.xlsx')
ws = wb.sheet_by_index(0)
row = [] # The row where we stock the name of the column
for col in range(ws.nrows):
    row.append(ws.cell_value(col, 0))

now = ''

def n():
    try:
        global now
        now = random.choice(row)
        os.mkdir('./audio/%s' % datetime.today().date())

    except:pass

schedule.every().day.at('00:00').do(n)

with open('text.json') as t:
    text = json.loads(t.read())

@bot.message_handler(regexp = 'Главное меню')
def g_m(message):
    bot.send_message(message.chat.id, 'Главное меню', reply_markup = keyboard1)

@bot.message_handler(commands=['stat'])
def statist(message):
    if message.chat.id == 20419906 or message.chat.id == 271411622:
        bot.send_message(message.chat.id, 'Статистика', reply_markup = keyboard5)
    else:
        all(message)

@bot.message_handler(regexp = 'Статистика по системе')
def stat_all(message):
    s = ''
    if message.chat.id == 20419906 or message.chat.id == 271411622:
        d = db.stat_all()
        s += 'Количество пользователей: ' + str(d[0]) + '\n'
        s += 'Количество акьтвных пользователей: ' + str(d[1]) + '\n'
        bot.send_message(message.chat.id, s, reply_markup=keyboard5)
    else:
        all(message)

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id in user_dat.keys():
        user_dat[message.chat.id].reset()
    else:
        user_dat[message.chat.id] = users()
    bot.send_message(message.chat.id, 'Дневник чувств')
    bot.send_message(message.chat.id, 'Сколько сейчас времени там, где ты живешь? (Например 23:59)')


@bot.message_handler(func=lambda message: re.search(r'\d{1,2}:\d{1,2}-\d{1,2}:\d{1,2}', message.text))
def get_time_2(message):
    if not user_dat[message.chat.id].proof():
        if user_dat[message.chat.id].get_data_2(message.text, message.chat.id):
            bot.send_message(message.chat.id,
                             "С какой регулярностью мне выходить на связь? (Укажи каждые сколько часов)")
        else:
            bot.send_message(message.chat.id, 'Ты ввел некорректный формат времени')
            bot.send_message(message.chat.id, 'Примеры: 22:00-6:00, 23:00-7:00 ')

        if user_dat[message.chat.id].proof():
            db.add_data(user_dat[message.chat.id])
    else:
        all(message)


@bot.message_handler(func=lambda message: re.search(r'\d{1,2}:\d{1,2}', message.text))
def get_time_1(message):
    if not user_dat[message.chat.id].proof():
        if user_dat[message.chat.id].get_data_1(message.text, message.chat.id):
            bot.send_message(message.chat.id, "Со скольки до скольки ты спишь, чтобы я тебя не беспокоил? (22:30-8:30)")
        else:
            bot.send_message(message.chat.id, 'Ты ввел некорректный формат времени')
            bot.send_message(message.chat.id, 'Примеры: 22:00, 6:00, 23:00, 7:00 ')

        if user_dat[message.chat.id].proof():
            db.add_data(user_dat[message.chat.id])
    else:
        all(message)


@bot.message_handler(func=lambda message: re.search(r'\d{1,2}', message.text))
def get_time_3(message):
    if not user_dat[message.chat.id].proof():
        if user_dat[message.chat.id].get_data_3(message.text, message.chat.id):
            bot.send_message(message.chat.id, "Напиши мне, как будешь готов!", reply_markup=keyboard1)
        else:
            bot.send_message(message.chat.id, 'Ты ввел некорректный формат времени')
            bot.send_message(message.chat.id, 'Примеры: 22, 1, 6, 2, 24')

        if user_dat[message.chat.id].proof():
            db.add_data(user_dat[message.chat.id])
    else:
        all(message)


@bot.message_handler(regexp="Настройка времени")
def rm(message):
    start(message)


@bot.message_handler(regexp="Новая запись")
def new(message):
    logging.info(message.text)
    schedule.clear(message.chat.id)
    user_dat[message.chat.id].vibor.append([])
    user_dat[message.chat.id].vibor[-1].append(datetime.strftime(datetime.today().date(), "%d:%m:%Y"))
    send = bot.send_message(message.chat.id,
                            'Какую эмоцию ты сейчас чувствуешь?\n\n1. Гнев\n2. Страх\n3. Грусть\n4. Радость\n5. Любовь')
    bot.register_next_step_handler(send, test)


@e
def test(message):
    user_dat[message.chat.id].vibor[-1].append(message.text)
    send = bot.send_message(message.chat.id, text[message.text][1])
    bot.register_next_step_handler(send, test_1)


@e
def test_1(message):
    user_dat[message.chat.id].vibor[-1].append(text[user_dat[message.chat.id].vibor[-1][1]][2][message.text])
    send = bot.send_message(message.chat.id, 'В привязке к какому человеку, предмету или событию ты это чувствуешь?')
    bot.register_next_step_handler(send, test_2)


@e
def test_2(message):
    user_dat[message.chat.id].vibor[-1].append(message.text)
    send = bot.send_message(message.chat.id, 'Как ты ощущаешь это в теле? (Например: Комок в горле)')
    bot.register_next_step_handler(send, test_3)


@e
def test_3(message):
    user_dat[message.chat.id].vibor[-1].append(message.text)
    send = bot.send_message(message.chat.id,
                            'На сколько сильное переживание ты сейчас испытываешь по десятибалльной шкале? (1-10)')
    bot.register_next_step_handler(send, test_4)


@e
def test_4(message):
    user_dat[message.chat.id].vibor[-1].append(int(message.text))
    user_dat[message.chat.id].vibor_week.append(user_dat[message.chat.id].vibor[-1])
    db.add_data(user_dat[message.chat.id])
    bot.send_message(message.chat.id,
                     f'Спасибо, я все записал. Напиши мне  как только состояние изменится или я напомню о себе через {user_dat[message.chat.id].data_3} ч.')
    schedule.every().day.at(delt_time(time(message.chat.id), message.chat.id)).tag(message.chat.id).do(lambda: opr(message.chat.id))

@bot.message_handler()
def all(message):
    print(message.chat.id)
    bot.send_message(message.chat.id, "Данная команда не найдена или вы ввели невенрое значение", reply_markup = keyboard1)

def opr(id):
    if datetime.now().time() < datetime.strptime(user_dat[id].data_2_1, "%H:%M").time() and datetime.now().time() > datetime.strptime(user_dat[id].data_2_2, "%H:%M").time():
        bot.send_message(id, "Привет, не хочешь поделиться чувствами?")
        schedule.every().day.at(delt_time(time(id), id)).tag(id).do(lambda: opr(id))
    else:
        schedule.every().day.at(delt_time((datetime.strptime(user_dat[id].data_2_2, "%H:%M") + timedelta(hours=1)).time().strftime("%H:%M"), id)).tag(id).do(lambda: opr(id))

###уведомление через Х часов
def time(id):
    return (datetime.now() + timedelta(hours=user_dat[id].data_3)).strftime("%H:%M")

###рассчет разницы времени
def delt_time(time_, id, t = ''):
    if t == '': t = user_dat[id].data_1
    if type(time_) == str:
        return (datetime.combine(date.today(), datetime.strptime(time_, "%H:%M").time()) + timedelta(hours=t)).strftime("%H:%M")
    else:
        return (datetime.combine(date.today(), time_) + timedelta(hours=t)).strftime("%H:%M")

def add_sched():
    while True:
        schedule.run_pending()
        ti.sleep(1)


def main():
    n()
    x = threading.Thread(target=add_sched)
    x.start()
    bot.infinity_polling(True)

###########################################################
def cit(id):
    bot.send_message(id, now)
    send = bot.send_message(id, "Прочитай, пожалуйста  цитату и запиши анонимное аудио сообщение со своими мыслями по этому опыту, поделись своим опытом", reply_markup = keyboard2)
    bot.register_next_step_handler(send, vol)

def vol(message):
    if message.content_type == 'voice':
        download_audio(message)
        send = bot.send_message(message.chat.id, 'Мы сохранили вашу запись\nСпасибо, что поделились\nХотите послушать мысли других людей?', reply_markup = keyboard3)
    else:
        send = bot.send_message(message.chat.id, 'Хотите послушать мысли других людей?', reply_markup = keyboard3)
    bot.register_next_step_handler(send, end)

def end(message):
    if message.text == 'Да, хочу' or message.text == 'Послушать еще':
        _ret_audio(message)
    else:
        bot.send_message(message.chat.id, 'Хорошо, в следующий раз', reply_markup = keyboard1)

def download_audio(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))

    with open('./audio/%s/%s_%s.ogg' %(datetime.today().date(), message.chat.id, datetime.now()), 'wb') as f:
        f.write(file.content)

def _ret_audio(message):
    path = "./audio/%s" % datetime.today().date()
    audio = open(path + '/' + random.choice(os.listdir(path)), 'rb')
    send = bot.send_audio(message.chat.id, audio, reply_markup = keyboard4)
    audio.close()
    bot.send_message(message.chat.id, 'Оцените васказываение от 1 до 10')
    bot.register_next_step_handler(send, end)

#################################
def stat(all = 0, id = 0):
    if all == 0:
        s = otch(user_dat[id].vibor, 1)
    else:
        s = otch(user_dat[id].vibor_week, 0)
    bot.send_message(id, s)

def otch(us, q):
    s = ''
    a = []
    for j, i in enumerate(us):
        s += f"{j + 1}. - {i[0]}, {text[i[1]][0]}, {i[2]}, {i[3]}, {i[4]}, {i[5]}\n"
    for i in us:
        if text[i[1]][0] not in a:
            a.append(text[i[1]][0])
    s += f"Сегодня ты контактировал со следующими сувствами: {', '.join(a)}"
    a = []
    for i in us:
        if i[2] not in a:
            a.append(i[2])
    s += f"Сегодня ты контактировал со следующими сувствами: {', '.join(a)}"
    us.sort(key=lambda i: i[-1])
    us.reverse()
    if q == 1: s += "Топ 5 переживаний/эмоций за этот день:\n  "
    else: s += "Топ 5 переживаний/эмоций за эту неделю:\n  "
    for i in us:
        if len(us) < 5:
            s += f"{j + 1}. - {i[0]}, {text[i[1]][0]}, {i[2]}, {i[3]}, {i[4]}, {i[5]}\n"

    us = []
    return s

db = DB(cit, stat, delt_time)

user_dat = db.all_check_data()