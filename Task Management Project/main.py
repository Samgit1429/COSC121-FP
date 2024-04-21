import tkinter as tk
from gui import TaskManagerGUI
from database import DatabaseManager
from task import Task

class TaskManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management System")
        
        # Initialize database manager
        self.db_manager = DatabaseManager("tasks.db")
        
        # Initialize GUI
        self.gui = TaskManagerGUI(root, self.add_task, self.edit_task, self.delete_task)
        self.refresh_tasks()

    def add_task(self, title, description, deadline):
        new_task = Task(title, description, deadline)
        self.db_manager.add_task(new_task)
        self.refresh_tasks()

    def edit_task(self, task_id, title, description, deadline):
        updated_task = Task(title, description, deadline, task_id)
        self.db_manager.edit_task(updated_task)
        self.refresh_tasks()

    def delete_task(self, task_id):
        self.db_manager.delete_task(task_id)
        self.refresh_tasks()

    def refresh_tasks(self):
        tasks = self.db_manager.get_all_tasks()
        self.gui.display_tasks(tasks)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagementApp(root)
    root.mainloop()
