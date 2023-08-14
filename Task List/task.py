import tkinter as tk
from tkinter import messagebox


class Task:
    def __init__(self, description, status="Incomplete"):
        self.description = description
        self.status = status


class TodoListManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, description):
        task = Task(description)
        self.tasks.append(task)
        self.save_tasks()
        messagebox.showinfo("Success", "Task added successfully.")

    def update_task(self, index, description):
        if index < len(self.tasks):
            self.tasks[index].description = description
            self.save_tasks()
            messagebox.showinfo("Success", "Task updated successfully.")
        else:
            messagebox.showinfo("Invalid Index", "Task index out of range.")

    def delete_task(self, index):
        if index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()
            messagebox.showinfo("Success", "Task deleted successfully.")
        else:
            messagebox.showinfo("Invalid Index", "Task index out of range.")

    def toggle_task_status(self, index):
        if index < len(self.tasks):
            task = self.tasks[index]
            if task.status == "Incomplete":
                task.status = "Complete"
            else:
                task.status = "Incomplete"
            self.save_tasks()
            messagebox.showinfo("Success", "Task status updated successfully.")
        else:
            messagebox.showinfo("Invalid Index", "Task index out of range.")

    def display_all_tasks(self):
        if self.tasks:
            task_list = "\n".join([f"{index+1}. {task.description} - {task.status}" for index, task in enumerate(self.tasks)])
            messagebox.showinfo("All Tasks", task_list)
        else:
            messagebox.showinfo("No Tasks", "No tasks found.")

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(f"{task.description},{task.status}\n")

    def load_tasks(self):
        self.tasks = []
        try:
            with open("tasks.txt", "r") as file:
                for line in file:
                    description, status = line.strip().split(",")
                    task = Task(description, status)
                    self.tasks.append(task)
        except FileNotFoundError:
            pass


class TodoListApp(tk.Tk):
    def __init__(self, todo_manager):
        super().__init__()
        self.todo_manager = todo_manager
        self.title("Todo List Manager")
        self.create_widgets()
        self.update_ui()

    def create_widgets(self):
        self.label_description = tk.Label(self, text="Task Description:")
        self.label_description.pack()
        self.entry_description = tk.Entry(self)
        self.entry_description.pack()

        self.button_add = tk.Button(self, text="Add Task", command=self.add_task)
        self.button_add.pack()

        self.label_index = tk.Label(self, text="Task Index:")
        self.label_index.pack()
        self.entry_index = tk.Entry(self)
        self.entry_index.pack()

        self.label_new_description = tk.Label(self, text="New Description:")
        self.label_new_description.pack()
        self.entry_new_description = tk.Entry(self)
        self.entry_new_description.pack()

        self.button_update = tk.Button(self, text="Update Task", command=self.update_task)
        self.button_update.pack()

        self.button_delete = tk.Button(self, text="Delete Task", command=self.delete_task)
        self.button_delete.pack()

        self.button_toggle = tk.Button(self, text="Task  Completed", command=self.toggle_task_status)
        self.button_toggle.pack()

        self.button_display = tk.Button(self, text="Display All Tasks", command=self.display_all_tasks)
        self.button_display.pack()

    def update_ui(self):
        self.entry_description.delete(0, tk.END)
        self.entry_index.delete(0, tk.END)
        self.entry_new_description.delete(0, tk.END)

    def add_task(self):
        description = self.entry_description.get()
        self.todo_manager.add_task(description)
        self.update_ui()

    def update_task(self):
        index = int(self.entry_index.get()) - 1
        new_description = self.entry_new_description.get()
        self.todo_manager.update_task(index, new_description)
        self.update_ui()

    def delete_task(self):
        index = int(self.entry_index.get()) - 1
        self.todo_manager.delete_task(index)
        self.update_ui()

    def toggle_task_status(self):
        index = int(self.entry_index.get()) - 1
        self.todo_manager.toggle_task_status(index)
        self.update_ui()

    def display_all_tasks(self):
        self.todo_manager.display_all_tasks()


if __name__ == "__main__":
    todo_manager = TodoListManager()
    todo_manager.load_tasks()
    app = TodoListApp(todo_manager)
    app.mainloop()
