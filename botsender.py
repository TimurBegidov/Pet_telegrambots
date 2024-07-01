import re
import telebot
import smtplib
from telebot import types
import os
from email.mime.text import MIMEText


#Токен бота Ы
bot = telebot.TeleBot('6798707022:AAGmABw5r95MHNSFOzIq5LBy5prOMXhL6QU')

#Логин и пароль почты,с которой отправляется сообщение 
login='timurbegidov@yandex.ru'
password='5223456415Bb'
email='beg.tim@bk.ru'
subject='Заголовок'

#Клавиатуры
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn2 = types.KeyboardButton('Хочу оставить заявку!')
markup.row( btn2)

markup_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_back = types.KeyboardButton('Вернуться')
markup_back.row(btn_back)

#Реакция на команду /start
@bot.message_handler(commands=['start'])
def starter(message):
    bot.send_message(message.chat.id, f'Здравствуйте!', parse_mode='html',reply_markup=markup)
    user_id = message.from_user.id
    bot.send_message(message.chat.id, f'Здесь вы можете оставить заявку на аккредитацию.', parse_mode='html')
    
#Реакция на кнопку "хочу оставить заявку!"
@bot.message_handler()
def btn(message):
    if message.text.lower() == 'хочу оставить заявку!':
        bot.send_message(message.chat.id, f'Как к вам можно обращаться', parse_mode='html',
                         reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, user_name)
    elif message.text.lower() == 'вернуться':
            bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}!', parse_mode='html',
                         reply_markup=markup)
            bot.send_message(message.chat.id, f'Здесь вы можете оставить заявку на аккредитацию.', parse_mode='html')
    
        
# Функция приема имя пользователя   
def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, f'Введите свою контактную информацию(e-mail или номер телефона)', parse_mode='html')
    bot.register_next_step_handler(message, user_contacts)


# Функция приема контактов пользователя
def user_contacts(message):
    contacts = message.text.strip()
    #Маски на email и телефон
    nresult = re.match(r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$", contacts)
    eresult = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", contacts)
    if bool(nresult) | bool(eresult) == True:
        bot.send_message(message.chat.id, f'Данные отправлены на обработку,в скором времени мы свяжемся с вами.',
                         parse_mode='html',
                         reply_markup=markup_back)
        #Вызов функции отправки сообщения 
        send_email("Имя:"+name+" - Контакты:"+contacts)
    else:
        bot.send_message(message.chat.id, f'Что-то пошло не так!Поверьте введенные данные.', parse_mode='html')
        bot.register_next_step_handler(message, user_contacts)

#Функция настройки отправки сообщения 
def send_email(text:str):
    msg=MIMEText(f'{text}','plain','utf-8')
    msg['subject']=subject
    msg['From']=login
    msg['To']=email
    
    s=smtplib.SMTP('smtp.yandex.ru',587,timeout=10)
    try:
        s.starttls()
        s.login(login,password)
        s.sendmail(msg['From'],msg['To'],msg.as_string())
    except Exception as ex:
        print('Error')
    finally:
        s.quit()
    
        

bot.polling(non_stop=True)