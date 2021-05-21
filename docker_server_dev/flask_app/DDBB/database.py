import mysql.connector as db
from json import loads
import logging
import traceback
import os


class User:

    def __init__(self):
        try:
            db_file_name = str(os.getcwd()).split('app')[0] + "app/DDBB/db_data.json"
            with open(db_file_name, 'r') as db_data_file:
                db_data = loads(db_data_file.read())
            self.db = db.connect(
                user=db_data['database']['user'],
                password=db_data['database']['password'],
                host=db_data['database']['host'],
                port=db_data['database']['port'],
                database=db_data['database']['database']
            )
            self.cursor = self.db.cursor()
        except IOError as ex:
            logging.error('CREATE_DATABASE IOERROR:\n%s\n%s', ex, traceback.format_exc())
        except db.Error as ex:
            logging.error('CREATE_DATABASE DB.ERROR:\n%s\n%s', ex, traceback.format_exc())
        except Exception as ex:
            logging.error('CREATE_DATABASE EXCEPTION:\n%s\n%s', ex, traceback.format_exc())

    def close(self):
        self.cursor.close()
        self.db.close()

    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        return tuple(self.cursor.fetchall())

    def set_user(self, user_data):
        message = "Unable to insert user"
        if 'name' in user_data and user_data['name'] != '':
            if self.__check_user(user_data['name']):
                message = message + ": '{user_name}' already exists".format(user_name=user_data['name'])
                return True, message
            self.cursor.execute("INSERT INTO users (name) VALUES ('{user_name}')".format(user_name=user_data['name']))
            self.db.commit()
            return True, "New user {user_name} inserted".format(user_name=user_data['name'])
        return False, message

    def __check_user(self, user_name):
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE name = '{user_name}'".format(user_name=user_name))
        return True if self.cursor.fetchall()[-1][-1] > 0 else False
