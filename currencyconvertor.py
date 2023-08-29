import telebot
from telebot import types
from  currency_converter import CurrencyConverter
import requests
import json

bot = telebot.TeleBot('5946840389:AAEnVJNVMBewWVCYqokFkWE1pOXU8disKfw')

currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, введите сумму')
    bot.register_next_step_handler(message, summa)
def summa(message):
    global amount
    try:
        amount = int(message.text.strip()) 
    except ValueError:
        bot.send_message(message.chat.id, 'Type errror,Ведите верную сумму')
        bot.register_next_step_handler(message, summa)      
        return
    if amount>1:        
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GPB', callback_data='usd/gpb')
        btn4 = types.InlineKeyboardButton('other', callback_data='else')
        markup.add(btn1,btn2,btn3, btn4)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)

    else :
        bot.send_message(message.chat.id, 'Число должно быть больше 0 ,Ведите верную сумму')
        bot.register_next_step_handler(message, summa)      
        return

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    values = call.data.upper().split('/')
    res = currency.convert(amount, values[0],values[1])
    bot.send_message(call.message.chat.id, f'Получается {round(res, 2)}, можете введит другую сумму ')
    bot.register_next_step_handler(call.message, summa)
    


bot.polling(non_stop=True)    
