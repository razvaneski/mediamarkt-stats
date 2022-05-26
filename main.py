from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
import matplotlib.pyplot as plt


def get_data():
    link = 'https://www.mediamarkt.de/de/category/ersatzklingen-rasierer-zubeh%C3%B6r-164.html'

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(link)

    time.sleep(1.5)

    # for i in range(1, 9):
    #     driver.execute_script("window.scrollTo(0, " + str(i) + " * document.body.scrollHeight/10)")
    #     time.sleep(1)

    product_list = driver.find_elements(by=By.CSS_SELECTOR, value="[data-test='mms-search-srp-productlist-item']")
    l = []

    for product in product_list:
        product_name = product.find_element(by=By.CSS_SELECTOR, value="[data-test='product-title']")\
            .get_attribute("innerText")
        price_text = str(product.find_element(by=By.CSS_SELECTOR, value="[data-test='product-price']")
                         .get_attribute("innerText")
                         .encode('unicode-escape')).split('\\\\n')

        try:
            product_price = float(price_text[3])
        except:
            product_price = float(price_text[1])
        d = dict()
        d['Name'] = product_name
        d['Price'] = product_price
        l.append(d)

    driver.quit()
    # print(l)
    return pd.DataFrame(l)


df = ""
while True:
    print('''
      [a]. Retrieve data
      [b]. Create product graph
      [c]. Display product matrix
      [d]. Save data to Excel (products.xlsx)
      [e]. Exit
      ''')
    choice = input("Please enter a choice: ")

    if choice == 'a':
        print('Start downloading data')
        df = get_data()
        print('Done')
    elif choice == 'b':
        while True:
            try:
                df_aux = df.set_index('Name')
                df_aux['Price'].plot.barh()

                plt.show()
                break
            except:
                df = get_data()
    elif choice == 'c':
        while True:
            try:
                print(df)
                break
            except:
                df = get_data()

    elif choice == 'd':
        while True:
            try:
                df.to_excel("products.xlsx")
                break
            except:
                df = get_data()
    elif choice == 'e':
        print("That's it!")
        break
