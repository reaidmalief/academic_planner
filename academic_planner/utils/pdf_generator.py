from fpdf import FPDF
import sqlite3

def generate_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add Report Title
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="Weekly Report", ln=True, align="C")
    pdf.ln(10)

    # Add Tasks Section
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt="Tasks Summary", ln=True)
    pdf.set_font("Arial", size=12)

    connection = sqlite3.connect("academic_planner.db")
    cursor = connection.cursor()
    cursor.execute("SELECT name, due_date, priority, completed FROM tasks")
    tasks = cursor.fetchall()

    for task in tasks:
        status = "Completed" if task[3] else "Pending"
        pdf.cell(200, 10, txt=f"Task: {task[0]}, Due: {task[1]}, Priority: {task[2]}, Status: {status}", ln=True)

    pdf.ln(10)

    # Add Goals Section
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt="Goals Summary", ln=True)
    pdf.set_font("Arial", size=12)

    cursor.execute("SELECT name, start_date, end_date, progress FROM goals")
    goals = cursor.fetchall()

    for goal in goals:
        pdf.cell(200, 10, txt=f"Goal: {goal[0]}, Start: {goal[1]}, End: {goal[2]}, Progress: {goal[3]}%", ln=True)

    connection.close()

    # Save the PDF
    pdf.output("Weekly_Report.pdf")
    print("Report generated: Weekly_Report.pdf")
