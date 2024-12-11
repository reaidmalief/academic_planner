import tkinter as tk
from tkinter import ttk
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def open_visualizations():
    # Visualization Window
    viz_window = tk.Tk()
    viz_window.title("Visualizations")
    viz_window.geometry("800x600")

    # Task Completion Chart Button
    task_chart_button = ttk.Button(viz_window, text="Task Completion Chart", command=show_task_completion_chart)
    task_chart_button.pack(pady=20)

    # Goal Progress Chart Button
    goal_chart_button = ttk.Button(viz_window, text="Goal Progress Chart", command=show_goal_progress_chart)
    goal_chart_button.pack(pady=20)

    viz_window.mainloop()

def show_task_completion_chart():
    # Fetch task data from database
    connection = sqlite3.connect("academic_planner.db")
    cursor = connection.cursor()
    cursor.execute("SELECT name, completion_percentage FROM tasks")
    data = cursor.fetchall()
    connection.close()

    # Ensure that there is data to display
    if not data:
        print("No tasks found in the database.")
        return

    # Prepare data for the pie chart
    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    # Validate the data (Ensure non-negative percentages)
    values = np.array(values)
    if np.any(values < 0) or np.any(values > 100):
        print("Invalid completion percentage values found (must be between 0 and 100).")
        return

    if len(values) == 0 or np.sum(values) == 0:
        print("No valid data to display in the pie chart.")
        return

    # Create figure with a larger size and adjust layout
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Add padding around the plot
    plt.subplots_adjust(left=0.1, right=0.75, top=0.9, bottom=0.1)

    # Plot the pie chart with percentage labels only (no category labels)
    wedges, texts, autotexts = ax.pie(
        values,
        labels=[''] * len(labels), 
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.75,
        wedgeprops=dict(width=0.5)
    )

    # Customize the percentage text properties
    plt.setp(autotexts, size=9, weight="bold")

    # Add a legend on the right side
    ax.legend(
        wedges,
        labels,
        title="Tasks",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )

    # Equal aspect ratio ensures the pie chart is circular
    ax.axis('equal')

    # Add a title with padding
    plt.title("Task Completion Chart", pad=20, size=12, weight="bold")

    show_chart_window(fig, "Task Completion Chart")

def show_goal_progress_chart():
    # Fetch goal data from database
    connection = sqlite3.connect("academic_planner.db")
    cursor = connection.cursor()
    cursor.execute("SELECT name, progress FROM goals")
    data = cursor.fetchall()
    connection.close()

    # Ensure that there is data to display
    if not data:
        print("No goals found in the database.")
        return

    # Prepare data for the bar chart
    names = [row[0] for row in data]
    progress = [row[1] for row in data]

    # Create a bar chart
    fig, ax = plt.subplots()
    ax.bar(names, progress, color="skyblue")
    ax.set_xlabel("Goals")
    ax.set_ylabel("Progress (%)")
    ax.set_title("Goal Progress")
    ax.set_ylim(0, 100)  

    # Display the chart in a new window
    show_chart_window(fig, "Goal Progress Chart")

def show_chart_window(fig, title):
    chart_window = tk.Toplevel()
    chart_window.title(title)
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)