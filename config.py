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

keyboard4 = types.ReplyKeyboardMarkup()
keyboard4.row('Послушать еще')
keyboard4.row('Спасибо, в другой раз')

keyboard5 = types.ReplyKeyboardMarkup()
keyboard5.row('Статистика по системе')
keyboard5.row('Общая статистика по всем юзерам')
keyboard5.row('Статистика по одному пользователю')
keyboard5.row('Статистика по единицам измерений')
keyboard5.row('Главное меню')