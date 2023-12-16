"""
Pick a date in the future and calculate how much time there is left until said date.
You can save and delete entries. Those entries will have the option of being updated 
by the minute when the program is running.
Create the ability to set reminders and alerts when there are x days left for a given entry.

"""

import tkinter as tk
from tkinter import ttk
import ttkthemes
# import notify2
import csv
import json
from tkcalendar import Calendar, DateEntry
import datetime
import random
from functools import partial
import subprocess
import os

future = None

# dates_file = 'none.csv'
# dates_file = 'mine.csv'
dates_file = 'dates.csv'


def calc_days():
    global future
    today = datetime.date.today()
    # get_date() method returns the date as a datetime object
    future = date_picker.get_date()
    print(future)
    days_left = future - today
    event_name = cal_event.get()
    days_label = tk.Label(root, text=days_left)
    days_label.pack()
    if not event_name or event_name == placeholder_text:
        event_name = future
    text = f"{days_left} days until {event_name}"
    days_label.config(text=text)
    

def save_date():
    global future
    global dates_dict
    event_name = cal_event.get()
    print(future)
    if not event_name or event_name == placeholder_text:
        event_name = random.randint(0,100)
    today = datetime.date.today()
    # don't let falsy values be stored
    if future:
        dates_dict[event_name] = str(future)

    with open(dates_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(dates_dict.keys())
        writer.writerow(dates_dict.values())
    
    update_dates(dates_dict)
        



def load_dates():
    try:
        with open(dates_file, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            row = {} # fallback val in case file is empty
            for row in csvreader:
                pass
            return row
    except FileNotFoundError as e:
        with open(dates_file, 'x') as file:
            pass
        return {} # empty dictionary for dates_dict var

def update_dates(dates_dict):
    # loop through the widgets in the parent widget and destroy them, then put the updated dates.
    for widget in entries_frame.winfo_children():
        widget.destroy()
    print_dates(dates_dict)

def delete_entry(entry_key):
    global dates_dict
    dates_dict.pop(entry_key)
    with open(dates_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(dates_dict.keys())
        writer.writerow(dates_dict.values())
    # print_dates()
    update_dates(dates_dict)


def order_by():
    global dates_dict
    global current_order
    # flip through the different orderings
    # 'none' is the order the entries were added.
    if current_order == 'none':
        current_order = 'desc'
        rev = False
    elif current_order == 'desc':
        current_order = 'asc'
        rev = True
    elif current_order == 'asc':
        current_order = 'none'
        update_dates(dates_dict)
        return
    

    today = datetime.date.today()

    def str_to_days(item: tuple):
        v = item[1]
        date = datetime.datetime.strptime(v, "%Y-%m-%d").date()
        days_left = date - today
        days_left = days_left.days
        return days_left
        # new_dict['k'] = days_left
    sorted_dict = dict(sorted(dates_dict.items(), key=str_to_days, reverse=rev))
    update_dates(sorted_dict)


# there is some repetition here that needs to be eliminated.
def add_reminder(key, spinvar):
    # remind again when there is 'new_reminder' days left
    print(spinvar.get())
    new_reminder = int(spinvar.get())
    try:
        with open('reminders.json', 'r') as reminders:
            rem = reminders.read()
            if not rem:
                rem = {}
            else:
                rem = json.loads(rem)

        if key not in rem:
            rem[key] = {}
        
        rem[key]['date'] = dates_dict[key]
        rem[key]['reminders'] = new_reminder
    except FileNotFoundError as e:
        label = tk.Label(top_frm, text=e)
        # label.pack()
        rem = {}
        rem[key] = {}
        rem[key]['date'] = dates_dict[key]
        rem[key]['reminders'] = new_reminder

    with open('reminders.json', 'w') as reminders:
        reminders_dump = json.dump(rem, reminders)
  
     



def print_dates(dates_dict):
    # global dates_dict
    today = datetime.date.today()
    if not dates_dict:
        return
    for k, v in dates_dict.items():
        future = datetime.datetime.strptime(v, "%Y-%m-%d").date()
        days_left = future - today # return a datetime.timedelta object => 12 days, 0:00:00
        days_left = days_left.days
        text = f"days until {k}, {future}"
        # text = f"{days_left} days until {k}, {future}"

        entry_frame = ttk.Frame(entries_frame, padding=4)
        days_label = ttk.Label(entry_frame, text=days_left, foreground='blue')
        label = ttk.Label(entry_frame, text=text)
        del_btn = ttk.Button(entry_frame, text=f'delete', command=partial(delete_entry, k))
        # spinbox for selecting when to remind
        # assoaciate with a StringVar to pass that value to the partial function so that the spinbox is assocaited with the button
        spinbox_var = tk.StringVar()
        spinbox = ttk.Spinbox(entry_frame, from_=1, to=20, width=4, textvariable=spinbox_var)
        add_reminder_btn = ttk.Button(entry_frame, text='add reminder', command=partial(add_reminder, k, spinbox_var))



        days_label.pack(side='left')
        label.pack(anchor=tk.W, side='left', padx=8)
        del_btn.pack(side='left', padx=5)
        spinbox.pack(side='left', padx=3)
        add_reminder_btn.pack(side='left')
        entry_frame.pack()
    

def notify_func():
    # notify2 needs dbus, so you need to be running a desktop environment like GNOME or KDE
    # notify2.init("tkinter app")
    # notification = notify2.Notification('HEllo!', 'this is a message')
    # notification.show()
    title = 'hi'
    message = 'hello world'
    subprocess.run(['notify-send', title, message])


# functions for entry placeholder
def on_entry_focus_in(event):
    if cal_event.get() == placeholder_text:
        cal_event.delete(0, tk.END)
        cal_event.configure(show='')
        cal_event.configure(foreground='black')

def on_entry_focus_out(event):
    if cal_event.get() == '':
        cal_event.insert(0, placeholder_text)
        cal_event.configure(foreground='gray')





root = tk.Tk()
root.title("Days Until")

style = ttkthemes.ThemedStyle(root)
style.set_theme('plastik')

top_frm = ttk.Frame(root, padding=15)
top_frm.pack()

current_order = 'none'

header = ttk.Label(top_frm, text="Days Until", font=(18))
header.pack(pady=8)

load_dates_button = ttk.Button(top_frm, text="load", command=print_dates)
# load_dates_button.pack()

date_input_frm = ttk.Frame(top_frm, padding=8)
cal_event = ttk.Entry(date_input_frm)
cal_event.pack(side='left', padx=10)
placeholder_text = "Enter event name"
cal_event.insert(0, placeholder_text)
cal_event.configure(foreground='gray')
cal_event.bind("<FocusIn>", on_entry_focus_in)
cal_event.bind("<FocusOut>", on_entry_focus_out)

date_picker = DateEntry(date_input_frm)
date_picker.pack(side='right')
date_input_frm.pack()

calc_days_btn = ttk.Button(top_frm, text="calculate days", command=calc_days)
calc_days_btn.pack(pady=8)

entries_frame = ttk.Frame(top_frm, padding=5)
entries_frame.pack()

dates_dict = load_dates() # load dates automatically
print_dates(dates_dict)

notify_btn = ttk.Button(top_frm, text='notification', command=notify_func)
# notify_btn.pack()

order_button = ttk.Button(top_frm, text='sort', command=order_by)
order_button.pack(pady=3)

save_button = ttk.Button(top_frm, text='save Date', command=save_date)


quit_button = ttk.Button(top_frm, text='Quit', command=root.destroy)
quit_button.pack(side='bottom', pady=3)
save_button.pack(side='bottom', pady=3)

root.mainloop()