from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def asi_price_grabber(sku_list):
    driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()))

    driver.get("https://www.asipartner.com/partneraccess/Auth/Login.aspx?ReturnUrl=%2fpartneraccess%2fdefault.aspx")

    title = driver.title
    assert title == "ASI Partner Access"

    driver.implicitly_wait(0.5)

    text_box = driver.find_element(by=By.NAME, value="username")
    password_box = driver.find_element(by=By.NAME, value="password1")
    submit_button = driver.find_element(by=By.NAME, value="ctl00$ctl00$main$main$ctl00$Logon")

    # Login using credentials below

    text_box.send_keys("99150")
    password_box.send_keys("by99150tM")
    submit_button.click()

    for x in sku_list:
        search_box = driver.find_element(by=By.ID, value="ctl00_ctl00_ctl00_main_main_proSearch_KEY")
        search_button = driver.find_element(by=By.ID, value="btnSearch")
        search_box.send_keys("\uE005")
        search_box.send_keys(x)
        search_button.click()
        sku = "item" + str(x)[2:8]
        item = driver.find_element(by=By.ID, value=sku)
        original_string = item.text
        split_string = original_string.split("\n")
        price = split_string.index("Price:")
        inventory = item.find_element(by=By.CLASS_NAME, value="inventory")
        inv_text = inventory.find_element(by=By.TAG_NAME, value="ul")
        current_inventory = inv_text.text
        print("SKU: " + str(x)[2:8])
        print(split_string[price] + " " + split_string[price + 1])
        print("Current Inventory: \n" + current_inventory + "\n")

    driver.quit()

