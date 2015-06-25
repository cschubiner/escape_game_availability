from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import json

dates = dict()

def saveAndQuit():
    print 'Quitting scraper...'
    with open('room_escape_dates.json','w') as j:
        json.dump(dates, j)
    browser.quit()
    exit()

browser = webdriver.Firefox()
browser.get('https://www-152h.bookeo.com/bookeo/b_31529FAT6N14529F4F5C9_start.html?inwidget=true&type=31523Y7JCW14D21721B49&a=31529FAT6N14529F4F5C9/')
browser.implicitly_wait(3)

# assert 'Yahoo' in browser.title
while True:
    print len(dates)
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cbtce_datarow")))
    except:
        print 'GG'
        saveAndQuit()

    date = None
    trs = browser.find_element_by_id('cbtce_casual').find_elements_by_css_selector('tr')
    if len(trs) == 0:
        break
    for tr in trs:
        if 'cbtce_DateHeader' in tr.get_attribute('class'):
            td = tr.find_element_by_css_selector('td')
            date = list()
            dates[td.text.strip()] = date
        elif 'cbtce_datarow' in tr.get_attribute('class'):
            eventTime, event, available, total = tr.find_elements_by_xpath('td')[:4]
            date.append({'eventTime':eventTime.text.strip(), 'event':event.text.strip(), 'available':available.text.strip(), 'total':total.text.strip()})

    try:
        browser.find_element_by_css_selector('#_buttonNext').find_element_by_css_selector('.smallbRight').click()
    except NoSuchElementException, e:
        break

    browser.implicitly_wait(5)
    time.sleep(3)

print dates
saveAndQuit()
