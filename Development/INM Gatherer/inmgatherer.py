import pandas as pd
import os
import glob
import csv
import sys
import tkMessageBox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import EasyDialogs

# provide geckodriver path
geckopath = os.getcwd()
os.environ["PATH"] += os.pathsep + geckopath

username = EasyDialogs.AskString("Username :")
password = EasyDialogs.AskPassword("Password :")

if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys.executable) + "/*.xlsx"
elif __file__:
    script_dir = os.path.dirname(__file__) + "/*.xlsx"

xclname = glob.glob(script_dir)

table = pd.read_excel(xclname[0],
                      sheetname="Tickets not updated Details",
                      header=6)
a = 0
ticketno = []
before = []
for x in table['Ticket Number']:
    ticketno.append(x)

for x in table['Current Status']:
    before.append(x)
gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), 'geckodriver'))

driver = webdriver.Firefox(executable_path=gecko + '.exe')
driver.get("https://websso.t-systems.com/tsviper/incident/show/id/" + ticketno[0])

WebDriverWait(driver, 40).until(
    ec.presence_of_element_located((By.NAME, 'username')))

username2 = driver.find_elements_by_name('username')[1]
username2.send_keys(username)

username2 = driver.find_elements_by_name('password')[1]
username2.send_keys(password)

driver.find_elements_by_class_name('Button')[2].click()

status = []
times = []

for x in ticketno:
    driver.find_element_by_xpath("//select[@name='resource']/option[text()='Incident ID']").click()
    inputss = driver.find_element_by_xpath("//div[@id='search-box']/input[@name='value']")
    inputss.send_keys(x)
    abc = driver.find_element_by_xpath("//input[@type='submit']").click()
    WebDriverWait(driver, 40).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'inner')))

    statuses = driver.find_elements_by_class_name('inline-block-list')[0].find_elements_by_tag_name("li")[
        12].find_elements_by_tag_name("span")[1]

    status.append(statuses.text)
    timer = driver.find_elements_by_class_name('inline-block-list')[0].find_elements_by_tag_name("li")[
        8].find_elements_by_tag_name("span")[1]

    times.append(timer.text)

fl = open("illecsvupdate.csv", 'wb+')
mycsv = csv.writer(fl)
mycsv.writerow(["INM NO", "BEFORE", "AFTER", "LAST UPDATED"])

for x in range(len(ticketno)):
    tmp = []
    for y in [ticketno, before, status, times]:
        tmp.append(y[x])
    mycsv.writerow(tmp)

fl.close()
driver.quit()

tkMessageBox.showinfo("CSV Updates", "CSV file created and crawling complete")
