from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading

path = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(path)
mill_list = ['index0', 'million', 'billion', 'trillion', 'quadrillion', 'quintillion']

driver.get("https://orteil.dashnet.org/cookieclicker/")

def get_cookie_num(cookie_count):

        try:
            # Make List
            if '.' in cookie_count.text:
                cookie_list = cookie_count.text.split("\n")
                cookie_list[0] = cookie_list[0].replace(" cookies", "")
                cookie_list[1] = cookie_list[1].replace(" cookies", "")

            else:
                cookie_list = cookie_count.text.split(" ")
                cookie_list[0] = cookie_list[0].split('\n')[0]

            print(f"Raw Text: {cookie_count.text}")
            print(cookie_list)

            if(len(cookie_list) > 1):

                if cookie_list[1] in mill_list:

                    mill_int = millify(cookie_list[1])       
                    cookie_num = float(cookie_list[0]) * mill_int
            
                else:

                    cookie_num = int(cookie_list[0].replace(",", ""))
                    print(cookie_num)
            return cookie_num

        except:
            print('Something went wrong')
            return 0

def populate_store():
    store_dict = {}

    # Populate Store
    for x in range(20):

        product_name = "product" + str(x)
        product_price = "productPrice" + str(x)

        price = driver.find_element(By.ID, product_price).text

        if price != '':

            price = int(price)

        store_dict[x] = {"product" : product_name, "price" : price}
    
    return store_dict

def update_store(store, cookie_amount):
    print('store running')
    cookie_count = driver.find_element(By.ID, "cookies")

    while True:

        # Find, Buy and Update Best Products
        best_product = None
        best_price = 0
        cookie_amount = get_cookie_num(cookie_count)

        check_products = True
        for x,y in store.items():

            if check_products:
                new_price = driver.find_element(By.ID, "productPrice" + str(x)).text.replace(",", "")

                if new_price != '':
                    new_price_split = new_price.split(" ")

                    if len(new_price_split) > 1:

                        if new_price_split[1] in mill_list:

                            y['price'] = int(float(new_price_split[0]) * millify(new_price_split[1]))
                    
                    else:
                        y['price'] = int(new_price)
                    
                else:
                    check_products = False

            if new_price != '':
                    
                if (y['price'] > best_price) and (y['price'] < cookie_amount):

                    best_price = y['price']
                    best_product = y['product']

        if best_product != None:

                try:
                    product_to_buy = driver.find_element(By.ID, best_product)
                    product_to_buy.click()
                except:
                    print(f"Best Product: {best_product}")
                    print(f"Product to Buy: {product_to_buy}")

def buy_upgrades():

    while True:
        time.sleep(12)

        try:
            upgrade = driver.find_element(By.ID, 'upgrade0')
            upgrade.click()
        except:
            print("Failed to buy upgrade")

def click_cookie():
    print('cookie running')
    cookie = driver.find_element(By.ID, "bigCookie")

    while True:
        cookie.click()

def millify(target):

    index = mill_list.index(target)
    num = 10 ** ((index * 3) + 3)

    return num

def run():

    try:
        language = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "langSelect-EN"))
        )
        language.click()

        wait = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "bigCookie"))
        )
        time.sleep(2.5)

        store_dict = populate_store()
        threads(0, store_dict)

    finally:
        driver.quit()

def threads(cookie_count, store_dict):

    
    store_thread = threading.Thread(target=update_store, args=(store_dict, cookie_count))
    upgrade_thread = threading.Thread(target=buy_upgrades)

    click_threads = []
    for i in range(20):
        t = threading.Thread(target=click_cookie)
        click_threads.append(t)


    for i in click_threads:
        i.start()

    store_thread.start()
    upgrade_thread.start()

    for i in click_threads:
        i.join()

    store_thread.join()
    upgrade_thread.join()
    
    

run()
