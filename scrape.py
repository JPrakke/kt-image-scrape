from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import os

issue_csv = os.path.join('.'+'/Data', 'issue.csv')

temp_part = 'RT-WARRIOR-30-10-14'
url = f'https://ktperformance.net/search.html?q={temp_part}'
print(url)
# reads csv and pulls partnumber to search in scrape
with open(issue_csv) as csvfile:
    read_csv = csv.reader(csvfile, delimiter=',')
    next(read_csv)
    part_number = []
    for row in read_csv:
        part = row[0]
        part_number.append(part)

option = webdriver.ChromeOptions()
option.add_argument(' - incognito')

browser = webdriver.Chrome('./chromedriver', chrome_options=option)
browser.get(url)

timeout = 100

try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH,"//img[@class='lazyload']")))
    print("timeout Passed")
except TimeoutException:
    print('Timed out on page load')
    browser.quit()