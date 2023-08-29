import telebot
import webbrowser
import sqlite3
from telebot import types

bot = telebot.TeleBot('6060654735:AAE49vWP-Kf7IZapTTj3-kgwmMwrlqYnGEE')

name = None

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('ecommerce.sql')
    cur = conn.cursor()


    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primery key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привет сейчас тебя сохраним')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()        
    bot.send_message(message.chat.id, 'введите пароль')
    bot.register_next_step_handler(message, user_password)



def user_password(message):
    password = message.text.strip() 

    conn = sqlite3.connect('ecommerce.sql')
    cur = conn.cursor()


    cur.execute(f"INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('list users', callback_data='users'))

    bot.send_message(message.chat.id, 'Пользователь зарегистрирован', reply_markup=markup)
    # bot.register_next_step_handler(message, user_password)

@bot.callback_query_handler(func=lambda call: True)
def calllback_sql(call):
    conn = sqlite3.connect('ecommerce.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users=cur.fetchall()

    info = ''
    for el in users:
        info += f'Имя: {el[1]}, пароль: {el[2]}\n'
    
    cur.close()
    conn.close()
    
    bot.send_message(call.message.chat.id, info)


@bot.message_handler(commands=['hello','whatsapp'])
def main(message):
    markup = types.ReplyKeyboardMarkup()
    btn_1=types.KeyboardButton('/site',)
    markup.row(btn_1)
    btn_2 = types.KeyboardButton('привет',)
    btn_3=types.KeyboardButton('/info',)
    markup.row(btn_2, btn_3)
    file = open('killua.jpeg', 'rb')
    bot.send_photo(message.chat.id, file, reply_markup=markup)

    bot.send_message(message.chat.id, 'Hello man', reply_markup=markup)

@bot.message_handler(commands=['info'])
def main(message):
    bot.send_message(message.chat.id, f'Informaton for you,{message.from_user.first_name}')

@bot.message_handler(commands=['site','website'])
def site(message):
    webbrowser.open('https://myshopecommerce.pythonanywhere.com/api/v1/')

@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    elif message.text.lower() == 'id':
        bot.send_message(message.chat.id, f'ID: {message.from_user.id}')

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn_1=types.InlineKeyboardButton('open site',url='https://instagram.com')
    markup.row(btn_1)
    btn_2 = types.InlineKeyboardButton('удалить',callback_data='delete')
    btn_3=types.InlineKeyboardButton('изменить', callback_data='edit')
    markup.row(btn_2, btn_3)

    # bot.send_message(message.chat.id,'beauty photo')
    bot.reply_to(message, 'какое красивое фото',reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('edit ', callback.message.chat.id, callback.message.message_id)    

bot.infinity_polling()
# bot.polling(non_stop=True)