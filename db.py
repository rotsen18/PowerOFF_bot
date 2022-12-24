import mysql.connector

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

    @staticmethod
    def create_user(user_id: int, first_name: str, last_name: str, username: str, chat_id: int):
        with MySQLCursor(commit=True) as cursor:
            cursor.execute(
                'INSERT INTO user_bot (user_id, first_name, last_name, username, chat_id) VALUES (?, ?, ?, ?, ?)',
                (user_id, first_name, last_name, username, chat_id)
            )

    @staticmethod
    def get_user(user_id: int):
        with MySQLCursor(as_dict=True) as cursor:
            cursor.execute(f'SELECT * FROM user_bot WHERE user_id = {user_id}')
            user = cursor.fetchone()
            return user

    @staticmethod
    def get_user_group(user_id: int):
        with MySQLCursor() as cursor:
            cursor.execute('SELECT group_id FROM user_bot WHERE user_id = ?', (user_id,))
            group = cursor.fetchone()
            if group:
                return group[0]

    @staticmethod
    def set_user_group(user_id: int, group_id: int):
        with MySQLCursor(commit=True) as cursor:
            sql_update_query = 'UPDATE user_bot SET group = ? WHERE user_id = ?'
            data = (group_id, user_id)
            cursor.execute(sql_update_query, data)
