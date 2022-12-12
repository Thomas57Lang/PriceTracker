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


def insert_base_item(item_name: str, sku: str, table_name: str, part_num: str, description: str):
    asisku = ''
    ingramsku = ''
    if table_name == "ASIItem":
        asisku = sku
    elif table_name == "IngramItem":
        ingramsku = sku

    try:
        insert_db(table_name, sku)
    except:
        print("Item insert in vendor table. Duplicate may exist.")

    dbconnect.connect()
    cur = dbconnect.conn.cursor()

    # INSERT INTO public."Item"
    # ("itemName", "asiSKU", "ingramSKU", "partnum", "partdescription")
    # VALUES('test', '12345', '', '123-test', 'test item');

    query = sql.SQL("INSERT INTO public.{item} ({iname},{asi},{ingram},{part},{descrip}) VALUES ({invalue},"
                    "{asivalue},{ingramvalue},{partnumvalue},{descripvalue});").format(
        item=sql.Identifier("Item"),
        iname=sql.Identifier("itemName"),
        asi=sql.Identifier("asiSKU"),
        ingram=sql.Identifier("ingramSKU"),
        part=sql.Identifier("partnum"),
        descrip=sql.Identifier("partdescription"),
        invalue=sql.Literal(item_name),
        asivalue=sql.Literal(asisku),
        ingramvalue=sql.Literal(ingramsku),
        partnumvalue=sql.Literal(part_num),
        descripvalue=sql.Literal(description)
    )

    cur.execute(query)
    dbconnect.conn.commit()
    cur.close()
    dbconnect.close()


#insert_base_item("Surface Pro 7+", "8NU289", "IngramItem", "1N9-00001", "Microsoft Surface Pro 7+")
