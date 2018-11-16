from whatsapp_helper import WhatsApp
import threading
import utils


interval = 5
record = {}
record_filepath = "record.dat"

wa = WhatsApp()
wa.open_chat_with_search('Dada')
online_activity_thread = threading.Thread(target=wa.observe_online_activity, args=[interval, record_filepath])
online_activity_thread.start()

while True:
    print("\nEnter your choice:")
    print("1. Visualize")
    print("2. Analyze")
    ch = int(input("->"))
    if ch == 1:
        tick_minutes = int(input("Distance between ticks in minutes: "))
        utils.visualise_record(record_filepath, interval, tick_minutes)
    elif ch == 2:
        utils.analyze_record(record_filepath)
