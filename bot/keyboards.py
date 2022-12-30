from telebot import types
from datetime import datetime


class Keyboard:
    @staticmethod
    def main():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=8)
        today = types.KeyboardButton('Світло сьогодні')
        tomorrow = types.KeyboardButton('Світло завтра')
        markup.add(today, tomorrow)
        markup.add(
            types.KeyboardButton('Пн'),
            types.KeyboardButton('Вт'),
            types.KeyboardButton('Ср'),
            types.KeyboardButton('Чт'),
            types.KeyboardButton('Пт'),
            types.KeyboardButton('Сб'),
            types.KeyboardButton('Нд')
        )
        return markup

    @staticmethod
    def choose_group(day: int = None):
        keyboard = types.InlineKeyboardMarkup()
        if day is None:
            day = datetime.now().weekday()
        for num in (1, 2, 3):
            button = types.InlineKeyboardButton(text=f'Група {num}', callback_data=f'group {num} day {day}')
            keyboard.add(button)
        return keyboard

    @staticmethod
    def send_photo(group: int):
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Показати фото', callback_data=f'show_photo group {group}')
        change_group = types.InlineKeyboardButton(text='Змінити групу', callback_data=f'change_group {group}')

        keyboard.add(button)
        keyboard.add(change_group)
        return keyboard

    @staticmethod
    def send_tomorrow_schedule():
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='toworrow schedule', callback_data='tomorrow_power_schedule')
        keyboard.add(button)
        return keyboard

    @staticmethod
    def group_answer(group: int):
        keyboard = types.InlineKeyboardMarkup()
        photo = types.InlineKeyboardButton(text='Показати фото', callback_data=f'show_photo group {group}')
        schedule = types.InlineKeyboardButton(text='Статус інших груп', callback_data=f'another_groups {group}')
        change_group = types.InlineKeyboardButton(text='Змінити групу', callback_data=f'change_group {group}')
        keyboard.add(photo)
        keyboard.add(schedule)
        keyboard.add(change_group)
        return keyboard
