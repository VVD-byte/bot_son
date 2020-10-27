# -*- coding: utf-8 -*-
from telebot import TeleBot, types

token = '1331692452:AAFsKuuxkPs2rKZe7A88ivRiqqQkXjZLh6M'
bot = TeleBot(token)

keyboard1 = types.ReplyKeyboardMarkup()
keyboard1.row('Новая запись')
#keyboard1.row('test')
keyboard1.row('Настройка времени')

keyboard2 = types.ReplyKeyboardMarkup()
keyboard2.row('В другой раз')

keyboard3 = types.ReplyKeyboardMarkup()
keyboard3.row('Да, хочу')
keyboard3.row('В другой раз')