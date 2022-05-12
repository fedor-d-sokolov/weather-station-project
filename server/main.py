# -*- coding: utf-8 -*-

import telebot
import threading
import config
import server

bot = telebot.TeleBot(config.settings["TELEGRAM_API_KEY"])


def start(message):
    text = "*Hello!\n"
    text += f"This bot allows you to get the weather directly from meteostation in {config.settings['LOCATION']}.*\n\n"
    text += "Command list:\n"
    text += "`/weather` - Get latest uploaded weather.\n"

    markup = telebot.types.InlineKeyboardMarkup()

    markup.add(telebot.types.InlineKeyboardButton("Get current weather 🌞", callback_data="get_weather"))
    bot.send_message(message.chat.id,
                     text,
                     disable_web_page_preview=True,
                     parse_mode='Markdown',
                     reply_markup=markup)


def weather(message):
    bot.send_message(chat_id=message.chat.id,
                     text=server.last_received_data,
                     parse_mode='Markdown')


def bot_thread():
    bot.infinity_polling()


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "get_weather":
        bot.send_message(chat_id=call.message.chat.id, text=server.last_received_data, parse_mode='Markdown')
        bot.answer_callback_query(call.id, f"Sent current weather!")


if __name__ == '__main__':
    print("Adding message handlers...")

    bot.register_message_handler(start, commands=["start"])
    bot.register_message_handler(weather, commands=["weather"])

    print("Starting bot thread...")
    threading.Thread(target=bot_thread).start()

    server.start()
