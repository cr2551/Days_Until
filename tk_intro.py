"""
Pick a date in the future and calculate how much time there is left until said date.
You can save and delete entries. Those entries will have the option of being updated 
by the minute when the program is running.
Create the ability to set reminders and alerts when there are x days left for a given entry.
"""

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import csv
from tkcalendar import Calendar, DateEntry
import pickle



root = tk.Tk()
# root.geometry('300x200')
root.maxsize(400,400)
# root.wm_maxsize(400, 300)
root.title("Tkinter Intro")

style = ThemedStyle(root)
style.set_theme('plastik')


def on_button_click():
    label.config(text=entry.get())


top_frm = ttk.Frame(root, padding=10)
frm = ttk.Frame(top_frm, padding=10)
date_picker = DateEntry(frm)


label = ttk.Label(top_frm, text="Days Until", font=("Helvetica", 16) )

# label.grid(row=0, column=2)


entry = ttk.Entry(frm)
entry.insert(0, string='Event')
entry.config(foreground='gray')
# entry.grid(row=1, column=0)
# date_picker.grid(row=1, column=2)
entry.pack(side='left', padx=8, pady=10)
date_picker.pack(side='right')

top_frm.pack()
label.pack(pady=5)
frm.pack()




button = tk.Button(root, text="Click Me!", command=on_button_click)
# button.grid(row=2, column=1)
button.pack()

quit_button = ttk.Button(root, text='Quit', command=root.destroy)
quit_button.pack()

root.mainloop()