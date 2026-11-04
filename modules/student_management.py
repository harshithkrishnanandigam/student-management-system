# ==============================================================================
# File: modules/student_management.py
# Purpose: Business Logic & SQLite Operations for Student Management
# ==============================================================================
#
# PYTHON CONCEPTS DEMONSTRATED IN THIS FILE:
# 1. Functions: Reusable blocks of code that perform specific tasks.
# 2. Lists & Dictionaries: Storing and structuring query results.
# 3. Loops: Iterating over cursor rows to build list collections.
# 4. Exception Handling: Using try-except-finally to handle SQLite errors gracefully.
# 5. Parameterized Queries: Using '?' placeholders to safely prevent SQL Injection attacks.
# 6. Object-Oriented Integration: Accepting and interacting with 'Student' model objects.
# ==============================================================================

import sqlite3
from database import get_connection
from models.student import Student


def add_student(student: Student) -> tuple[bool, str]:
    """
    Inserts a new student record into the 'students' database table.
    
    Why this function exists:
    Allows the user interface to add a student safely through validation and SQL transactions.
    
    Parameters:
        student (Student): An instance of the Student model class.
        
    Returns:
        tuple (bool, str): (Success flag, descriptive message).
    """
    # Step 1: Validate student object data
    is_valid, validation_msg = student.validate()
    if not is_valid:
        return False, validation_msg

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # SQL INSERT query using parameterized placeholders (?)
        # NEVER concatenate variables directly into SQL strings (prevents SQL Injection)
        query = """
            INSERT INTO students (student_id, name, age, gender, department, email, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        cursor.execute(query, (
            student.student_id,
            student.name,
            student.age,
            student.gender,
            student.department,
            student.email,
            student.phone
        ))
        
        # Save the transaction
        conn.commit()
        return True, f"Student '{student.name}' (ID: {student.student_id}) added successfully!"

    except sqlite3.IntegrityError:
        # IntegrityError occurs if the student_id already exists (PRIMARY KEY violation)
        return False, f"A student with ID '{student.student_id}' already exists. Please use a unique ID."
    except sqlite3.Error as error:
        return False, f"Database error while adding student: {error}"
    finally:
        # Ensure database connection is closed even if an exception occurs
        if conn:
            conn.close()


def get_all_students() -> list[dict]:
    """
    Retrieves all students currently stored in the database.
    
    Demonstrates:
    - SQL 'SELECT * FROM students ORDER BY name ASC'
    - Looping over database records
    - Storing records as a Python list of dictionaries
    """
    students_list = []
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT student_id, name, age, gender, department, email, phone FROM students ORDER BY student_id ASC;"
        cursor.execute(query)

        rows = cursor.fetchall()
        for row in rows:
            # Converting sqlite3.Row to a standard Python dictionary
            student_dict = {
                "Student ID": row["student_id"],
                "Name": row["name"],
                "Age": row["age"],
                "Gender": row["gender"],
                "Department": row["department"],
                "Email": row["email"],
                "Phone": row["phone"]
            }
            students_list.append(student_dict)

        return students_list
    except sqlite3.Error as error:
        print(f"Error fetching students: {error}")
        return []
    finally:
        if conn:
            conn.close()


def search_student_by_id(student_id: str) -> dict | None:
    """
    Searches for a single student by their unique Student ID.
    
    Returns:
        dict: Student details if found, or None if no match is found.
    """
    cleaned_id = str(student_id).strip()
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM students WHERE student_id = ?;"
        cursor.execute(query, (cleaned_id,))
        row = cursor.fetchone()

        if row:
            return dict(row)
        return None
    except sqlite3.Error as error:
        print(f"Error searching student by ID: {error}")
        return None
    finally:
        if conn:
            conn.close()


def search_students_by_name(name_query: str) -> list[dict]:
    """
    Searches for students whose name contains the search term (case-insensitive).
    
    Demonstrates:
    - SQL 'LIKE' operator with wildcard '%'
    """
    search_term = f"%{name_query.strip()}%"
    matching_students = []
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT * FROM students 
            WHERE LOWER(name) LIKE LOWER(?) 
            ORDER BY name ASC;
        """
        cursor.execute(query, (search_term,))
        rows = cursor.fetchall()

        for row in rows:
            matching_students.append(dict(row))

        return matching_students
    except sqlite3.Error as error:
        print(f"Error searching students by name: {error}")
        return []
    finally:
        if conn:
            conn.close()


def update_student(student: Student) -> tuple[bool, str]:
    """
    Updates an existing student's personal and academic details.
    
    Demonstrates:
    - SQL 'UPDATE ... SET ... WHERE' statement.
    """
    # Validate before updating
    is_valid, validation_msg = student.validate()
    if not is_valid:
        return False, validation_msg

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE students
            SET name = ?, age = ?, gender = ?, department = ?, email = ?, phone = ?
            WHERE student_id = ?;
        """
        cursor.execute(query, (
            student.name,
            student.age,
            student.gender,
            student.department,
            student.email,
            student.phone,
            student.student_id
        ))

        # rowcount tells us how many rows were actually modified
        if cursor.rowcount == 0:
            return False, f"No student found with ID '{student.student_id}' to update."

        conn.commit()
        return True, f"Student '{student.student_id}' updated successfully!"

    except sqlite3.Error as error:
        return False, f"Database error during update: {error}"
    finally:
        if conn:
            conn.close()


def delete_student(student_id: str) -> tuple[bool, str]:
    """
    Deletes a student record from the database.
    Because Foreign Keys with CASCADE are enabled, deleting a student will
    also automatically delete their marks and attendance records.
    
    Demonstrates:
    - SQL 'DELETE FROM students WHERE student_id = ?'
    """
    cleaned_id = str(student_id).strip()
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "DELETE FROM students WHERE student_id = ?;"
        cursor.execute(query, (cleaned_id,))

        if cursor.rowcount == 0:
            return False, f"No student found with ID '{cleaned_id}'."

        conn.commit()
        return True, f"Student '{cleaned_id}' and all associated records deleted successfully."

    except sqlite3.Error as error:
        return False, f"Database error during deletion: {error}"
    finally:
        if conn:
            conn.close()


def get_all_student_ids() -> list[str]:
    """
    Helper function that returns a simple list of all student IDs.
    Useful for population of dropdown menus in Marks and Attendance modules.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT student_id, name FROM students ORDER BY student_id ASC;")
        rows = cursor.fetchall()
        # Return format: ["CS101 - Alex Johnson", "CS102 - Sophia Martinez"]
        return [f"{row['student_id']} - {row['name']}" for row in rows]
    except sqlite3.Error:
        return []
    finally:
        if conn:
            conn.close()


def get_total_student_count() -> int:
    """
    Returns the total number of students currently registered.
    Used on the Dashboard page.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM students;")
        row = cursor.fetchone()
        return int(row["total"]) if row else 0
    except sqlite3.Error:
        return 0
    finally:
        if conn:
            conn.close()


def get_department_distribution() -> dict:
    """
    Returns a dictionary mapping each department to its student count.
    Used for plotting the Department-wise chart on the Dashboard.
    
    Example output:
    {'Computer Science': 2, 'Electronics': 1, 'Mechanical': 1}
    """
    dept_counts = {}
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT department, COUNT(*) AS count 
            FROM students 
            GROUP BY department 
            ORDER BY count DESC;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            dept_counts[row["department"]] = row["count"]
        return dept_counts
    except sqlite3.Error:
        return {}
    finally:
        if conn:
            conn.close()
