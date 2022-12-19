from datetime import datetime, timedelta

from models import User, db_handle
import settings
from bot.commands import Command
from bot.keyboards import Keyboard


bot = PowerOFF_bot.TeleBot(settings.TOKEN)


@bot.message_handler(content_types=["text"])
def main_menu(message):
    if message.text.lower() in ('/menu', '/start'):
        with db_handle:
            user = User.get_or_create(
                id=message.from_user.id,
                defaults={
                    'id': message.from_user.id,
                    'username': message.from_user.username,
                    'first_name': message.from_user.first_name
                }
            )
        bot.send_message(message.chat.id, 'hello:)', reply_markup=Keyboard.main())
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
    else:
        bot.send_message(message.chat.id, 'unknown')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:  # message from chat with bot
        if call.data.startswith('group '):
            _, group, _, day = call.data.split()
            response_text = Command.day_power_off_schedule(int(group), int(day))
            bot.send_message(call.message.chat.id, text=response_text, reply_markup=Keyboard.send_photo(group), parse_mode='HTML')
        elif call.data.startswith('show_photo'):
            _, _, group_num = call.data.split()
            img = f'https://poweroff.loe.lviv.ua/static/img/{int(group_num)}group.png'
            bot.send_photo(call.message.chat.id, img, reply_markup=Keyboard.main())
    elif call.inline_message_id:  # message from inline mode
        if call.data == "test":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="another")


if __name__ == '__main__':
    bot.infinity_polling()
