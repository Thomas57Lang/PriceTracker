import psycopg2
from psycopg2 import sql
import config
import csv


# TODO: Create a method that will grab the names of the tables from the CSV. This will be used in the main method.
# noinspection DuplicatedCode
def get_tables():
    f = open('tables.csv')
    csvreader = csv.reader(f)
    tables = []

    for row in csvreader:
        if (row[0] != 'Item') & (row[0] != 'table_name'):
            # noinspection PyBroadException
            try:
                tables.append(row[0])
            except:
                print("An exception was thrown. Please check table: " + row[0])

    f.close()
    return tables

# TODO: Create a method that takes the name of the table and passes that to the controller.

# TODO: Create a method to update the prices of each item in a table with new data. Needs to accept a table name as a
#  parameter and the sku.
