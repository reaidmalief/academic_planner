import sys
import os

# Dynamically add the project root directory to the module search path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

import tkinter as tk
from tkinter import ttk
from tasks import open_task_manager
from goals import open_goal_tracker
from utils.visualizer import open_visualizations
from utils.pdf_generator import generate_report

def create_dashboard():
    root = tk.Tk()
    root.title("Academic Skills Planner and Tracker")
    root.geometry("800x600")

    # Dashboard title
    title_label = tk.Label(root, text="Academic Skills Planner and Tracker",
                           font=("Arial", 20, "bold"))
    title_label.pack(pady=20)

    # Navigation buttons
    task_button = ttk.Button(root, text="Manage Tasks", command=open_task_manager)
    task_button.pack(pady=10)

    goal_button = ttk.Button(root, text="Track Goals", command=open_goal_tracker)
    goal_button.pack(pady=10)

    viz_button = ttk.Button(root, text="Visualize Progress", command=open_visualizations)
    viz_button.pack(pady=10)

    report_button = ttk.Button(root, text="View Reports", command=generate_report)
    report_button.pack(pady=10)



    # Run the application
    root.mainloop()

if __name__ == "__main__":
    create_dashboard()
