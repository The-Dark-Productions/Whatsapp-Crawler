from selenium import webdriver

driver = webdriver.Chrome()
print(str(driver.command_executor._url))
print(str(driver.session_id))