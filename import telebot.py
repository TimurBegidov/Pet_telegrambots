import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot('7114468628:AAFngtTnCJiyM9aje23VnM-uBj8cWXoMAhQ')
name=None




@bot.message_handler(commands=['start'])
def starter(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Больше о нас')
    btn2 = types.KeyboardButton('Оставить контакты')
    resize = True
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}', parse_mode='html', reply_markup=markup)
    conn = sqlite3.connect('dbusers.sql')
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS users (id int a auto_increment primary key,name varchar(50),contacts varchar(50),status varchar(10))')
    conn.commit()
    cur.close()
    conn.close()


@bot.message_handler()
def btn(message):
    if message.text.lower() == 'больше о нас':
        bot.send_message(message.chat.id,
                         f'Варфоломе́евская ночь (фр. Massacre de la Saint-Barthélemy — резня святого Варфоломея) — массовое убийство гугенотов во Франции, устроенное католиками в ночь на 24 августа 1572 года, в канун дня святого Варфоломея. По различным оценкам, в Париже в этот день погибло около трёх тысяч человек, а по всей Франции в погромах было убито около 30 тысяч гугенотов.',
                         parse_mode='html')
    elif message.text.lower() == 'оставить контакты':
        bot.send_message(message.chat.id, f'Введите свое имя и фамилию ', parse_mode='html')
        bot.register_next_step_handler(message,user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, f'Введите контактную информацию ', parse_mode='html')
    bot.register_next_step_handler(message, user_contacts)

def user_contacts(message):
    contacts = message.text.strip()
    conn = sqlite3.connect('dbusers.sql')
    cur = conn.cursor()
    cur.execute(f"INSERT INTO users (name,contacts) VALUES('%s','%s')" % (name, contacts))
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, f'Данные сохранены,мы скоро свяжемся с вами. ', parse_mode='html')


bot.polling(non_stop=True)
