import tkinter as tk
from tkcalendar import DateEntry
import datetime
import threading
import time
import subprocess

class CalendarEvent:
    def __init__(self, title, event_time, reminder_time):
        self.title = title
        self.event_time = event_time
        self.reminder_time = reminder_time

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar App")

        self.events = []

        # GUI Components
        self.title_entry = tk.Entry(root, width=30)
        self.event_time_entry = DateEntry(root, width=30)
        self.reminder_time_entry = tk.Entry(root, width=30)
        self.add_event_button = tk.Button(root, text="Add Event", command=self.add_event)
        self.event_listbox = tk.Listbox(root, width=40, height=10)
        self.quit_button = tk.Button(root, text="Quit", command=self.root.destroy)
        
        self.spinbox = tk.Spinbox(root, from_=1, to=20, width=5)
        self.spinbox.pack(pady=6)

        # Pack GUI Components
        self.title_entry.pack(pady=5)
        self.event_time_entry.pack(pady=5)
        self.reminder_time_entry.pack(pady=5)
        self.add_event_button.pack(pady=5)
        self.event_listbox.pack(pady=10)
        self.quit_button.pack(pady=5)

        name = "***********************--=========== This is my python thread =========----------******************************"
        self.reminder_thread = threading.Thread(target=self.check_reminders, name=name)
        self.reminder_thread.daemon = True
        self.reminder_thread.start()
        # Start the reminder loop
        # self.check_reminders()

    def add_event(self):
        title = self.title_entry.get()
        title  = 'hi'
        # event_time = datetime.strptime(self.event_time_entry.get(), "%Y-%m-%d %H:%M:%S")
        event_time = self.event_time_entry.get_date()
        # reminder_time = datetime.strptime(self.reminder_time_entry.get(), "%Y-%m-%d %H:%M:%S")
        # remind_me_in = self.reminder_time_entry.get()
        # remind_me_in = int(remind_me_in)
        remind_me_in = 1
        reminder_time = event_time - datetime.timedelta(days=remind_me_in)


        new_event = CalendarEvent(title, event_time, reminder_time)
        self.events.append(new_event)

        # Update the listbox with event titles
        text = f"reminder set for {remind_me_in} days before event: {title}"
        self.event_listbox.insert(tk.END, text)

    def check_reminders(self):
        current_time = datetime.date.today()

        for event in self.events:
            time_difference = event.event_time - current_time # => timedelta object
            reminder_difference = event.reminder_time - current_time

            if 0 <= reminder_difference.total_seconds() <= 60:
                # print(f"Reminder: {event.title} is approaching in {time_difference.total_seconds()} seconds.")
                print(f"Reminder: {event.title} is approaching in {time_difference.total_seconds()} seconds.")
                subprocess.run(['notify-send', event.title])

            if time_difference.total_seconds() <= 0:
                print(f"Event: {event.title} is happening now!")

        # Schedule the next check after 10 seconds
        self.root.after(10000, self.check_reminders)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
