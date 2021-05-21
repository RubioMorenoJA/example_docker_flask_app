import mysql.connector as db
from json import loads
import logging
import traceback


def create_db():
    db_created = False
    try:
        with open('db_data.json', 'r') as db_data_file:
            db_data = loads(db_data_file)
        db_connection = db.connect(
            user=db_data['database']['user'],
            password=db_data['database']['password'],
            host=db_data['database']['host'],
            port=db_data['database']['port']
        )
        db_cursor = db_connection.cursor()
        db_cursor.execute(f"CREATE DATABASE {db_data['database']['database']}")
        db_created = True
    except IOError as ex:
        logging.error('CREATE_DATABASE IOERROR:\n%s\n%s', ex, traceback.format_exc())
    except db.Error as ex:
        logging.error('CREATE_DATABASE DB.ERROR:\n%s\n%s', ex, traceback.format_exc())
    except Exception as ex:
        logging.error('CREATE_DATABASE EXCEPTION:\n%s\n%s', ex, traceback.format_exc())
    finally:
        return db_created


logging.info("Database created successfully") if create_db() else logging.error("Error creating database")
