# Use this code if you want to create a systemd service.
# creating a daemon as in daemon.py will not work with systemd
# this works. If it stops working, the problem is related to something else.


import time
import subprocess
import datetime
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
reminders_path = os.path.join(script_dir, 'reminders.json')

def send_notif(event, days):
    """see man notify-send for more options"""

    subprocess.run(["notify-send", '-u', 'normal','-t', '10000', f"{event} is in {days} days"])


# check if we need to remind the user of  an upcoming event
# events = {"xmas": {"date": "2023-12-25", "reminders": 10}}


# the problem with this code is that it will continue issuing notifications every 10secs for the same events
# it would be better if it only did it once or every so often until the user takes an action
# I am thinking of deleting the reminder from the dictionary once the notification is issued.
while True:
    try:
        with open(reminders_path, 'r') as f:
            rem = f.read()
    except Exception as e:
        print('No reminders yet')
        print(e)
        exit(1)

# parse date
    reminders = json.loads(rem)
    for r in reminders.items():
        print(r)
        event_date = datetime.datetime.strptime(r[1]["date"], "%Y-%m-%d").date()
        today = datetime.date.today()
        reminder = r[1]["reminders"]

        delta = event_date - today
        # check if we need to issue a reminder
        if delta.days == reminder:
            event_name = r[0].upper()
            send_notif(event_name, delta.days)
            time.sleep(5)
    time.sleep(20)
