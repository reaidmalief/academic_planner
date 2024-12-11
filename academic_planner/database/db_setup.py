import sqlite3

# Function to initialize the database
def initialize_db():
    connection = sqlite3.connect("academic_planner.db")
    cursor = connection.cursor()

    # Drop any existing Tasks table to avoid conflicts 
    cursor.execute("DROP TABLE IF EXISTS Tasks")
    
    # Create the updated Tasks table schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            due_date TEXT NOT NULL,
            priority INTEGER DEFAULT 1,
            completed INTEGER DEFAULT 0,
            completion_percentage INTEGER DEFAULT 0
        );
    """)

    # Create GOALS table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            progress INTEGER DEFAULT 0
        );
    """)

    connection.commit()
    connection.close()

# Run initialization when the script is executed
if __name__ == "__main__":
    initialize_db()
    print("Database initialized successfully.")
