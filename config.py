# -*- coding: utf-8 -*-
from telebot import TeleBot, types

bot = TeleBot('1331692452:AAFsKuuxkPs2rKZe7A88ivRiqqQkXjZLh6M')

keyboard1 = types.ReplyKeyboardMarkup()
keyboard1.row('Новая запись')
keyboard1.row('Настройка времени')
keyboard1.row('Настройка времени сна')
keyboard1.row('Настройка интервала уведомлений')