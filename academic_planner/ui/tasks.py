import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def open_task_manager():
    # Task manager window
    task_window = tk.Tk()
    task_window.title("Task Manager")
    task_window.geometry("800x600")

    # Task manager title
    title_label = tk.Label(task_window, text="Task Manager", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Add Task Button
    add_task_button = ttk.Button(task_window, text="Add Task", command=lambda: add_task(task_window))
    add_task_button.pack(pady=10)

    # Add Delete Task Button
    delete_task_button = ttk.Button(task_window, text="Delete Task", command=lambda: delete_task(task_tree))
    delete_task_button.pack(pady=10)

    # Add Edit Task Button
    edit_task_button = ttk.Button(task_window, text="Edit Task", command=lambda: edit_task(task_tree, task_window))
    edit_task_button.pack(pady=10)

    # Task List (Tree View)
    columns = ("ID", "Name", "Due Date", "Priority", "Completed")
    task_tree = ttk.Treeview(task_window, columns=columns, show="headings", height=10)
    for col in columns:
        task_tree.heading(col, text=col)
        task_tree.column(col, width=100)
    task_tree.pack(pady=10, fill="x")

    # Fetch and display tasks
    fetch_tasks(task_tree)

    # Placeholder for the task list
    if task_window.winfo_exists():
        tasks_label = tk.Label(task_window, text="Tasks will be displayed here")
        tasks_label.pack(pady=10)
    else:
        print("Task Manager window is closed.")

    # Start the Tkinter event loop
    task_window.mainloop()


def add_task(task_window):
    # Create a new pop-up window for adding a task
    add_task_window = tk.Toplevel(task_window)
    add_task_window.title("Add New Task")
    add_task_window.geometry("400x300")

    #Task Name Entry
    tk.Label(add_task_window, text = "Task Name: ").pack(pady = 5)
    task_name_entry = tk.Entry((add_task_window))
    task_name_entry.pack(pady = 5)

    #Due Date Entry
    tk.Label(add_task_window, text = "Due Date (YYYY-MM-DD): ").pack(pady = 5)
    due_date_entry = ttk.Entry(add_task_window)
    due_date_entry.pack(pady = 5)

    #Priority Selector
    tk.Label(add_task_window, text = "Priority (1-5): ").pack(pady = 5)
    priority_spinbox = tk.Spinbox(add_task_window, from_ = 1, to = 5, width = 5)
    priority_spinbox.pack(pady = 5)

    #Save Button
    save_button = ttk.Button(add_task_window, text = "Save Task", command = lambda: save_task(task_name_entry.get(), due_date_entry.get(), priority_spinbox.get(), add_task_window))
    save_button.pack(pady = 10)

def save_task(name, due_date, priority, window):
    # Save the task to the database
    if name and due_date and priority:
        try:
            connection = sqlite3.connect("academic_planner.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO tasks (name, due_date, priority, completed) VALUES (?, ?, ?, 0)", (name, due_date, int(priority)))
            connection.commit()
            connection.close()
            tk.messagebox.showinfo("Success", "Task saved successfully.")
            window.destroy()
        except Exception as e:
            tk.messagebox.showinfo("Error", f"Failed to add task: {e}")
    else:
        tk.messagebox.showerror("Error", "All fields are required.")

def fetch_tasks(tree):
    #Clear existing rows
    for row in tree.get_children():
        tree.delete(row)

    #Fetch tasks from the database
    connection = sqlite3.connect("academic_planner.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, due_date, priority, completed FROM tasks")
    rows = cursor.fetchall()
    connection.close()

    #Insert rows into TreeView
    for row in rows:
        tree.insert("", "end", values = row)

def delete_task(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a task to delete.")
        return
    
    #Get the selected tasks ID
    task_id = tree.item(selected_item, "values")[0]

    #Confirm deletion
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this task?")
    if confirm:
        try:
            connection = sqlite3.connect("academic_planner.db")
            cursor = connection.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id))
            connection.commit()
            connection.close()
            messagebox.showinfo("Success", "Task deleted successfully.")
            fetch_tasks(tree)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete task: {e}")

def edit_task(tree, task_window):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a task to edit.")
        return
    
    #Get the selected task's ID
    task_data = tree.item(selected_item, "values")
    task_id, name, due_date, priority, completed = task_data

    #Create a popup window
    edit_task_window = tk.Toplevel(task_window)
    edit_task_window.title("Edit Task")
    edit_task_window.geometry("400x300")

    #Field for editing
    tk.Label(edit_task_window, text="Task Name: ").pack(pady=5)
    task_name_entry = tk.Entry(edit_task_window)
    task_name_entry.insert(0, name)
    task_name_entry.pack(pady=5)

    tk.Label(edit_task_window, text="Due Date (YYYY-MM-DD): ").pack(pady=5)
    due_date_entry = ttk.Entry(edit_task_window)
    due_date_entry.insert(0, due_date)
    due_date_entry.pack(pady=5)

    tk.Label(edit_task_window, text="Priority (1-5): ").pack(pady=5)
    priority_spinbox = tk.Spinbox(edit_task_window, from_=1, to=5, width=5)
    priority_spinbox.insert(0, priority)
    priority_spinbox.pack(pady=5)

    #Save changes button
    save_button = ttk.Button(edit_task_window, text="Save Changes", command=lambda: save_edited_task(task_id, task_name_entry.get(), due_date_entry.get(), priority_spinbox.get(), edit_task_window, tree))
    save_button.pack(pady=10)

def save_edited_task(task_id, name, due_date, priority, window, tree):
    if name and due_date and priority:
        try:
            connection = sqlite3.connect("academic_planner.db")
            cursor = connection.cursor()
            cursor.execute("""
                           UPDATE tasks
                           SET name = ?, due_date = ?, priority = ?
                           WHERE id = ?
                           """, (name, due_date, int(priority), task_id))
            connection.commit()
            connection.close()
            messagebox.showinfo("Success", "Task saved successfully!")
            window.destroy()
            fetch_tasks(tree)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {e}")
    else:
        messagebox.showwarning("Error", "All fields are required.")
        


if __name__ == "__main__":
    open_task_manager()

