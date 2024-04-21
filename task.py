class Task:
    def __init__(self, title, description, deadline, task_id=None):
        self.id = task_id
        self.title = title
        self.description = description
        self.deadline = deadline
