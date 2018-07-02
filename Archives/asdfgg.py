import os
import sys

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver

# Set the MOZ_HEADLESS environment variable which casues Firefox to start in headless mode.
os.environ['MOZ_HEADLESS'] = '1'

# Select your Firefox binary.
binary = FirefoxBinary('C:\\Program Files(x86)\\Mozilla Firefox\\firefox.exe', log_file=sys.stdout)

# Start selenium with the configured binary.
driver = webdriver.Firefox(firefox_binary=binary)

# Visit this webpage.
driver.get("https://intoli.com/blog/running-selenium-with-headless-firefox/")

