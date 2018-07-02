
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait


def waiting(xpaths):
    wait(browser, 40).until(
        EC.presence_of_element_located((By.XPATH, xpaths)))


servername = "CAM-S-6314"
browser = webdriver.Chrome()
browser.get('https://t-rep.t-systems.com/2/search')

waiting("//input[@id='search-start-field']")
searchfield = browser.find_element_by_id('search-start-field')

browser.execute_script("arguments[0].setAttribute('value','%s')" % servername, searchfield)

browser.find_element_by_css_selector(".input-group-btn").click()

waiting("//div[@class='search-result-group-header']")

serverheader = browser.find_element_by_xpath(
    ' //*[@class="search-result-group-header"]/strong[text()="Server"]/../span[@class="label pull-right customer-1"]/../../div[@class="search-result-group-body"]/*/*')
serverheader.click()


wait(browser, 40).until(
    EC.presence_of_element_located((By.XPATH, '//*[@data-category-uid="40"]/a/span[text()="Application"]'))).click()

waiting('//*[contains(text(),"@SHELL.COM")]')
name = browser.find_elements_by_xpath('//*[contains(text(),"@SHELL.COM")]')

for x in name:
    print x.text
