#!/usr/bin/env python
# coding: utf-8

import csv
import os
import time
import datetime as dt
from datetime import date
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait


def get_date(data, writer):
    date_collect = dt.date.today()

    for WebElement in data:
        elementHTML = WebElement.get_attribute('outerHTML')
        elementSoup = bs(elementHTML, 'html.parser')

    soup = elementSoup

    tds = soup.findAll('div', {'class': 'ab-2062-time'})
    lst = []
    time_in = []
    time_out = []
    name = []
    for td in tds:
        inner_text = td.text
        strings = inner_text.split("\n")
        lst.extend([string for string in strings if string])
    for count, a in enumerate(lst):
        if count % 2 == 1:
            time_in.append(a)
        else:
            time_out.append(a)

    for each_div in soup.findAll('div', {'class': 'hdOp'}):
        na = each_div.text
        name.append(na)

    date = soup.findAll('div', {'class': 'ab-2062-date'})
    dat_ = []
    date_ = []
    date_today = []
    for count, td in enumerate(date):
        inner_text = td.text
        strings = inner_text.split("\n")
        if count % 2 == 0:
            dat_.append(strings[1])
        else:
            pass

    p = []
    pk = []
    for each_div in soup.findAll('div', {'class': 'price'}):
        price = each_div.text[1:10]
        p.append(price)
    for count, a in enumerate(p):
        strings = a.split("\n")
        if count % 2 == 1:
            pk.append(strings[0])
    for pr, nm, to, ti, d_ in zip(pk, name, time_out, time_in, dat_):
        out = [date_collect, pr, nm, to, ti, d_]
        writer.writerow(out)


def scrape():
    url = "https://www.directferries.co.uk/"
    s = Service('chromedriver')
    options = Options()
    options.headless = False
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=s, options=options)

    # loc="P&O Dover Calais"
    loc = input('Enter route_name: ')

    driver.get(url)
    time.sleep(1)

    # Click on one way
    single = driver.find_element(by=By.XPATH, value='//*[@id="dealfinder-wrapper"]/section[1]/label[2]')
    single.click()
    time.sleep(1)

    # Writing The Route Name
    route_name = driver.find_element(by=By.XPATH, value='//*[@id="route_outbound"]')
    route_name.send_keys(loc)
    time.sleep(1)

    # Clicking on Confirm button
    confirm_bttn = driver.find_element(by=By.XPATH, value='//*[@id="deafinder-submit"]')
    confirm_bttn.click()
    time.sleep(1)
# Select cookies
cookies_button = driver.find_element(By.XPATH, '//*[@id="df_cc_close"]')
cookies_button.click()
time.sleep(2)

# Click on consent button
consent_button = driver.find_element(By.XPATH, '//*[@id="journey_route_parent"]/div[2]/aside/ul/li[1]')
consent_button.click()

# Select calendar
calendar = driver.find_element(By.XPATH, '//*[@id="dealfinder-wrapper"]/section[2]')
ActionChains(driver).move_to_element(calendar).click(calendar).perform()
time.sleep(1)

# Confirm date
date_confirm = driver.find_element(By.XPATH, '//*[@id="deafinder-submit"]')
date_confirm.click()
time.sleep(1)

# Confirm time
time_confirm = driver.find_element(By.ID, 'deafinder-submit')
time_confirm.click()
time.sleep(2)

# Select car
car_button = driver.find_element(By.XPATH, '//*[@id="dealfinder-wrapper"]/section[4]/section[1]/ul[2]/li[3]/a')
car_button.click()
time.sleep(2)

# Select BMW car
car_type_button = driver.find_element(By.XPATH, '//*[@id="vehicle_type_2"]')
car_type_button.click()
time.sleep(2)

# Select car make
car_make_button = driver.find_element(By.ID, 'vehicle_make_outbound_2191')
car_make_button.click()
time.sleep(3)

# Select car model
car_model_button = driver.find_element(By.XPATH, '//*[@id="dealfinder-wrapper"]/aside/div/div[2]/fieldset[2]/ol/li[7]/label')
car_model_button.click()
time.sleep(2)

# Confirm car details
car_done_button = driver.find_element(By.XPATH, '//*[@id="dealfinder-wrapper"]/aside/footer/button')
car_done_button.click()

# Confirm details
details_confirm_button = driver.find_element(By.XPATH, '//*[@id="deafinder-submit"]')
details_confirm_button.click()
time.sleep(10)

# Iterate through dates and times
for date in [' 30 / 9', ' 28 / 10', ' 25 / 11', ' 30 / 12']:
    print('Working on date:', date)
    sp = str(date).split("/")
    year = 2023
    month = int(sp[1].strip()) - 1
    day = sp[0].strip()

    # Change search date
    change_search_date_button = driver.find_element(By.XPATH, '//*[@id="lnkChangeSearch"]')
    ActionChains(driver).move_to_element(change_search_date_button).click(change_search_date_button).perform()
    time.sleep(3)

    # Select new date
    new_date = driver.find_element(By.XPATH, '//*[@id="cal_out"]')
    ActionChains(driver).move_to_element(new_date).click(new_date).perform()
    time.sleep(3)

    # Update date and click
    a_element = driver.find_element(By.XPATH, '//a[@class="ui-state-default ui-state-active"]')
    td_element = a_element.find_element(By.XPATH, '..')
    driver.execute_script(f"arguments[0].setAttribute('data-month', '{month}')", td_element)
    driver.execute_script("arguments[0].textContent = arguments[1]", a_element, str(day))
    a_element.click()
    time.sleep(1)

   # select route and click on search button
    route_name = driver.find_element(by=By.XPATH, value='//*[@id="destination"]//option[@value="calais"]')
    route_name.click()
    search_button = driver.find_element(by=By.XPATH, value='//*[@id="searchButton"]')
    search_button.click()

    # select date and time and click on search button
    time.sleep(1)
    time_0 = driver.find_element(by=By.XPATH, value='//*[@id="timeOut"]')
    time_0.click()
    time_0_set = driver.find_element(by=By.XPATH, value='//select[@id="timeOut"]//option[@value=0]')
    time_0_set.click()

    time.sleep(1)
    new_date_confrim = driver.find_element(by=By.XPATH, value='//*[@id="btnSearch"]')
    new_date_confrim.click()
    time.sleep(1)

    time.sleep(5)
    for t in [6, 7, 8, 9, 10, 13, 14, 15, 16, 17, 20, 21, 22, 23]:
        print("Working on time: ", dat, "time:", t)
        data = driver.find_elements(by=By.ID, value="divQuotesContainer")
        get_date(data)
        done_t = driver.find_element(by=By.XPATH, value="//*[@id='lnkChangeSearch']")
        time.sleep(2)
        ActionChains(driver).move_to_element(done_t).click(done_t).perform()
        time.sleep(2)
        new_time = driver.find_element(by=By.XPATH, value='//*[@id="timeOut"]')
        ActionChains(driver).move_to_element(new_time).click(new_time).perform()
        new_time_set = driver.find_element(by=By.XPATH, value=f'//select[@id="timeOut"]//option[@value={t}]')
        new_time_set.click()
        new_time_submit = driver.find_element(by=By.XPATH, value='//*[@id="btnSearch"]')
        new_time_submit.click()
        time.sleep(5)

    print(route_name)
    
    
    
name='XXX.csv'
if os.path.isfile(fname):
    with open(fname, 'a', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        scrape()
else:
    with open(fname, 'a', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['data collection on', 'price', 'comp', 'outbound', 'reach', 'date'])
        scrape()
driver.close
