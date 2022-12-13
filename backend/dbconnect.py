import psycopg2
import config

conn = None

# Handles the connection to the database.
# connect () Initiates the connection to the DB.
def connect():
    global conn
    try:
        params = config.config()

        print('Connecting to database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# closed() Ensures that the db connection is closed afterwards.
# noinspection PyUnresolvedReferences
def close():
    global conn
    try:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
        else:
            print('Database connection already closed')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
