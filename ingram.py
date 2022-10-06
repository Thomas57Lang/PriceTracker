from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import url_matches
from selenium.webdriver.support.expected_conditions import url_contains


def ingram_price_grabber(sku_list):
    driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()))

    driver.get("https://usa.ingrammicro.com/Site/Home")

    driver.implicitly_wait(0.5)
    # title = driver.title
    # assert title == "ASI Partner Access"

    login_button = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(by=By.ID, value="loginBtn"))

    login_button.click()

    text_box = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(by=By.ID, value="okta-signin-username"))
    password_box = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(by=By.ID, value="okta-signin-password"))
    submit_button = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(by=By.ID, value="okta-signin-submit"))

    # Login using credentials below

    text_box.send_keys("thomas@nordicpc.com")
    password_box.send_keys("@Ingr4mM1cr0")
    submit_button.click()

    WebDriverWait(driver, timeout=15).until(url_matches("https://usa.ingrammicro.com/Site/Home"))

    for x in sku_list:
        search_box = driver.find_element(by=By.ID, value="searchBox_Global_v2")
        # search_button = driver.find_element(by=By.ID, value="btnSearch")
        search_box.send_keys("\uE005")
        search_box.send_keys(x)
        search_box.send_keys("\uE007")
        id = str(x)[2:8]
        # search_button.click()
        item = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="lstView-A300-" + id))
        price = item.find_element(by=By.ID, value="BBB_A300-" + id)
        WebDriverWait(price, timeout=10).until(lambda p: p.text != "Loading...")
        inventory = item.find_element(by=By.ID, value="AAA_A300-" + id)
        print("Price: " + price.text + "\n")
        print("Current Inventory: \n" + inventory.text + "\n")
    #     original_string = item.text
    #     split_string = original_string.split("\n")
    #     price = split_string.index("Price:")
    #     inventory = item.find_element(by=By.CLASS_NAME, value="inventory")
    #     inv_text = inventory.find_element(by=By.TAG_NAME, value="ul")
    #     current_inventory = inv_text.text
    #     print("SKU: " + str(x)[2:8])
    #     print(split_string[price] + " " + split_string[price + 1])
    #     print("Current Inventory: \n" + current_inventory + "\n")

    driver.quit()

# ingram_price_grabber()
