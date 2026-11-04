# ==============================================================================
# File: database.py
# Purpose: SQLite Database Configuration, Connection & Schema Setup
# ==============================================================================
#
# PYTHON & DATABASE CONCEPTS DEMONSTRATED IN THIS FILE:
# 1. SQLite: A lightweight, serverless relational database engine bundled with Python.
# 2. File Path Handling: Using 'os.path' to create reliable cross-platform directory paths.
# 3. Connection and Cursor:
#      - 'connection': Represents the open channel to the database file.
#      - 'cursor': The object used to execute SQL queries and fetch results.
# 4. Transactions: Changes are saved only when 'conn.commit()' is called.
# 5. Exception Handling: try-except-finally blocks to safely close database resources.
# 6. Relational Integrity: Primary Keys, Foreign Keys, and Cascading Deletes.
# ==============================================================================

import os
import sqlite3

# Determine the absolute directory where this file lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the database folder and database file path
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "students.db")


def get_connection():
    """
    Creates and returns an active connection to the SQLite database.
    
    Why this function exists:
    Instead of repeating connection code across multiple files, centralizing it
    ensures consistent settings (such as enabling Foreign Keys).
    """
    # Ensure the 'database/' directory exists before attempting to open the database file
    os.makedirs(DB_DIR, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    
    # By default, SQLite does NOT enforce Foreign Key constraints.
    # Executing 'PRAGMA foreign_keys = ON' enables relational integrity.
    conn.execute("PRAGMA foreign_keys = ON;")
    
    # row_factory = sqlite3.Row allows column access by name (row['name'])
    # as well as index (row[0]), making query results much easier to read.
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    """
    Creates the required database tables if they do not already exist.
    
    Tables Created:
    1. 'students'   - Stores general profile information for each student.
    2. 'marks'      - Stores subject marks linked to a student.
    3. 'attendance' - Stores daily attendance status linked to a student.
    
    SQL Concepts Used:
    - CREATE TABLE IF NOT EXISTS: Idempotent operation; only creates table on first run.
    - PRIMARY KEY: A unique identifier for every record in the table.
    - FOREIGN KEY: A reference linking child records (marks, attendance) to the parent student.
    - ON DELETE CASCADE: When a student is deleted, their marks & attendance are automatically removed.
    - UNIQUE: Guarantees no duplicate records for the same student on the same date/subject.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # ----------------------------------------------------------------------
        # Table 1: Students
        # ----------------------------------------------------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                department TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL
            );
        """)

        # ----------------------------------------------------------------------
        # Table 2: Marks
        # ----------------------------------------------------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS marks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                subject TEXT NOT NULL,
                marks_obtained REAL NOT NULL,
                max_marks REAL NOT NULL DEFAULT 100,
                FOREIGN KEY (student_id) REFERENCES students (student_id) ON DELETE CASCADE,
                UNIQUE (student_id, subject)
            );
        """)

        # ----------------------------------------------------------------------
        # Table 3: Attendance
        # ----------------------------------------------------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('Present', 'Absent')),
                FOREIGN KEY (student_id) REFERENCES students (student_id) ON DELETE CASCADE,
                UNIQUE (student_id, date)
            );
        """)

        # Commit all table creation statements to the database
        conn.commit()

    except sqlite3.Error as error:
        # Catch and print any SQLite database errors
        print(f"Database Initialization Error: {error}")
        raise error
    finally:
        # Always close the connection to release system resources and avoid locks
        if conn:
            conn.close()


def seed_sample_data():
    """
    Seeds initial realistic sample data if the students table is empty.
    This provides an immediate, out-of-the-box working experience for beginners
    and project evaluators without having to manually enter 10 records first.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check if students table is currently empty
        cursor.execute("SELECT COUNT(*) AS total FROM students;")
        row = cursor.fetchone()
        if row["total"] > 0:
            return  # Data already exists, do not duplicate

        # Sample student list (demonstrating Python List of Tuples)
        sample_students = [
            ("CS101", "Alex Johnson", 19, "Male", "Computer Science", "alex.j@university.edu", "555-0101"),
            ("CS102", "Sophia Martinez", 20, "Female", "Computer Science", "sophia.m@university.edu", "555-0102"),
            ("EC201", "Liam Smith", 19, "Male", "Electronics", "liam.s@university.edu", "555-0103"),
            ("ME301", "Emma Watson", 21, "Female", "Mechanical", "emma.w@university.edu", "555-0104"),
            ("IT105", "Noah Brown", 20, "Male", "Information Tech", "noah.b@university.edu", "555-0105"),
        ]

        cursor.executemany("""
            INSERT INTO students (student_id, name, age, gender, department, email, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, sample_students)

        # Sample marks data: (student_id, subject, marks_obtained, max_marks)
        sample_marks = [
            ("CS101", "Python Programming", 92, 100),
            ("CS101", "Data Structures", 88, 100),
            ("CS101", "Mathematics I", 85, 100),
            
            ("CS102", "Python Programming", 96, 100),
            ("CS102", "Data Structures", 94, 100),
            ("CS102", "Mathematics I", 90, 100),

            ("EC201", "Digital Logic", 74, 100),
            ("EC201", "Circuit Theory", 68, 100),
            ("EC201", "Mathematics I", 70, 100),

            ("ME301", "Thermodynamics", 81, 100),
            ("ME301", "Mechanics", 79, 100),
            ("ME301", "Mathematics I", 75, 100),

            ("IT105", "Web Development", 89, 100),
            ("IT105", "Python Programming", 84, 100),
            ("IT105", "Database Systems", 86, 100),
        ]

        cursor.executemany("""
            INSERT INTO marks (student_id, subject, marks_obtained, max_marks)
            VALUES (?, ?, ?, ?);
        """, sample_marks)

        # Sample attendance data: (student_id, date, status)
        dates = ["2026-10-01", "2026-10-02", "2026-10-03", "2026-10-04", "2026-10-05"]
        sample_attendance = []
        for s in sample_students:
            s_id = s[0]
            for idx, d in enumerate(dates):
                # CS102 attended all; EC201 missed a few (to demonstrate varying percentages)
                if s_id == "EC201" and idx in [1, 3]:
                    status = "Absent"
                elif s_id == "ME301" and idx == 2:
                    status = "Absent"
                else:
                    status = "Present"
                sample_attendance.append((s_id, d, status))

        cursor.executemany("""
            INSERT INTO attendance (student_id, date, status)
            VALUES (?, ?, ?);
        """, sample_attendance)

        conn.commit()
        print("Database seeded with sample data successfully.")

    except sqlite3.Error as error:
        print(f"Error seeding sample data: {error}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    # If run directly as a script (python database.py), test table creation & seeding
    print("Initializing Database...")
    initialize_database()
    seed_sample_data()
    print(f"Database successfully verified at: {DB_PATH}")
