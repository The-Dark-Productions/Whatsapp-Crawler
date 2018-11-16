import pickle
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta


def get_formatted_record(record):
    keys = [entry for entry in record.keys()]
    values = [entry for entry in record.values()]
    return keys, values


def visualise_record(filename, interval, tick_minutes):
    with open(filename, "rb") as file:
        record = pickle.load(file)
    timestamps, values = get_formatted_record(record)
    timestamps_local = [time.localtime(ts) for ts in timestamps]
    x_labels = ["{0}:{1}:{2}".format(ts.tm_hour, ts.tm_min, ts.tm_sec) for ts in timestamps_local]
    plt.plot(x_labels, values)
    plt.xticks(ticks=[x for x in range(0, len(timestamps), int(60/interval*tick_minutes))])
    plt.show()
    plt.close()


def analyze_record(filename):
    with open(filename, "rb") as file:
        record = pickle.load(file)
    timestamps, values = get_formatted_record(record)
    sessions = []
    total_duration = 0
    session_ongoing = False
    session_start_time = timestamps[0]
    for i in range(len(timestamps)):
        if values[i]:
            if not session_ongoing:
                session_ongoing = True
                session_start_time = timestamps[i]
        if not values[i] or i == len(timestamps)-1:
            if session_ongoing:
                session_ongoing = False
                total_duration += timestamps[i] - session_start_time
                local_start_time = time.localtime(session_start_time)
                local_end_time = time.localtime(timestamps[i])
                local_duration = datetime(1, 1, 1) + timedelta(seconds=timestamps[i] - session_start_time)
                sessions.append({"Start time": "{0}:{1}:{2}".
                                format(local_start_time.tm_hour, local_start_time.tm_min, local_start_time.tm_sec),
                                 "End time": "{0}:{1}:{2}".
                                format(local_end_time.tm_hour, local_end_time.tm_min, local_end_time.tm_sec),
                                 "Duration": "{0}:{1}:{2}".
                                format(local_duration.hour, local_duration.minute, local_duration.second)})
    local_total_duration = datetime(1, 1, 1) + timedelta(seconds=total_duration)
    local_total_observed = datetime(1, 1, 1) + timedelta(seconds=timestamps[len(timestamps)-1] - timestamps[0])
    print("\nTime observed - {0}:{1}:{2}".
          format(local_total_observed.hour, local_total_observed.minute, local_total_observed.second))
    print("\nTotal duration - {0}:{1}:{2}".
          format(local_total_duration.hour, local_total_duration.minute, local_total_duration.second))
    print("\nNumber of sessions - {0}".format(len(sessions)))
    print("\n\nSessions:")
    for i, session in enumerate(sessions):
        print("\n"+str(i+1)+".")
        print("Start time - {0}".format(sessions[i]["Start time"]))
        print("End time - {0}".format(sessions[i]["End time"]))
        print("Duration - {0}".format(sessions[i]["Duration"]))
