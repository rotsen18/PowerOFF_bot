from telebot import types
from datetime import datetime


class Keyboard:
    @staticmethod
    def main():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        zakaz = types.KeyboardButton('Zakaz')
        today = types.KeyboardButton('Світло сьогодні')
        tomorrow = types.KeyboardButton('Світло завтра')
        markup.row(zakaz, today, tomorrow)
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
        keyboard.add(button)
        return keyboard

    @staticmethod
    def send_tomorrow_schedule():
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='toworrow schedule', callback_data='tomorrow_power_schedule')
        keyboard.add(button)
        return keyboard
