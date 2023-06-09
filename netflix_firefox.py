import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service


firefox_driver_path = "web_drivers/geckodriver-v0.33.0-win64/geckodriver.exe"
service = Service(executable_path=firefox_driver_path)

options = webdriver.FirefoxOptions()
options.add_argument("--start-maximized")

# Exclude switches for automation extension and enable developer mode
options.set_preference("dom.webdriver.enabled", False)
options.set_preference("useAutomationExtension", False)
options.set_capability("moz:webdriverClick", False)

driver = webdriver.Firefox(service=service, options=options)
driver.get("https://www.netflix.com")

while True:
    time.sleep(1)
