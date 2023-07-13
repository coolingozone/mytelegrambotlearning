# -*- coding: utf-8 -*-
"""
This Example will show you how to use register_next_step handler. 
This example ask user for message to translate then the language to translate
This example illustrate how to collect andsave user replies and process it
Author: Teo Kok Keong
Date: 13th July 2023
"""

import telebot
from telebot import types

API_TOKEN = 'Token'#replace by your bot api token

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}


class User:
    def __init__(self, name):
      
        self.msg = None
        self.lang = None


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Hi there, I am Example bot.
What's your Message?
""")
    bot.register_next_step_handler(msg, process_msg_step)


def process_msg_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user.msg = message.text
        user_dict[chat_id] = user
        print(message.text)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Chinese', 'Japanese')
        msg = bot.reply_to(message, 'language?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_lang_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')
    





def process_lang_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        lang= message.text
        user = user_dict[chat_id]
        if (lang == u'Chinese') or (lang == u'Japanese'):
            user.lang = lang
        else:
            raise Exception("Unknown language")
        #bot.send_message(chat_id, 'Nice to meet you ' + user.name +  + '\n Sex:' + user.sex)
    
    except Exception as e:
        bot.reply_to(message, 'oooops lang')
    
    bot.send_message(chat_id, 'your message :' + user.msg + '\n Languagee:'  + str(user.lang))

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()