import telebot
from telebot import types
import requests
import json

bot = telebot.TeleBot('6082306595:AAFPj4Gugc-q3GLdW2Mu9I-noHct-UaTi3c')

API = 'd6b7da0b736343c5ba6100556230307'



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет рад тебя видет')

@bot.message_handler(content_types=['text'])
def get_wather(message):
    city = message.text.strip().lower()
    res=requests.get(f'http://api.weatherapi.com/v1/current.json?key={API}&q={city}')
    # bot.reply_to(message, f'now weather: {res.json()}')
    data = json.loads(res.text)
    temp_c= data["current"]["temp_c"]
    region = data["location"]["region"]
    bot.reply_to(message, f'Сейчас погода в:{region}е {temp_c}*C')

    image = 'sunny.png' if temp_c > 5 else 'rain.png'
    file = open('./'+ image, 'rb')
    bot.send_photo(message.chat.id, file)


bot.polling(non_stop=True)    

# {'location': {'name'}: 'Bishkek', 'region': 'Bishkek', 'country': 'Kyrghyzstan', 'lat': 42.87, 'lon': 74.6, 'tz_id': 'Asia/Bishkek', 'localtime_epoch': 1688380455, 'localtime': '2023-07-03 16:34'}, 