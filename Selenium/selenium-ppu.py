import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

r_clean = re.compile(r'[^\d,]+')

options = Options()
options.add_argument('--headless')  # běží bez GUI
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

from_iata = 'VIE'
to_iata = 'TFS'
departure_date = '2025-04-03'
return_date = '2025-04-08'


# url = f'https://www.ryanair.com/cz/cs/booking/home/{from_iata}/{to_iata}/{departure_date}/{return_date}/1/0/0/0'
# https://www.wizzair.com/cs-cz/booking/select-flight/VIE/TFS/2025-04-03/2025-04-08/1/0/0/null
#url = f'https://www.wizzair.com/cs-cz/booking/select-flight/{from_iata}/{to_iata}/{departure_date}/{return_date}/1/0/0/null'
url = f'https://www.pelikan.cz/cs/akcni-letenky/'
driver.get(url)

time.sleep(5)

try:
    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "codeblocks-reject-cookies"))
        )
        print("Klikám na 'Odmítnout všechny cookies'...")
        cookie_button.click()
    except:
        print("Tlačítko 'Odmítnout cookies' se nezobrazilo.")

    time.sleep(5)
    driver.save_screenshot("screenshot.png")

    # test if there is departure element
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "calendar-item-info-action"))
    )

    print("Loaded...")

    items = driver.find_elements(By.CLASS_NAME, "calendar-item-info-action")

    print(f"Načteno {len(items)} akcí")

    for i in items:
        departure = i.find_elements(By.CLASS_NAME, "calendars-item-departure")
        arrival = i.find_elements(By.CLASS_NAME, "calendars-item-arrival")
        if departure and arrival:
            departure = departure[0].text.strip().split()[0]
            arrival = arrival[0].text.strip().split()[0]
        
        price = i.find_elements(By.CLASS_NAME, "calendars-item-price")
        currency = i.find_elements(By.CLASS_NAME, "calendars-item-currency")
        if price and currency:
            price = price[0].text
            currency = currency[0].text

        #print(f'Departure: {departure}, Arrival: {arrival}, Price: {price}')
        print(f'Price: {price} {currency}')

    # dprice = None
    # rprice = None

    # departure_price = driver.find_elements(By.XPATH, f'//button[@data-ref="{departure_date}"]/div[contains(@class, "date-item__price")]')
    # if departure_price:
    #     dprice = float(r_clean.sub('', departure_price[0].text).replace(',', '.'))
    #     print(dprice)

    # return_price = driver.find_elements(By.XPATH, f'//button[@data-ref="{return_date}"]/div[contains(@class, "date-item__price")]')
    # if return_price:
    #     rprice = float(r_clean.sub('', return_price[0].text).replace(',', '.'))
    #     print(rprice)
    
    # price = dprice + rprice

    # print(f'Price of flight from {from_iata} to {to_iata} on {departure_date} and return on {return_date} is {price} EUR.')


except Exception as e:
    print("Chyba při získávání dat:", e)

driver.quit()