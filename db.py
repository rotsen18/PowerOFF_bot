import mysql.connector
from telebot.types import User

import settings


class MySQLCursor:
    def __init__(self, commit=False, as_dict=False):
        self.dictionary = as_dict
        self.commit = commit

    def __enter__(self):
        self.conn = mysql.connector.connect(
            host=settings.DB_HOST,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        self.cursor = self.conn.cursor(dictionary=self.dictionary)
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.commit:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()
        return


class DB:

    @classmethod
    def create_user(cls, _id: int, name: str, surname: str, us_name: str, user_chat_id: int):
        with MySQLCursor(commit=True) as cursor:
            sql_update_query = f"INSERT INTO user_bot (user_id, first_name, last_name, username, chat_id) VALUES (%s, %s, %s, %s, %s)"
            data = (_id, name, surname, us_name, user_chat_id)
            cursor.execute(sql_update_query, data)
        return cls.get_user(_id)

    @staticmethod
    def get_user(user_id: int):
        with MySQLCursor(as_dict=True) as cursor:
            cursor.execute(f'SELECT * FROM user_bot WHERE user_id = {user_id}')
            user = cursor.fetchone()
            return user

    @staticmethod
    def get_all_users():
        with MySQLCursor(as_dict=True) as cursor:
            cursor.execute(f'SELECT * FROM user_bot')
            users = cursor.fetchall()
            return users

    @staticmethod
    def set_user_group(user_id: int, group_id: int):
        with MySQLCursor(commit=True) as cursor:
            sql_update_query = 'UPDATE user_bot SET group_id = %s WHERE user_id = %s'
            input_data = (group_id, user_id)
            cursor.execute(sql_update_query, input_data)

    @classmethod
    def get_or_create_user(cls, user_id: int, defaults: User):
        user = cls.get_user(user_id)
        if user:
            return user, False
        kwargs = {
            'name': defaults.first_name,
            'surname': defaults.last_name,
            'us_name': defaults.username,
            '_id': defaults.id,
            'user_chat_id': defaults.id,
        }
        return cls.create_user(**kwargs), True

    @classmethod
    def increase_user_message(cls, user_id: int):
        with MySQLCursor(commit=True) as cursor:
            sql_update_query = 'UPDATE user_bot SET message_count = message_count + 1 WHERE user_id = %s'
            input_data = (user_id,)
            cursor.execute(sql_update_query, input_data)
