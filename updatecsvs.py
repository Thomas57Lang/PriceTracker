import psycopg2
from psycopg2 import sql
import config
import pandas as pd
import csv

# Connection variable created by psycopg2 handles the connection to the DB.
conn = None


# Handles the connection to the database.
#


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


# get_skus() Run a sql query to collect the SKUs from a particular table then outputs that in a CSV.
# Parameter: table_name - Name of the table to run the query on.
def get_skus(table_name):
    global conn
    cur = conn.cursor()
    # Execute sql query to select all rows from the table and get the SKUs.
    query = sql.SQL("SELECT {itemSKU} FROM {table};").format(
        table=sql.Identifier(table_name),
        itemSKU=sql.Identifier("itemSKU"), )
    cur.execute(query)
    # Collect the output using cur.fetchall().
    data = cur.fetchall()
    # Create dataframe and pass to pandas to parse and generate updated SKU.csv file. See
    # https://www.linkedin.com/pulse/how-create-pandas-data-frame-postgresql-psycopg-vitor-spadotto/ for more
    # information.
    cols = []
    for elt in cur.description:
        cols.append(elt[0])
    df = pd.DataFrame(data=data, columns=cols)
    # Then use df.to_csv to create the csv.
    df.to_csv(r"/Users/thomaslangston/PycharmProjects/pythonProject/" + table_name + ".csv", index=False)
    cur.close()


def get_table_csvs():
    global conn
    cur = conn.cursor()

    # Pull each table name.
    # SELECT TABLE_NAME
    # FROM INFORMATION_SCHEMA.TABLES
    # WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='public'
    query = sql.SQL("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = %s AND TABLE_SCHEMA = %s;")
    tt = 'BASE TABLE'
    ts = 'public'
    data = (tt, ts)
    cur.execute(query, data)
    tables = cur.fetchall()

    # Create dataframe and pass to pandas to parse and generate updated tables.csv file.
    cols = []
    for elt in cur.description:
        cols.append(elt[0])
    df = pd.DataFrame(data=tables, columns=cols)
    # Then use df.to_csv to create the csv.
    df.to_csv(r"/Users/thomaslangston/PycharmProjects/pythonProject/" + "tables" + ".csv", index=False)
    cur.close()


# TODO: Call each table using get_skus() and the csv from get_table_csvs() and update each CSV. Handle errors
#  gracefully.
def update_csvs():
    global conn
    cur = conn.cursor()
    # Update the tables csv.
    # For each table call get_skus and update the csv that the web scrapers will use.
    # Utilize try except block to handle failures.
    get_table_csvs()

    f = open('tables.csv')
    csvreader = csv.reader(f)
    tables = []

    for row in csvreader:
        if (row[0] != 'Item') & (row[0] != 'table_name'):
            get_skus(row[0])

    f.close()


# TODO: Create a method to update the prices of each item in a table with new data. Needs to accept a table name as a
#  parameter and the sku.

if __name__ == '__main__':
    connect()
    update_csvs()
    close()
