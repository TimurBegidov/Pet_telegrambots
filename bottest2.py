import re
import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot('7114468628:AAFngtTnCJiyM9aje23VnM-uBj8cWXoMAhQ')
name = None
Admint_id = 519234757
#Admind_id =

user_id = ''

# Клава user
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton('Расскажите мне о вашей компании')
btn2 = types.KeyboardButton('Хочу пройти консультацию')
markup.row(btn1, btn2)

markup_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_back = types.KeyboardButton('Вернуться')
markup_back.row(btn_back)

# Клава admin
markup_admin_conect = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1_con = types.KeyboardButton('Расскажите мне о вашей компании')
btn2_con = types.KeyboardButton('Хочу пройти консультацию')
btn_con = types.KeyboardButton('Админ-панель')
markup_admin_conect.row(btn_con, btn1_con, btn2_con)

markup_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1_admin = types.KeyboardButton('Информация по клиентам')
btn2_admin=types.KeyboardButton('Вернуться')
markup_admin.row(btn1_admin,btn2_admin)


# Страт
@bot.message_handler(commands=['start'])
def starter(message):
    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}!', parse_mode='html',
                     reply_markup=markup)
    user_id = message.from_user.id
    conn = sqlite3.connect('dbusers.sql')
    cur = conn.cursor()
    # Создание бд
    cur.execute(
        'CREATE TABLE IF NOT EXISTS users (num int auto_increment primary key,id int ,name varchar(50),contacts varchar(50),status varchar(10))')
    conn.commit()
    cur.close()
    conn.close()
    if message.from_user.id == Admint_id:
        bot.send_message(message.chat.id, f'Подключиться к админ-панели', parse_mode='html',
                         reply_markup=markup_admin_conect)


# Логика кнопок
@bot.message_handler()
def btn(message):
    if message.text.lower() == 'расскажите мне о вашей компании':
        bot.send_message(message.chat.id,
                         f'Варфоломе́евская ночь (фр. Massacre de la Saint-Barthélemy — резня святого Варфоломея) — массовое убийство гугенотов во Франции, устроенное католиками в ночь на 24 августа 1572 года, в канун дня святого Варфоломея. По различным оценкам, в Париже в этот день погибло около трёх тысяч человек, а по всей Франции в погромах было убито около 30 тысяч гугенотов.',
                         parse_mode='html')
    elif message.text.lower() == 'хочу пройти консультацию':
        bot.send_message(message.chat.id, f'Как к вам можно обращаться', parse_mode='html',
                         reply_markup=types.ReplyKeyboardRemove())

        bot.register_next_step_handler(message, user_name)
    elif message.text.lower() == 'вернуться':
        if message.from_user.id == Admint_id:
            bot.send_message(message.chat.id, f'Админ_панель включена', parse_mode='html', reply_markup=markup_admin_conect)
        else:
            bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}!', parse_mode='html',
                         reply_markup=markup)
    elif message.text.lower() == 'админ-панель' and message.from_user.id == Admint_id:
        bot.send_message(message.chat.id, f'Админ_панель включена', parse_mode='html', reply_markup=markup_admin)
    elif message.text.lower() == 'информация по клиентам' and message.from_user.id == Admint_id:
        conn = sqlite3.connect('dbusers.sql')
        cur = conn.cursor()
        # Запрос в  бд
        cur.execute(
            'SELECT * FROM users')
        bdusers = cur.fetchall()
        info = ''
        for el in bdusers:
            info += f'id:{el[1]},Имя: {el[2]},Контакная информация: {el[3]}\n'

        cur.close()
        conn.close()
        bot.send_message(message.chat.id, info)
    else:
        bot.send_message(message.chat.id, f'Указана неверная команда', parse_mode='html', reply_markup=markup)


# Функция имени пользователя
def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, f'Введите свою контактную информацию(e-mail или номер телефона)', parse_mode='html')
    bot.register_next_step_handler(message, user_contacts)


# Функция контактов пользователя
def user_contacts(message):
    contacts = message.text.strip()
    nresult = re.match(r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$", contacts)
    eresult = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", contacts)

    if bool(nresult) | bool(eresult) == True:
        conn = sqlite3.connect('dbusers.sql')
        cur = conn.cursor()
        cur.execute(
            f"INSERT OR IGNORE INTO users (id,name,contacts) VALUES('%s','%s','%s')" % (message.from_user.id, name, contacts))
        conn.commit()
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, f'Данные сохранены,в скором времени мы свяжемся с вами.',
                         parse_mode='html',
                         reply_markup=markup_back)
    else:
        bot.send_message(message.chat.id, f'Что-то пошло не так!Поверьте введенные данные.', parse_mode='html')
        bot.register_next_step_handler(message, user_contacts)


bot.polling(non_stop=True)
