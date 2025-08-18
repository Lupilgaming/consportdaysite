from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_binary_path = "<OSPATH to chrome binary>"

# Create ChromeOptions and set the binary path
options = Options()
options.binary_location = chrome_binary_path

service = webdriver.ChromeService(executable_path="<OSPATH to downloaded driver binary>")
driver = webdriver.Chrome(service=service, options=options)

#driver = webdriver.Chrome()
driver.get('https://strava.com/')


driver.quit()
