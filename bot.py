import telebot

from rates import *
from env import *
from pprint import pprint

import requests
import math


bot = telebot.TeleBot(TOKEN)

need_sum = 0
all_sum = 0

main_keyboard = telebot.types.ReplyKeyboardMarkup(True)
main_keyboard.row('My Data')
main_keyboard.row('Change need number')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello, you can enter the number you need (BYN)!')
    bot.register_next_step_handler(message, get_need_sum)


def get_need_sum(message):
    global need_sum
    flag = 1
    try:
        need_sum = int(message.text)
    except:
        bot.send_message(message.from_user.id, 'incorrect number, try again')
        bot.register_next_step_handler(message, get_need_sum)
        flag = 0
    if flag:
        bot.send_message(message.from_user.id, 'Cool, I saved your number(' + str(need_sum) + ' BYN).',
                         reply_markup=main_keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'my data':
        get_data(message)
    elif message.text.lower() == 'change need number':
        bot.register_next_step_handler(message, get_need_sum)
    else:
        cur_sum = 0
        global all_sum
        try:
            cur_sum = int(message.text)
        except:
            bot.send_message(message.from_user.id, 'incorrect number')
        all_sum += cur_sum
        global need_sum
        if need_sum:
            percent = round(all_sum / need_sum * 100, 2)
        else:
            percent = 101

        out = 'Saved! now you have: ' + str(all_sum) + ' BYN\n' + 'It`s ' + str(percent) + '%'
        bot.send_message(message.from_user.id, out)


def get_data(message):
    global all_sum
    global need_sum
    rate = get_rate('USD')
    need_sum_usd = round(need_sum / rate, 2)
    all_sum_usd = round(all_sum / rate, 2)
    str1 = 'You need:\n' + str(need_sum) + ' BYN\n' + str(need_sum_usd) + ' USD'
    str2 = 'You have:\n' + str(all_sum) + ' BYN\n' + str(all_sum_usd) + ' USD'
    if need_sum:
        percent = round(all_sum / need_sum * 100, 2)
    else:
        percent = 101
    str3 = 'It`s ' + str(percent) + '%'
    bot.send_message(message.chat.id, str1 + '\n' + str2 + '\n' + str3)


bot.polling()
