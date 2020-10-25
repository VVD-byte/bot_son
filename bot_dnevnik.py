# -*- coding: utf-8 -*-
from config import bot, keyboard1
import re
from DataBase import DB
import json
from datetime import time

from user import users

def e(func):
    def wop(message):
        try:
            func(message)
        except:
            del user_dat[message.chat.id].vibor[-1]
            all(message)
    return wop
with open('text.json') as t:
    text = json.loads(t.read())

db = DB()

user_dat = db.all_check_data()

@bot.message_handler(commands = ['start'])
def start(message):
    if message.chat.id in user_dat.keys():
        user_dat[message.chat.id].reset()
    else: user_dat[message.chat.id] = users()
    bot.send_message(message.chat.id, 'Дневник чувств')
    bot.send_message(message.chat.id, 'Сколько сейчас времени там, где ты живешь? (Например 23:59)')

@bot.message_handler(func = lambda message: re.search(r'\d{1,2}:\d{1,2}-\d{1,2}:\d{1,2}', message.text))
def get_time_2(message):
    if not user_dat[message.chat.id].proof():
        if user_dat[message.chat.id].get_data_2(message.text, message.chat.id):
            bot.send_message(message.chat.id, "С какой регулярностью мне выходить на связь? (Укажи каждые сколько часов)")
        else:
            bot.send_message(message.chat.id, 'Ты ввел некорректный формат времени')
            bot.send_message(message.chat.id, 'Примеры: 22:00-6:00, 23:00-7:00 ')

        if user_dat[message.chat.id].proof():
            db.add_data(user_dat[message.chat.id])
    else:
        all(message)

@bot.message_handler(func = lambda message: re.search(r'\d{1,2}:\d{1,2}', message.text))
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

@bot.message_handler(func = lambda message: re.search(r'\d{1,2}', message.text))
def get_time_3(message):
    if not user_dat[message.chat.id].proof():
        if user_dat[message.chat.id].get_data_3(message.text, message.chat.id):
            bot.send_message(message.chat.id, "Напиши мне, как будешь готов!", reply_markup = keyboard1)
        else:
            bot.send_message(message.chat.id, 'Ты ввел некорректный формат времени')
            bot.send_message(message.chat.id, 'Примеры: 22, 1, 6, 2, 24')

        if user_dat[message.chat.id].proof():
            db.add_data(user_dat[message.chat.id])
    else:
        all(message)

@bot.message_handler(regexp = "Настройка времени")
def rm(message):
    start(message)

@bot.message_handler(regexp = "Новая запись")
def new(message):
    user_dat[message.chat.id].vibor.append([])
    send = bot.send_message(message.chat.id, 'Какую эмоцию ты сейчас чувствуешь?\n\n1. Гнев\n2. Страх\n3. Грусть\n4. Радость\n5. Любовь')
    bot.register_next_step_handler(send, test)

@e
def test(message):
    user_dat[message.chat.id].vibor[-1].append(message.text)
    send = bot.send_message(message.chat.id, text[message.text][1])
    bot.register_next_step_handler(send, test_1)

@e
def test_1(message):
    user_dat[message.chat.id].vibor[-1].append(text[user_dat[message.chat.id].vibor[-1][0]][2][message.text])
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
    send = bot.send_message(message.chat.id, 'На сколько сильное переживание ты сейчас испытываешь по десятибалльной шкале? (1-10)')
    bot.register_next_step_handler(send, test_4)

@e
def test_4(message):
    user_dat[message.chat.id].vibor[-1].append(int(message.text))
    db.add_data(user_dat[message.chat.id])
    bot.send_message(message.chat.id, 'Спасибо, я все записал. Напиши мне  как только состояние изменится или я напомню о себе через 2 ч.')

@bot.message_handler()
def all(message):
    bot.send_message(message.chat.id, "Данная команда не найдена или вы ввели невенрое значение")

def main():
    bot.infinity_polling(True)