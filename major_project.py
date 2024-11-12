from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from tkcalendar import DateEntry
import ast
import threading
import time

class TODOApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reminder App")
        self.tasks = []
        self.root.configure(bg='orange')

        for i in range(7):
            # if(i==4):
            #     continue
            self.root.grid_rowconfigure(i,weight=1)
        self.root.columnconfigure(0,weight=1)
        self.root.columnconfigure(1,weight=1)

        self.title_label = Label(self.root, text="Title",bg='orange',font="calibri 12 bold")
        self.title_label.grid(row=0, column=0, padx=10, pady=10,sticky="ew")

        self.title_var = StringVar()
        self.title_entry = Entry(self.root, textvariable=self.title_var,bg='orange',font="calibri 12 bold")
        self.title_entry.grid(row=0, column=1, padx=10, pady=10,sticky="ew")

        self.des_label = Label(self.root, text="Description",bg='orange',font="calibri 12 bold")
        self.des_label.grid(row=1, column=0, padx=10, pady=10,sticky="ew")

        self.des_var = StringVar()
        self.des_entry = Entry(self.root, textvariable=self.des_var,bg='orange',font="calibri 12 bold")
        self.des_entry.grid(row=1, column=1, padx=10, pady=10,sticky="ew")

        self.date_label = Label(self.root, text="Select a date:",bg='orange',font="calibri 12 bold")
        self.date_label.grid(row=2, column=0, padx=10, pady=10,sticky="ew")

        self.cal = DateEntry(root, width=12, background='black',
                             foreground='orange', borderwidth=2, year=2024,bg='orange',font="calibri 12 bold")
        self.cal.grid(row=2, column=1, padx=10, pady=10,sticky="ew")

        self.time_label = Label(self.root, text="Time (HH:MM)",bg='orange',font="calibri 12 bold")
        self.time_label.grid(row=3, column=0, padx=10, pady=10,sticky="ew")

        self.time_var = StringVar()
        self.time_entry = Entry(self.root, textvariable=self.time_var,bg='orange',font="calibri 12 bold")
        self.time_entry.grid(row=3, column=1, padx=10, pady=10,sticky="ew")

        self.add_task_button = Button(root, text="Add Task", command=self.add_task,bg='black',fg='orange',font="calibri 12 bold")
        self.add_task_button.grid(row=4, column=0, columnspan=2, pady=10,sticky="ew")

        self.style = ttk.Style()
        self.style.configure("Treeview,heading",background="black",foreground="orange")

        self.tree = ttk.Treeview(root, columns=("Title", "Description", "Date", "Time", "Status"), show="headings")
        self.tree.heading("Title", text="Task Title")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Status", text="Status")
        self.tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10,sticky="ew")

        self.delete_task_button = Button(root, text="Delete Task", command=self.delete_task,bg='black',fg='orange',font="calibri 12 bold")
        self.delete_task_button.grid(row=6, column=0, pady=10,sticky="ew")

        self.complete_task_button = Button(root, text="Mark as Complete", command=self.complete_task,bg='black',fg='orange',font="calibri 12 bold")
        self.complete_task_button.grid(row=6, column=1, pady=10,sticky="ew")

        self.upload_list()

    def add_task(self):
        title = self.title_entry.get()
        des = self.des_entry.get()
        date = self.cal.get()
        time_str = self.time_entry.get()

        try:
            task_time = datetime.strptime(time_str, "%H:%M")
        except ValueError:
            messagebox.showerror("Invalid Time", "Please enter time in HH:MM format.")
            return

        self.tasks.append([title, des, date, task_time.strftime("%H:%M"), "Pending"])
        self.tree.insert("", "end", values=(title, des, date, task_time.strftime("%H:%M"), "Pending"))
        self.save_tasks()
        self.start_reminders()

        self.title_var.set('')
        self.des_var.set('')
        self.time_var.set('')

    def save_tasks(self):
        with open("tasks.txt", 'w') as file:
            file.write(str(self.tasks))

    def upload_list(self):
        try:
            with open("tasks.txt", 'r') as file:
                content = file.read()
                if content:
                    self.tasks = ast.literal_eval(content)
                    for task in self.tasks:
                        self.tree.insert("", "end", values=task)
            self.start_reminders()
        except FileNotFoundError:
            pass

    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            task_index = self.tree.index(selected_item)
            self.tree.delete(selected_item)
            del self.tasks[task_index]
            self.save_tasks()

    def complete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            task_index = self.tree.index(selected_item)
            self.tasks[task_index][4] = "Complete"
            self.tree.item(selected_item, values=self.tasks[task_index])
            self.save_tasks()

    def start_reminders(self):
        for task in self.tasks:
            task_time = datetime.strptime(f"{task[2]} {task[3]}", "%m/%d/%y %H:%M")
            current_time = datetime.now()
            delay = (task_time - current_time).total_seconds()

            if delay > 0:
                threading.Thread(target=self.task_reminder, args=(task, delay)).start()

    def task_reminder(self, task, delay):
        time.sleep(delay)
        if task[4] == "Pending":
            messagebox.showinfo("Reminder", f"Time to do the task: {task[0]}")
            task[4] = "Complete"
            self.save_tasks()
            self.update_treeview()

    def update_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for task in self.tasks:
            self.tree.insert("", "end", values=task)


if __name__ == "__main__":
    root = Tk()
    obj = TODOApp(root)
    root.mainloop()

