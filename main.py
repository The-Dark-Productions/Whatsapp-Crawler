import time
from selenium import webdriver

driver = webdriver.Chrome()

driver = webdriver.Remote(command_executor='http://127.0.0.1:52127', desired_capabilities={})
driver.session_id = '217937f19c321892ef8ff5eee3d35f9f'
print(str(driver.current_url))

while True:
    try:
        online = driver.find_element_by_xpath("//div[@class='_3sgkv Gd51Q']")
        print('The person is online')
        text = driver.find_element_by_xpath("//*[@id=\"main\"]/footer/div[1]/div[2]/div/div[2]")
        text.send_keys("This message is sent by python code automatically, which was waiting for you to come online !")
        send = driver.find_element_by_xpath("//*[@id=\"main\"]/footer/div[1]/div[3]/button")
        send.click()
        print("Message sent to the person")
        print("Terminating")
        break
    except:
        print('The person is NOT online')
    time.sleep(5)

