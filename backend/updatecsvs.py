from psycopg2 import sql
import pandas as pd
import csv
import dbconnect

# Connection variable created by psycopg2 handles the connection to the DB.
# conn = None

# get_skus() Run a sql query to collect the SKUs from a particular table then outputs that in a CSV.
# Parameter: table_name - Name of the table to run the query on.
# noinspection PyUnresolvedReferences
def get_skus(table_name):
    localconn = dbconnect.conn
    cur = localconn.cursor()
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


# get_table_csvs() Runs a SQL query to select all the tables from the public schema. It then updates the tables.csv.
# noinspection PyUnresolvedReferences
def get_table_csvs():
    localconn = dbconnect.conn
    cur = localconn.cursor()

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


# update_csvs() Uses get_table_csvs() to update the tables.csv and then iterates through the file.
# For each row in tables.csv check some edge cases and then call get_skus() to update the respective csvs.
# noinspection PyUnresolvedReferences
def update_csvs():
    dbconnect.connect()
    # Update the tables csv.
    # For each table call get_skus and update the csv that the web scrapers will use.
    # Utilize try except block to handle failures.
    get_table_csvs()

    f = open('tables.csv')
    csvreader = csv.reader(f)

    for row in csvreader:
        if (row[0] != 'Item') & (row[0] != 'table_name'):
            # noinspection PyBroadException
            try:
                get_skus(row[0])
            except:
                print("An exception was thrown. Please check table: " + row[0])

    f.close()
    dbconnect.close()


if __name__ == '__main__':
    update_csvs()
