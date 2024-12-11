import json
import webbrowser

import telebot
import redis
from telebot import types
from django_telegram.settings import BOT_TOKEN


bot = telebot.TeleBot(BOT_TOKEN)

# вариант №1. Передать данные как get параметры в url и затем уже в джанго их вывести
# btn 1 = types.InlineKeyboardButton(
#         'Авторизоваться', url=f'http://127.0.0.1:8000/?id={message.from_user.id}&name={message.from_user.first_name}&'
#                               f'u={message.from_user.username}
# )
# вариант №2. Используем redis. Данные кешируем и затем в джанго обращаемся к redis кэшу и авторизовываем пользователя.


@bot.message_handler(commands=['start'])
def main(message):

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(
        'Авторизоваться', callback_data='auth'
    )
    btn2 = types.InlineKeyboardButton('Отмена', callback_data='delete')
    markup.add(btn1, btn2)
    text = f'Добро пожаловать на сайт {message.from_user.first_name}.\nДля авторизации на сайте нажмите ' \
           f'кнопку Авторизоваться. Если вы зашли по ошибке нажмите Отмена.'
    bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_func(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'auth':
        data_user = {
            'id': callback.message.chat.id,
            'name': callback.message.chat.first_name,
            'u': callback.message.chat.username
        }
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.set('data_user', json.dumps(data_user), 120)
        bot.send_message(callback.message.chat.id, 'Вы успешно авторизовались на сайте.')
        webbrowser.open('http://127.0.0.1:8000')


bot.polling(none_stop=True)


