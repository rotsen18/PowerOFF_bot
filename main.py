import os
import sqlite3
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime, timedelta

import telebot

import settings
from bot.commands import Command
from bot.keyboards import Keyboard

bot = telebot.TeleBot(settings.TOKEN)

conn = sqlite3.connect(settings.DB_NAME, check_same_thread=False)
cursor = conn.cursor()


def create_user(user_id: int, first_name: str, last_name: str, username: str, chat_id: int):
    cursor.execute('INSERT INTO bot_user (user_id, first_name, last_name, username, chat_id) VALUES (?, ?, ?, ?, ?)',
                   (user_id, first_name, last_name, username, chat_id))
    conn.commit()


def get_user(user_id: int):
    cursor.execute('SELECT * FROM bot_user WHERE user_id = ?', (user_id,))
    return cursor.fetchone()


def get_user_group(user_id: int):
    cursor.execute('SELECT group_id FROM bot_user WHERE user_id = ?', (user_id,))
    group = cursor.fetchone()
    if group:
        return group[0]

def set_user_group(user_id: int, group_id: int):
    sql_update_query = """UPDATE bot_user SET group = ? WHERE user_id = ?"""
    data = (group_id, user_id)
    cursor.execute(sql_update_query, data)
    conn.commit()


@bot.message_handler(content_types=["text"])
def main_menu(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    # if user is None:
    #     first_name = message.from_user.first_name
    #     last_name = message.from_user.last_name
    #     username = message.from_user.username
    #     create_user(user_id=user_id, first_name=first_name, last_name=last_name, username=username, chat_id=chat_id)

    if message.text.lower() in ('/menu', '/start'):
        bot.send_message(message.chat.id, 'hello:)', reply_markup=Keyboard.main())
    elif message.text.lower() == '/which_group':
        bot.send_message(message.chat.id, 'https://poweroff.loe.lviv.ua/gav_city3')
    elif message.text.lower() == 'світло сьогодні':
        weekday = datetime.now().weekday()
        bot.send_message(message.chat.id, 'Вибери групу:', reply_markup=Keyboard.choose_group(day=weekday))
    elif message.text.lower() == 'світло завтра':
        tomorrow = datetime.now() + timedelta(days=1)
        weekday = tomorrow.weekday()
        bot.send_message(message.chat.id, 'Вибери групу:', reply_markup=Keyboard.choose_group(day=weekday))
    elif message.text.lower() == 'zakaz':
        response_text = Command.zakaz_shedule()
        bot.send_message(message.chat.id, response_text, reply_markup=Keyboard.main())
    elif message.text.lower() == 'me':
        me = get_user(user_id=2)
        bot.send_message(message.chat.id, f'your group is {me}')
    else:
        bot.send_message(message.chat.id, 'unknown')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:  # message from chat with bot
        if call.data.startswith('group '):
            _, group, _, day = call.data.split()
            response_text = Command.day_power_off_schedule(int(group), int(day))
            if int(day) == datetime.now().weekday():
                bot.send_message(call.message.chat.id, text=response_text, reply_markup=Keyboard.group_answer(group),
                                 parse_mode='HTML')
            else:
                bot.send_message(call.message.chat.id, text=response_text, reply_markup=Keyboard.send_photo(group))
        elif call.data.startswith('show_photo'):
            _, _, group_num = call.data.split()
            img = f'https://poweroff.loe.lviv.ua/static/img/{int(group_num)}group.png'
            bot.send_photo(call.message.chat.id, img, reply_markup=Keyboard.main())
        elif call.data.startswith('another_groups'):
            _, group_id = call.data.split()
            response_text = Command.another_group_statuses(int(group_id))
            bot.send_message(call.message.chat.id, response_text, reply_markup=Keyboard.main())
    elif call.inline_message_id:  # message from inline mode
        if call.data == "test":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="another")


if __name__ == '__main__':
    # bot.infinity_polling()
    bot.polling(none_stop=True)
