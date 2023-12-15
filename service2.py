# Use this code if you want to create a systemd service.
# creating a daemon as in daemon.py will not work with systemd


import time
import subprocess
import datetime
import json


def main_program():
    while True:
        print("inside main program")
        subprocess.run(["notify-send", "this is daemon"])
        time.sleep(10)


def send_notif(days):
    subprocess.run(["notify-send", f"there is {days} days left"])


# check if we need to remind the user of  an upcoming event
events = {"xmas": {"date": "2023-12-25", "reminders": 10}}

# parse date
ev = events["xmas"]
event_date = datetime.datetime.strptime(ev["date"], "%Y-%m-%d").date()
today = datetime.date.today()
reminder = ev["reminders"]

delta = event_date - today
print(delta.days)
if delta.days == reminder:
    send_notif(delta.days)
