import time
from selenium import webdriver
from enum import Flag, auto
import pickle
import threading


class Page(Flag):
    """Enum to show which interface is currently displayed"""
    SIGN_IN = auto()
    LANDING = auto()
    PERSONAL_CHAT = auto()
    GROUP_CHAT = auto()
    PROFILE_PHOTO = auto()
    GROUP_INFO = auto()
    CONTACT_INFO = auto()
    SELF_PROFILE_INFO = auto()


class WhatsApp:
    """Class to access and handle operations in whatsapp web"""
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://web.whatsapp.com")
        self.page = Page.SIGN_IN
        print("Please sign in")
        while not self.is_signed_in():
            time.sleep(1)
        print("Signed in")
        self.page = Page.LANDING

    def is_signed_in(self):
        try:
            self.driver.find_element_by_class_name('_3q4NP')
            return True
        except:
            return False

    def open_chat_with_search(self, chat_name):
        search_box = self.driver.find_element_by_class_name('jN-F5')
        search_box.send_keys(chat_name)
        for i in range(4):
            time.sleep(2)
            try:
                contacts = self.driver.find_elements_by_class_name('_2wP_Y')
                for contact in contacts:
                    try:
                        style = contact.get_attribute('style')
                        if style.split(sep=';')[2].split(sep=':')[1] == " translateY(72px)":    # To get first element
                            contact.click()
                            print("Chat found")
                            self.page = Page.PERSONAL_CHAT
                            return
                    except:
                        pass
            except:
                pass
        print("Chat not found")

    def check_if_online(self):
        assert self.page & Page.PERSONAL_CHAT == Page.PERSONAL_CHAT
        try:
            if self.driver.find_element_by_xpath("//div[@class='_3sgkv Gd51Q']").text == "online":
                return True
            else:
                return False
        except:
            return False

    def observe_online_activity(self, interval, file_path, logging=False):
        record = {}
        for i in range(int(86400 / interval)):
            current_time_sec = int(time.time())
            current_time = time.localtime()
            if self.check_if_online():
                if logging:
                    print("{0}:{1}:{2} - online".
                          format(current_time.tm_hour, current_time.tm_min, current_time.tm_sec))
                is_online = True
            else:
                if logging:
                    print("{0}:{1}:{2} - not online".
                          format(current_time.tm_hour, current_time.tm_min, current_time.tm_sec))
                is_online = False
            record[current_time_sec] = is_online
            thread1 = threading.Thread(target=dump_record, args=[record, file_path])
            thread1.start()
            time.sleep(interval)


def dump_record(record, file_path):
    with open(file_path, "wb") as file:
        pickle.dump(record, file)

# pg = Page.LANDING
# print(pg)
# print(type(pg))
# pg = pg | Page.SELF_PROFILE_INFO
# print(pg)
# st = pg & Page.LANDING
# print(st)
