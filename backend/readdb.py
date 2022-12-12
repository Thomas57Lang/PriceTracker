import dbconnect
from psycopg2 import sql
from psycopg2.extras import RealDictCursor


# Selects all the rows from the specified table and returns it as a list.
def read_db(table_name: str):
    dbconnect.connect()
    cur = dbconnect.conn.cursor(cursor_factory=RealDictCursor)

    # SELECT * FROM public."{table_name}"
    # ORDER BY "itemSKU" ASC

    query = sql.SQL("SELECT * FROM public.{tn}").format(
        tn=sql.Identifier(table_name)
    )

    cur.execute(query)
    data = cur.fetchall()

    cur.close()
    dbconnect.close()

    return data


# Selects the specific item from the specified table.
def read_item_db(table_name: str, item_sku: str):
    dbconnect.connect()
    cur = dbconnect.conn.cursor(cursor_factory=RealDictCursor)

    # SELECT * FROM public."{table_name}}"
    # WHERE "itemSKU" = '{sku}';

    query = sql.SQL("SELECT * FROM public.{tn} WHERE {itemsku} = ({sku})").format(
        tn=sql.Identifier(table_name),
        itemsku=sql.Identifier("itemSKU"),
        sku=sql.Literal(item_sku)
    )

    cur.execute(query)
    data = cur.fetchall()

    cur.close()
    dbconnect.close()

    return data
