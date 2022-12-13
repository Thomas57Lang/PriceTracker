from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import dbconnect
from psycopg2 import sql

tableName = 'ASIItem'


# noinspection PyBroadException
def asi_price_grabber(sku_list):
    driver = webdriver.Chrome(
        service=ChromeService(executable_path='/backend/chromedriver'))

    driver.get("https://www.asipartner.com/partneraccess/Auth/Login.aspx?ReturnUrl=%2fpartneraccess%2fdefault.aspx")

    title = driver.title
    assert title == "ASI Partner Access"

    driver.implicitly_wait(0.5)

    text_box = driver.find_element(by=By.NAME, value="username")
    password_box = driver.find_element(by=By.NAME, value="password1")
    submit_button = driver.find_element(by=By.NAME, value="ctl00$ctl00$main$main$ctl00$Logon")

    # Login using credentials below
    f = open('asi.txt')
    lines = f.read().splitlines()
    f.close()

    text_box.send_keys(lines[0])
    password_box.send_keys(lines[1])

    submit_button.click()

    # Establish connection to database.
    dbconnect.connect()
    #localconn = dbconnect.conn
    cur = dbconnect.conn.cursor()

    try:
        for x in sku_list:
            search_box = driver.find_element(by=By.ID, value="ctl00_ctl00_ctl00_main_main_proSearch_KEY")
            search_button = driver.find_element(by=By.ID, value="btnSearch")
            search_box.send_keys("\uE005")
            search_box.send_keys(x)
            search_button.click()
            sku = "item" + str(x)[2:8]
            itemsku = str(x)[2:8]
            item = driver.find_element(by=By.ID, value=sku)
            original_string = item.text
            split_string = original_string.split("\n")
            # price = split_string.index("Price:")
            priceIndex = split_string.index("Price:")
            price = float(split_string[priceIndex + 1][1:])
            # inventory = item.find_element(by=By.CLASS_NAME, value="inventory")
            # inv_text = inventory.find_element(by=By.TAG_NAME, value="ul")
            # current_inventory = int(inv_text.text)
            current_inventory = 0
            insert_db(cur, itemsku, price, current_inventory)
            # Insert into tableName
            # print("SKU: " + str(x)[2:8])
            # print(split_string[price] + " " + split_string[price + 1])
            # print("Current Inventory: \n" + current_inventory + "\n")
    except:
        print("Exception thrown while gathering prices from ASI.")
    driver.quit()
    dbconnect.conn.commit()
    cur.close()
    dbconnect.close()


def insert_db(cur, sku, price, stock):
    # UPDATE "ASIItem"
    # SET price = price , stock = inventory
    # WHERE "itemSKU" = sku;
    query = sql.SQL("UPDATE {tn} SET price = %s , stock = %s WHERE {itemSKU} = {sku};").format(
        tn=sql.Identifier(tableName),
        itemSKU=sql.Identifier("itemSKU"),
        sku=sql.Literal(sku)
    )
    cur.execute(query, [price, stock])
