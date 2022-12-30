import os
import sys

from telebot import apihelper

from db import DB

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime, timedelta

import telebot

import settings
from bot.commands import Command
from bot.keyboards import Keyboard


apihelper.ENABLE_MIDDLEWARE = True

bot = telebot.TeleBot(settings.TOKEN)


class Admin:
    ADMIN_ID = settings.ADMIN_ID

    @classmethod
    def send_message(cls, message):
        bot.send_message(cls.ADMIN_ID, message)


@bot.middleware_handler(update_types=['message'])
def modify_message(bot_instance, message):
    user, created = DB.get_or_create_user(message.from_user.id, message.from_user)
    message.user = user
    if created:
        Admin.send_message(f'new user: {user}')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'hello:)')


@bot.message_handler(commands=['which_group'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'you can find your group on website:')
    bot.send_message(message.chat.id, 'https://poweroff.loe.lviv.ua/gav_city3', disable_web_page_preview=True)


@bot.message_handler(content_types=["text"])
def main_menu(message):
    group = message.user.get('group_id')
    if message.text.lower() == 'світло сьогодні':
        weekday = datetime.now().weekday()
        if group is None:
            bot.send_message(message.chat.id, 'Вибери групу:', reply_markup=Keyboard.choose_group(day=weekday))
        else:
            response_text = Command.day_power_off_schedule(group, weekday)
            bot.send_message(message.chat.id, text=response_text, reply_markup=Keyboard.group_answer(group),
                             parse_mode='HTML')
        return
    elif message.text.lower() == 'світло завтра':
        tomorrow = datetime.now() + timedelta(days=1)
        weekday = tomorrow.weekday()
        if group is None:
            bot.send_message(message.chat.id, 'Вибери групу:', reply_markup=Keyboard.choose_group(day=weekday))
        else:
            response_text = Command.day_power_off_schedule(group, weekday)
            bot.send_message(message.chat.id, text=response_text, reply_markup=Keyboard.send_photo(group))
        return
    for weekday, day_name in enumerate(['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд']):
        if message.text == day_name:
            if group is None:
                bot.send_message(message.chat.id, 'Вибери групу:', reply_markup=Keyboard.choose_group(day=weekday))
            else:
                response_text = Command.day_power_off_schedule(group, weekday)
                bot.send_message(message.chat.id, text=response_text, reply_markup=Keyboard.send_photo(group))
            return

    if message.text.lower() == 'zakaz':
        response_text = Command.zakaz_shedule()
        bot.send_message(message.chat.id, response_text, reply_markup=Keyboard.main())
    elif message.text.lower() == 'me':
        bot.send_message(message.chat.id, str(message.user))
    elif message.text.lower() == 'users':
        rows = DB.get_all_users()
        bot.send_message(message.chat.id, f'total: {len(rows)}')
        for i, row in enumerate(rows):
            bot.send_message(message.chat.id, f'{i}. {row}')
    else:
        bot.send_message(message.chat.id, 'unknown')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:  # message from chat with bot
        user_id = call.from_user.id
        if call.data.startswith('group '):
            _, group, _, day = call.data.split()
            DB.set_user_group(user_id, int(group))
            bot.send_message(call.message.chat.id, f'Now your group is {group}')
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
        elif call.data.startswith('change_group'):
            _, group_id = call.data.split()
            weekday = datetime.now().weekday()
            bot.send_message(call.message.chat.id, 'Вибери нову групу:',
                             reply_markup=Keyboard.choose_group(day=weekday))
    elif call.inline_message_id:  # message from inline mode
        if call.data == "test":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="another")


if __name__ == '__main__':
    bot.infinity_polling()
    # bot.polling(none_stop=True)
