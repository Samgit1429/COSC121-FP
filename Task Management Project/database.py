import sqlite3
from task import Task

class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_tables()

    def create_tables(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Tasks (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    deadline TEXT
                )
            """)
            conn.commit()

    def add_task(self, task):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Tasks (title, description, deadline)
                VALUES (?, ?, ?)
            """, (task.title, task.description, task.deadline))
            conn.commit()

    def edit_task(self, task):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Tasks
                SET title=?, description=?, deadline=?
                WHERE id=?
            """, (task.title, task.description, task.deadline, task.id))
            conn.commit()

    def delete_task(self, task_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Tasks WHERE id=?", (task_id,))
            conn.commit()

    def get_all_tasks(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Tasks")
            tasks = cursor.fetchall()
            return [{'id': row[0], 'title': row[1], 'description': row[2], 'deadline': row[3]} for row in tasks]
