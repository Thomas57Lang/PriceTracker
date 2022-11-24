import dbconnect
from psycopg2 import sql


def insert_db(table_name, sku):
    dbconnect.connect()
    cur = dbconnect.conn.cursor()
    # INSERT INTO "table_name" ("itemSKU")
    # VALUES (sku);
    query = sql.SQL("INSERT INTO {tn} ({itemsku}) VALUES ({sku})").format(
        tn=sql.Identifier(table_name),
        itemsku=sql.Identifier("itemSKU"),
        sku=sql.Literal(sku)
    )
    cur.execute(query)
    dbconnect.conn.commit()
    cur.close()
    dbconnect.close()
