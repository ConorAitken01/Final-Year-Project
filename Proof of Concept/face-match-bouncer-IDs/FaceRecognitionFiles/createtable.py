import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    # create a database connection to the db file FaceBase.db
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    # create a table from the create_table_sql statement
    # Passing in the Connection object and the create table SQL statement
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "FaceBase.db"

    # SQL statement that creates the People table if its not already there
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS People (
                                        ID text PRIMARY KEY,
                                        Name text NOT NULL,
                                        Age text NOT NULL
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)

    else:
        # give error message if it doesn't connect
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
