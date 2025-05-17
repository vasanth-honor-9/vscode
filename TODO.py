import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import json
import os
from datetime import datetime

DATA_FILE = "tasks.json"

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced To-Do App")
        self.root.geometry("600x600")
        self.tasks = []
        self.filter_status = "all"

        self.load_tasks()

        # --- Top bar ---
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)

        self.task_entry = tk.Entry(top_frame, width=40)
        self.task_entry.pack(side=tk.LEFT, padx=5)

        self.add_button = tk.Button(top_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.filter_var = tk.StringVar(value="all")
        filter_menu = tk.OptionMenu(top_frame, self.filter_var, "all", "in-progress", "done", command=self.refresh_tasks)
        filter_menu.pack(side=tk.LEFT, padx=5)

        # --- Task list frame ---
        self.task_frame = tk.Frame(root)
        self.task_frame.pack(fill=tk.BOTH, expand=True)

        self.refresh_tasks()

    def save_tasks(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                self.tasks = json.load(f)

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text == "":
            messagebox.showwarning("Input Error", "Task cannot be empty.")
            return

        due_date = simpledialog.askstring("Due Date", "Enter due date (YYYY-MM-DD):")
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date", "Please use YYYY-MM-DD format.")
                return
        else:
            due_date = ""

        new_task = {
            "text": task_text,
            "status": "in-progress",
            "due": due_date
        }
        self.tasks.append(new_task)
        self.task_entry.delete(0, tk.END)
        self.save_tasks()
        self.refresh_tasks()

    def toggle_status(self, index):
        self.tasks[index]["status"] = "done" if self.tasks[index]["status"] == "in-progress" else "in-progress"
        self.save_tasks()
        self.refresh_tasks()

    def delete_task(self, index):
        if messagebox.askyesno("Delete", "Are you sure you want to delete this task?"):
            del self.tasks[index]
            self.save_tasks()
            self.refresh_tasks()

    def edit_task(self, index):
        new_text = simpledialog.askstring("Edit Task", "Update task:", initialvalue=self.tasks[index]["text"])
        if new_text:
            self.tasks[index]["text"] = new_text
            self.save_tasks()
            self.refresh_tasks()

    def sort_tasks(self):
        self.tasks.sort(key=lambda x: (x["status"] == "done", x.get("due", "")))

    def refresh_tasks(self, *args):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        self.sort_tasks()

        for idx, task in enumerate(self.tasks):
            if self.filter_status != "all" and task["status"] != self.filter_var.get():
                continue

            row = tk.Frame(self.task_frame)
            row.pack(fill=tk.X, padx=10, pady=4)

            checkbox_var = tk.BooleanVar(value=(task["status"] == "done"))
            checkbox = tk.Checkbutton(row, variable=checkbox_var, command=lambda i=idx: self.toggle_status(i))
            checkbox.pack(side=tk.LEFT)

            label_color = "green" if task["status"] == "done" else "blue"
            label_text = f"{task['text']}  [Due: {task['due'] or 'N/A'}]"
            label = tk.Label(row, text=label_text, fg=label_color, width=40, anchor="w")
            label.pack(side=tk.LEFT)

            edit_btn = tk.Button(row, text="Edit", width=6, command=lambda i=idx: self.edit_task(i))
            edit_btn.pack(side=tk.LEFT, padx=5)

            delete_btn = tk.Button(row, text="Delete", width=6, command=lambda i=idx: self.delete_task(i))
            delete_btn.pack(side=tk.LEFT)

# --- Run the application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
