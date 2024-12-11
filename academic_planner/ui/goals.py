import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def open_goal_tracker():
    # Goal Tracker Window
    goal_window = tk.Tk()
    goal_window.title("Goal Tracker")
    goal_window.geometry("600x400")

    # Goal Tracker Title
    title_label = tk.Label(goal_window, text="Goal Tracker", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Add Goal Button
    add_goal_button = ttk.Button(goal_window, text="Add Goal", command=lambda: add_goal(goal_window, goal_tree))
    add_goal_button.pack(pady=10)

    # Goal List (Treeview)
    columns = ("ID", "Name", "Start Date", "End Date", "Progress")
    goal_tree = ttk.Treeview(goal_window, columns=columns, show="headings", height=10)
    for col in columns:
        goal_tree.heading(col, text=col)
        goal_tree.column(col, width=100)
    goal_tree.pack(pady=20, fill="x")

    # Fetch and Display Goals
    fetch_goals(goal_tree)

    # Add Edit and Delete Buttons
    edit_goal_button = ttk.Button(goal_window, text="Edit Goal", command=lambda: edit_goal(goal_tree, goal_window))
    edit_goal_button.pack(pady=5)

    delete_goal_button = ttk.Button(goal_window, text="Delete Goal", command=lambda: delete_goal(goal_tree))
    delete_goal_button.pack(pady=5)

    goal_window.mainloop()


def fetch_goals(tree):
    # Clear existing rows
    for row in tree.get_children():
        tree.delete(row)

    # Fetch data from the database
    connection = sqlite3.connect("academic_planner.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, start_date, end_date, progress FROM goals")
    rows = cursor.fetchall()
    connection.close()

    # Insert rows into Treeview
    for row in rows:
        tree.insert("", "end", values=row)

def add_goal(goal_window, goal_tree):
    add_goal_window = tk.Toplevel(goal_window)
    add_goal_window.title("Add New Goal")
    add_goal_window.geometry("400x300")

    # Goal Name
    tk.Label(add_goal_window, text="Goal Name:").pack(pady=5)
    goal_name_entry = ttk.Entry(add_goal_window)
    goal_name_entry.pack(pady=5)

    # Start Date
    tk.Label(add_goal_window, text="Start Date (YYYY-MM-DD):").pack(pady=5)
    start_date_entry = ttk.Entry(add_goal_window)
    start_date_entry.pack(pady=5)

    # End Date
    tk.Label(add_goal_window, text="End Date (YYYY-MM-DD):").pack(pady=5)
    end_date_entry = ttk.Entry(add_goal_window)
    end_date_entry.pack(pady=5)

    # Progress
    tk.Label(add_goal_window, text="Progress (%):").pack(pady=5)
    progress_spinbox = ttk.Spinbox(add_goal_window, from_=0, to=100, width=10)
    progress_spinbox.pack(pady=5)

    # Save Button
    save_button = ttk.Button(add_goal_window, text="Save Goal",
                             command=lambda: save_goal(goal_name_entry.get(), start_date_entry.get(),
                                                       end_date_entry.get(), progress_spinbox.get(), add_goal_window, goal_tree))
    save_button.pack(pady=10)

def save_goal(name, start_date, end_date, progress, window, goal_tree):
    if name and start_date and end_date and progress:
        try:
            connection = sqlite3.connect("academic_planner.db")
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO goals (name, start_date, end_date, progress)
                VALUES (?, ?, ?, ?)
            """, (name, start_date, end_date, int(progress)))
            connection.commit()
            connection.close()
            messagebox.showinfo("Success", "Goal added successfully!")
            fetch_goals(goal_tree)  # Refresh the goal list
            window.destroy()  # Close the add goal window
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add goal: {e}")
    else:
        messagebox.showwarning("Warning", "All fields are required!")


def edit_goal(name, start_date, end_date, progress, window):
    if name and start_date and end_date and progress:
        try:
            connection = sqlite3.connect("academic_planner.db")
            cursor = connection.cursor()
            cursor.execute("""
                           UPDATE goals
                           SET name = ?, start_date = ?, end_date = ?, progress = ?
                           WHERE id = ?
                           """, (name, start_date, end_date, int(progress), id))
            connection.commit()
            connection.close()
            messagebox.showinfo("Success", "Goal updated successfully.")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update goal: {e}")
    else:
        messagebox.showwarning("Warning", "All fields are required.")

def edit_goal(tree, goal_window):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a goal to edit.")
        return

    # Get the selected goal's details
    goal_data = tree.item(selected_item, "values")
    goal_id, name, start_date, end_date, progress = goal_data

    # Create a popup window
    edit_goal_window = tk.Toplevel(goal_window)
    edit_goal_window.title("Edit Goal")
    edit_goal_window.geometry("400x300")

    # Fields for editing
    tk.Label(edit_goal_window, text="Goal Name:").pack(pady=5)
    goal_name_entry = ttk.Entry(edit_goal_window)
    goal_name_entry.insert(0, name)
    goal_name_entry.pack(pady=5)

    tk.Label(edit_goal_window, text="Start Date (YYYY-MM-DD):").pack(pady=5)
    start_date_entry = ttk.Entry(edit_goal_window)
    start_date_entry.insert(0, start_date)
    start_date_entry.pack(pady=5)

    tk.Label(edit_goal_window, text="End Date (YYYY-MM-DD):").pack(pady=5)
    end_date_entry = ttk.Entry(edit_goal_window)
    end_date_entry.insert(0, end_date)
    end_date_entry.pack(pady=5)

    tk.Label(edit_goal_window, text="Progress (%):").pack(pady=5)
    progress_spinbox = ttk.Spinbox(edit_goal_window, from_=0, to=100, width=10)
    progress_spinbox.insert(0, progress)
    progress_spinbox.pack(pady=5)

    # Save Changes Button
    save_button = ttk.Button(edit_goal_window, text="Save Changes",
                              command=lambda: save_edited_goal(goal_id, goal_name_entry.get(),
                                                               start_date_entry.get(),
                                                               end_date_entry.get(),
                                                               progress_spinbox.get(),
                                                               edit_goal_window, tree))
    save_button.pack(pady=10)

def save_edited_goal(goal_id, name, start_date, end_date, progress, window, tree):
    if name and start_date and end_date and progress:
        try:
            connection = sqlite3.connect("academic_planner.db")
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE goals
                SET name = ?, start_date = ?, end_date = ?, progress = ?
                WHERE id = ?
            """, (name, start_date, end_date, int(progress), goal_id))
            connection.commit()
            connection.close()
            messagebox.showinfo("Success", "Goal updated successfully!")
            window.destroy()
            fetch_goals(tree)  # Refresh the goal list
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update goal: {e}")
    else:
        messagebox.showwarning("Warning", "All fields are required!")


def delete_goal(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a goal to delete.")
        return

    # Get the selected goal's ID
    goal_id = tree.item(selected_item, "values")[0]

    # Confirm deletion
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this goal?")
    if confirm:
        try:
            connection = sqlite3.connect("academic_planner.db")
            cursor = connection.cursor()
            cursor.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
            connection.commit()
            connection.close()
            messagebox.showinfo("Success", "Goal deleted successfully!")
            fetch_goals(tree)  # Refresh the goal list
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete goal: {e}")
    else:
        messagebox.showinfo("Info", "Deletion cancelled.")

if __name__ == "__main__":
    open_goal_tracker()
