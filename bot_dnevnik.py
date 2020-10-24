# -*- coding: utf-8 -*-
from config import bot, keyboard1
import re
from DataBase import DB
from datetime import time

from user import users

db = DB()

user_dat = db.all_check_data()

@bot.message_handler(commands = ['start'])
def start(message):
    user_dat[message.chat.id] = users()
    bot.send_message(message.chat.id, 'Дневник чувств')
    bot.send_message(message.chat.id, 'Сколько сейчас времени там, где ты живешь? (Например 23:59)')

@bot.message_handler(func = lambda message: re.search(r'\d{1,2}:\d{1,2}-\d{1,2}:\d{1,2}', message.text))
def get_time_2(message):
    if user_dat[message.chat.id].get_data_2(message.text, message.chat.id):
        bot.send_message(message.chat.id, user_dat[message.chat.id].data_2_2)
        bot.send_message(message.chat.id, "С какой регулярностью мне выходить на связь? (Укажи каждые сколько часов)")
    else:
        bot.send_message(message.chat.id, 'Ты ввел некорректный формат времени')
        bot.send_message(message.chat.id, 'Примеры: 22:00-6:00, 23:00-7:00 ')


    if user_dat[message.chat.id].proof():
        db.add_data(user_dat[message.chat.id])

@bot.message_handler(func = lambda message: re.search(r'\d{1,2}:\d{1,2}', message.text))
def get_time_1(message):
    if user_dat[message.chat.id].get_data_1(message.text, message.chat.id):
        bot.send_message(message.chat.id, user_dat[message.chat.id].data_1)
        bot.send_message(message.chat.id, "Со скольки до скольки ты спишь, чтобы я тебя не беспокоил? (22:30-8:30)")
    else:
        bot.send_message(message.chat.id, 'Ты ввел некорректный формат времени')
        bot.send_message(message.chat.id, 'Примеры: 22:00, 6:00, 23:00, 7:00 ')


    if user_dat[message.chat.id].proof():
        db.add_data(user_dat[message.chat.id])

@bot.message_handler(func = lambda message: re.search(r'\d{1,2}', message.text))
def get_time_3(message):
    if user_dat[message.chat.id].get_data_3(message.text, message.chat.id):
        bot.send_message(message.chat.id, user_dat[message.chat.id].data_3)
        bot.send_message(message.chat.id, "Напиши мне, как будешь готов!", reply_markup = keyboard1)
    else:
        bot.send_message(message.chat.id, 'Ты ввел некорректный формат времени')
        bot.send_message(message.chat.id, 'Примеры: 22, 1, 6, 2, 24')

    if user_dat[message.chat.id].proof():
        db.add_data(user_dat[message.chat.id])

@bot.message_handler(regexp = "Настройка времени")
def rm(message):
    start(message)

@bot.message_handler()
def all(message):
    bot.send_message(message.chat.id, "Данная команда не найдена или вы ввели невенрое значение")
    try:
        bot.send_message(message.chat.id, f"{user_dat[message.chat.id]}")
    except:
        bot.send_message(message.chat.id, "ERROR")

def main():
    bot.infinity_polling(True)