import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    # ensure db file can connect by create a database connection to the db file FaceBase.db
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    # close connection after opened
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_connection("../FaceBase.db")
