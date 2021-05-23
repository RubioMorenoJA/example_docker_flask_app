import mysql.connector as db
from json import loads
import logging
import traceback
import os


def check_empty_fields(user_data):
    return all(map(lambda value: value and value != '', user_data.values()))


class User:

    user_keys = ('name', 'email', 'address', 'phone')

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

    def __check_all_user_data(self, user_data):
        user_data_keys = user_data.keys()
        return all(map(lambda key: key in user_data_keys, self.user_keys)) and check_empty_fields(user_data)

    def __check_any_user_data(self, user_data):
        user_data_keys = user_data.keys()
        return any(map(lambda key: key in user_data_keys, self.user_keys)) and check_empty_fields(user_data)

    def __check_user_exists(self, user_data):
        self.cursor.execute(
            """
            SELECT COUNT(*) FROM users 
            WHERE name = '{user_name}' OR email = '{user_email}'
            """.format(user_name=user_data['name'], user_email=user_data['email'])
        )
        return True if self.cursor.fetchall()[-1][-1] > 0 else False

    def get_users(self, user_id: str = None):
        query = "SELECT * FROM users"
        if user_id:
            query = query + f" WHERE id = '{user_id}'"
            self.cursor.execute(query)
            result = tuple(self.cursor.fetchall())
            if len(result) > 0:
                return result, 200
            return f'Unable to get user with id {user_id}', 404
        self.cursor.execute(query)
        return tuple(self.cursor.fetchall()), 200

    def set_user(self, user_data):
        message = "Unable to insert user"
        if self.__check_all_user_data(user_data):
            if self.__check_user_exists(user_data):
                message = message + ": '{user_name}' already exists".format(user_name=user_data['name'])
                return message, 405
            query = """
                INSERT INTO users (name, email, address, phone) 
                VALUES (%s, %s, %s, %s)
                """
            values = (f"{user_data['name']}", f"{user_data['email']}",
                      f"{user_data['address']}", f"{user_data['phone']}")
            self.cursor.execute(query, values)
            self.db.commit()
            return "New user {user_name} inserted".format(user_name=user_data['name']), 201
        return message, 400

    def set_user_changes(self, user_id, user_data):
        if self.__check_any_user_data(user_data):
            update_query = ", ".join([f"{key} = '{value}'" for key, value in user_data.items()])
            self.cursor.execute(
                """
                UPDATE users 
                SET {update_query}
                WHERE id = {user_id}                
                """.format(user_id=user_id, update_query=update_query)
            )
            self.db.commit()
            if self.cursor.rowcount > 0:
                return f'Changes applied on {self.cursor.rowcount} items', 202
            return 'Unable to apply changes', 404
        return 'Fields cannot be empty', 400

    def delete_user(self, user_id):
        query = """
            DELETE FROM users WHERE id = %s
            """
        values = (f"{user_id}", )
        self.cursor.execute(query, values)
        self.db.commit()
        if self.cursor.rowcount > 0:
            return f'User with id {user_id} was deleted', 200
        return f'Unable to delete user with id {user_id}', 404
