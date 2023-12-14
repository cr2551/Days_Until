"""
Pick a date in the future and calculate how much time there is left until said date.
You can save and delete entries. Those entries will have the option of being updated 
by the minute when the program is running.
Create the ability to set reminders and alerts when there are x days left for a given entry.

"""

import tkinter as tk
from tkinter import ttk
import ttkthemes
import csv
from tkcalendar import Calendar, DateEntry
import datetime
import random
from functools import partial

future = None

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
    text = f"{days_left} days until {event_name}"
    days_label.config(text=text)
    


def save_date():
    global future
    global dates_dict
    event_name = cal_event.get()
    print(future)
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
        row = {} # fallback val in case file is empty
        for row in csvreader:
            pass
        print(row)
        return row

def update_dates():
    # loop through the widgets in the parent widget and destroy them, then put the updated dates.
    for widget in entries_frame.winfo_children():
        widget.destroy()
    print_dates()

def delete_entry(entry_key):
    global dates_dict
    print(entry_key)
    dates_dict.pop(entry_key)
    print(dates_dict)
    with open('dates.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(dates_dict.keys())
        writer.writerow(dates_dict.values())
    # print_dates()
    update_dates()




def print_dates():
    global dates_dict
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
        del_btn = ttk.Button(entry_frame, text=f'delete {k}', command=partial(delete_entry, k))

        days_label.pack(side='left')
        label.pack(anchor=tk.W, side='left', padx=5)
        del_btn.pack(side='left')
        entry_frame.pack()
        #new line 
        # new_line = ttk.Label(entries_frame, text='')
        # new_line.pack()
    
    finished_label = tk.Label(root, text="finished loading")
    finished_label.pack()




root = tk.Tk()
root.title("Tkinter Intro")

style = ttkthemes.ThemedStyle(root)
style.set_theme('plastik')

top_frm = ttk.Frame(root, padding=15)
top_frm.pack()



header = ttk.Label(top_frm, text="Days Until", font=(18))
header.pack(pady=8)

load_dates_button = ttk.Button(top_frm, text="load", command=print_dates)
# load_dates_button.pack()

date_input_frm = ttk.Frame(top_frm, padding=8)
cal_event = ttk.Entry(date_input_frm)
cal_event.pack(side='left', padx=10)

date_picker = DateEntry(date_input_frm)
date_picker.pack(side='right')
date_input_frm.pack()

calc_days_btn = ttk.Button(top_frm, text="calculate days", command=calc_days)
calc_days_btn.pack(pady=8)

entries_frame = ttk.Frame(top_frm, padding=5)
entries_frame.pack()

dates_dict = load_dates() # load dates automatically
print_dates()

save_button = ttk.Button(top_frm, text='save Date', command=save_date)


quit_button = ttk.Button(top_frm, text='Quit', command=root.destroy)
quit_button.pack(side='bottom')
save_button.pack(side='bottom', pady=0)

root.mainloop()