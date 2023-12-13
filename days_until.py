"""
Pick a date in the future and calculate how much time there is left until said date.
You can save and delete entries. Those entries will have the option of being updated 
by the minute when the program is running.
Create the ability to set reminders and alerts when there are x days left for a given entry.
"""

import tkinter as tk
from tkinter import ttk
import csv
from tkcalendar import Calendar, DateEntry
import datetime
import random

future = None

def calc_days():
    global future
    today = datetime.date.today()
    # get_date() method returns the date as a datetime object
    future = date_picker.get_date()
    days_left = future - today
    event_name = cal_event.get()
    days_label = tk.Label(root, text=days_left)
    days_label.pack()
    text = f"{days_left} days until {event_name}"
    days_label.config(text=text)
    


saved_dates = {}
def save_date():
    global future
    dates_dict = {}
    # read csv file
    with open('dates.csv', 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        row = None
        for row in csvreader:
            pass
        if row:
            dates_dict = row
    event_name = cal_event.get()
    if not event_name:
        event_name = random.randint(0,100)
    today = datetime.date.today()
    dates_dict[event_name] = future

    with open('dates.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(dates_dict.keys())
        writer.writerow(dates_dict.values())
        



def load_dates():
    with open('dates.csv', 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        row = None
        for row in csvreader:
            pass
        if row:
            dates_dict = row
        else: # is empty there is nothing to load
            return
        # print(csvreader)
        today = datetime.date.today()
        for k, v in dates_dict.items():
            future = datetime.datetime.strptime(v, "%Y-%m-%d").date()
            days_left = future - today
            text = f"{days_left} days until {k}"
            label = tk.Label(root, text=text)
            label.pack()
        finished_label = tk.Label(root, text="finished loading")
        finished_label.pack()

root = tk.Tk()
root.title("Tkinter Intro")


load_dates_button = tk.Button(root, text="load saved dates", command=load_dates)
load_dates_button.pack()


date_picker = DateEntry(root)
date_picker.pack()

cal_event = tk.Entry(root)
cal_event.pack()

calc_days_btn = tk.Button(root, text="calculate days!", command=calc_days)
calc_days_btn.pack()

save_button = tk.Button(root, text='save Date', command=save_date)
save_button.pack()

label = tk.Label(root, text=" ")
label.pack()


root.mainloop()