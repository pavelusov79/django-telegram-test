import telebot
from telebot import types
from django_telegram.settings import BOT_TOKEN


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(
        'Авторизоваться', url=f'http://127.0.0.1:8000/?id={message.from_user.id}&name={message.from_user.first_name}&'
                              f'u={message.from_user.username}'
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
    else:
        bot.send_message(callback.message.chat.id, 'Вы успешно авторизовались на сайте.')


bot.polling(none_stop=True)


