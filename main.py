import time
from whatsapp_helper import WhatsApp


wa = WhatsApp()
wa.open_chat_with_search('Mummy')
while True:
    if wa.check_if_online():
        print("Person is online")
    else:
        print("Person is not online")
    time.sleep(5)
