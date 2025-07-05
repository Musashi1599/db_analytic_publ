import telebot
import pars
import os
from telebot import types
from telebot.util import split_string
from config import token
from text_handler import text

bot = telebot.TeleBot(token)

last_message_id = None
last_message_text =''
zad_mess = ''
running = True
first_name = ''


def bot_start():
    while running:
        bot.infinity_polling(timeout=10, long_polling_timeout = 5)

def send_mess(chat_id, message, markup) -> None:
    global last_message_id
    global last_message_text

    mess = bot.send_message(chat_id=chat_id, text=message, reply_markup=markup)
    last_message_id = mess.message_id
    last_message_text = message

def send_long_message(bot, chat_id, text, max_length=4096, **kwargs):
    """
    Отправляет длинное сообщение, разбивая его на части
    :param bot: объект TeleBot
    :param chat_id: ID чата
    :param text: текст сообщения
    :param max_length: максимальная длина части (по умолчанию 4096)
    :param kwargs: дополнительные параметры для send_message
    """
    for part in split_string(text, max_length):
        bot.send_message(chat_id, part, **kwargs)


def create_buttons(*args):
    markup = types.InlineKeyboardMarkup()
    half_len = int(len(args)/2)
    for i in range(half_len):
        if 'http' in args[i+half_len]:
            markup.add(types.InlineKeyboardButton(args[i], url=args[i+half_len]))
        else:    
            markup.add(types.InlineKeyboardButton(args[i],callback_data=args[(i+half_len)]))

    return markup



@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Статистика по СРО")
    #btn2 = types.KeyboardButton("Тенденция по всем АУ за месяц") пока убрал фичу
    markup.add(btn1)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@bot.message_handler(content_types='text')
def text_h(mess):
    b = bot
    text(b, mess)


bot_start()