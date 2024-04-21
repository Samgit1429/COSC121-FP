import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class TaskManagerGUI:
    def __init__(self, root, add_task_callback, edit_task_callback, delete_task_callback):
        self.root = root
        self.add_task_callback = add_task_callback
        self.edit_task_callback = edit_task_callback
        self.delete_task_callback = delete_task_callback

        self.create_widgets()

    def create_widgets(self):
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        # Title
        title_label = ttk.Label(self.main_frame, text="Task Management System", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Task List Section
        self.create_task_list_section()

        # Button Section
        self.create_button_section()

        # Add tooltips
        self.add_tooltips()

    def create_task_list_section(self):
        task_list_frame = ttk.Frame(self.main_frame)
        task_list_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        ttk.Label(task_list_frame, text="Task List", font=("Helvetica", 12, "bold")).pack(pady=5)

        # Task list
        self.task_list = tk.Listbox(task_list_frame, width=50, height=20)
        self.task_list.pack(padx=10, pady=10)

    def create_button_section(self):
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Edit and Delete buttons
        self.edit_button = ttk.Button(button_frame, text="Edit", command=self.open_edit_task_window)
        self.edit_button.pack(side="left", padx=5)

        self.delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_task)
        self.delete_button.pack(side="left", padx=5)

        # Add Task button
        self.add_task_button = ttk.Button(button_frame, text="Add Task", command=self.open_add_task_window)
        self.add_task_button.pack(side="left", padx=5)

    def add_tooltips(self):
        self.add_task_button_tooltip = CreateToolTip(self.add_task_button, "Add a new task")
        self.edit_button_tooltip = CreateToolTip(self.edit_button, "Edit selected task")
        self.delete_button_tooltip = CreateToolTip(self.delete_button, "Delete selected task")

    def open_add_task_window(self):
        self.add_task_window = tk.Toplevel(self.root)
        self.add_task_window.title("Add Task")

        # Task details form
        ttk.Label(self.add_task_window, text="Title:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.title_entry = ttk.Entry(self.add_task_window)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.add_task_window, text="Description:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.description_entry = ttk.Entry(self.add_task_window)
        self.description_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.add_task_window, text="Deadline:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.deadline_entry = ttk.Entry(self.add_task_window)
        self.deadline_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Button(self.add_task_window, text="Add", command=self.add_task).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def open_edit_task_window(self):
        selected_task_index = self.task_list.curselection()
        if selected_task_index:
            task_details = self.task_list.get(selected_task_index[0])
            task_id = task_details.split(" - ")[0]  # Extracting task ID
            task_title, task_description, task_deadline = task_details.split(" - ")[1:]  # Extracting task details
            self.edit_task_window = tk.Toplevel(self.root)
            self.edit_task_window.title("Edit Task")

            ttk.Label(self.edit_task_window, text="Title:").grid(row=0, column=0, padx=10, pady=5)
            self.title_entry = ttk.Entry(self.edit_task_window)
            self.title_entry.insert(0, task_title)
            self.title_entry.grid(row=0, column=1, padx=10, pady=5)

            ttk.Label(self.edit_task_window, text="Description:").grid(row=1, column=0, padx=10, pady=5)
            self.description_entry = ttk.Entry(self.edit_task_window)
            self.description_entry.insert(0, task_description)
            self.description_entry.grid(row=1, column=1, padx=10, pady=5)

            ttk.Label(self.edit_task_window, text="Deadline:").grid(row=2, column=0, padx=10, pady=5)
            self.deadline_entry = ttk.Entry(self.edit_task_window)
            self.deadline_entry.insert(0, task_deadline)
            self.deadline_entry.grid(row=2, column=1, padx=10, pady=5)

            ttk.Button(self.edit_task_window, text="Update", command=lambda: self.edit_task(task_id)).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        deadline = self.deadline_entry.get()
        self.add_task_callback(title, description, deadline)
        self.add_task_window.destroy()

    def edit_task(self, task_id):
        title = self.title_entry.get()
        description = self.description_entry.get()
        deadline = self.deadline_entry.get()
        self.edit_task_callback(task_id, title, description, deadline)
        self.edit_task_window.destroy()

    def delete_task(self):
        selected_task_index = self.task_list.curselection()
        if selected_task_index:
            task_details = self.task_list.get(selected_task_index[0])
            task_id = task_details.split(" - ")[0]  # Extracting task ID
            self.delete_task_callback(task_id)

    def display_tasks(self, tasks):
        self.task_list.delete(0, tk.END)
        for task in tasks:
            self.task_list.insert(tk.END, f"{task['id']} - {task['title']} - {task['description']} - {task['deadline']}")

class CreateToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event):
        x = y = 0
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="lightyellow", relief="solid", borderwidth=1, padx=5, pady=2)
        label.pack()

    def leave(self, event):
        if self.tooltip:
            self.tooltip.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root, None, None, None)
    root.mainloop()