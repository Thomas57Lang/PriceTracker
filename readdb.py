import dbconnect
from psycopg2 import sql
from psycopg2.extras import RealDictCursor



# Selects all the rows from the specified table and returns it as a list.
def read_db(table_name: str):
    dbconnect.connect()
    cur = dbconnect.conn.cursor(cursor_factory=RealDictCursor)

    # SELECT * FROM public."ASIItem"
    # ORDER BY "itemSKU" ASC

    query = sql.SQL("SELECT * FROM public.{tn} ORDER BY {itemsku} ASC").format(
        tn=sql.Identifier(table_name),
        itemsku=sql.Identifier("itemSKU")
    )

    cur.execute(query)
    data = cur.fetchall()

    cur.close()
    dbconnect.close()

    return data
