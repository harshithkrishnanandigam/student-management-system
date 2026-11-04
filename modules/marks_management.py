# ==============================================================================
# File: modules/marks_management.py
# Purpose: Business Logic for Student Academic Marks & Grade Evaluation
# ==============================================================================
#
# PYTHON CONCEPTS DEMONSTRATED IN THIS FILE:
# 1. Conditional Logic: if-elif-else statements for academic grading.
# 2. Arithmetic Operations: Calculating totals, averages, and percentages.
# 3. Aggregations & Loops: Iterating through lists of subject scores.
# 4. Sorting with Lambdas: Sorting student dictionaries by score using Python's sort().
# 5. SQLite Joins: Combining the 'students' and 'marks' tables in a single SQL query.
# 6. Default Arguments: Functions with default parameters (e.g., max_marks=100.0).
# ==============================================================================

import sqlite3
from database import get_connection


def calculate_grade(percentage: float) -> tuple[str, str]:
    """
    Determines letter grade and academic standing based on overall percentage.
    
    Demonstrates:
    - Conditional statements (if-elif-else ladder)
    - Returning tuples (grade_letter, descriptive_status)
    
    Grading Scale:
        >= 90% : A+ (Outstanding)
        >= 80% : A  (Excellent)
        >= 70% : B  (Very Good)
        >= 60% : C  (Good)
        >= 50% : D  (Pass)
        <  50% : F  (Fail)
    """
    if percentage >= 90.0:
        return "A+", "Outstanding"
    elif percentage >= 80.0:
        return "A", "Excellent"
    elif percentage >= 70.0:
        return "B", "Very Good"
    elif percentage >= 60.0:
        return "C", "Good"
    elif percentage >= 50.0:
        return "D", "Pass"
    else:
        return "F", "Fail"


def add_or_update_marks(student_id: str, subject: str, 
                        marks_obtained: float, max_marks: float = 100.0) -> tuple[bool, str]:
    """
    Inserts a new subject mark or updates the score if the subject already exists
    for the specified student.
    
    Parameters:
        student_id (str): ID of the student.
        subject (str): Name of the academic subject.
        marks_obtained (float): Marks scored by the student.
        max_marks (float): Maximum possible marks (default is 100).
        
    Returns:
        tuple (bool, str): (Success flag, descriptive message).
    """
    cleaned_id = str(student_id).strip()
    cleaned_subject = str(subject).strip()

    # Input Validation using Conditional Statements
    if not cleaned_id:
        return False, "Student ID cannot be empty."
    if not cleaned_subject:
        return False, "Subject name cannot be empty."
    if marks_obtained < 0:
        return False, "Marks obtained cannot be negative."
    if marks_obtained > max_marks:
        return False, f"Marks obtained ({marks_obtained}) cannot exceed maximum marks ({max_marks})."
    if max_marks <= 0:
        return False, "Maximum marks must be greater than zero."

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check if marks for this student and subject already exist
        check_query = "SELECT id FROM marks WHERE student_id = ? AND LOWER(subject) = LOWER(?);"
        cursor.execute(check_query, (cleaned_id, cleaned_subject))
        existing_record = cursor.fetchone()

        if existing_record:
            # Record already exists -> UPDATE it
            update_query = """
                UPDATE marks 
                SET marks_obtained = ?, max_marks = ?
                WHERE id = ?;
            """
            cursor.execute(update_query, (marks_obtained, max_marks, existing_record["id"]))
            action = "updated"
        else:
            # No existing record -> INSERT new row
            insert_query = """
                INSERT INTO marks (student_id, subject, marks_obtained, max_marks)
                VALUES (?, ?, ?, ?);
            """
            cursor.execute(insert_query, (cleaned_id, cleaned_subject, marks_obtained, max_marks))
            action = "added"

        conn.commit()
        return True, f"Marks for '{cleaned_subject}' {action} successfully for Student {cleaned_id}."

    except sqlite3.IntegrityError:
        return False, f"Could not record marks. Please verify that Student ID '{cleaned_id}' exists in the database."
    except sqlite3.Error as error:
        return False, f"Database error while saving marks: {error}"
    finally:
        if conn:
            conn.close()


def get_student_marks(student_id: str) -> list[dict]:
    """
    Fetches all individual subject marks recorded for a single student.
    
    Returns:
        list of dicts, where each dict represents one subject score.
    """
    cleaned_id = str(student_id).strip()
    marks_list = []
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT id, subject, marks_obtained, max_marks 
            FROM marks 
            WHERE student_id = ? 
            ORDER BY subject ASC;
        """
        cursor.execute(query, (cleaned_id,))
        rows = cursor.fetchall()

        for row in rows:
            obtained = float(row["marks_obtained"])
            maximum = float(row["max_marks"])
            pct = (obtained / maximum) * 100.0 if maximum > 0 else 0.0
            grade, _ = calculate_grade(pct)

            marks_list.append({
                "ID": row["id"],
                "Subject": row["subject"],
                "Marks Obtained": obtained,
                "Max Marks": maximum,
                "Percentage (%)": round(pct, 2),
                "Grade": grade
            })

        return marks_list
    except sqlite3.Error as error:
        print(f"Error fetching marks for student: {error}")
        return []
    finally:
        if conn:
            conn.close()


def calculate_student_summary(student_id: str) -> dict:
    """
    Calculates total marks, average marks, overall percentage, and final grade.
    
    Demonstrates:
    - Looping over a list
    - Accumulator variables (total_obtained, total_max)
    - Handling division-by-zero safely
    - Nested dictionary return structure
    """
    marks = get_student_marks(student_id)

    if not marks:
        return {
            "has_data": False,
            "subject_count": 0,
            "total_obtained": 0.0,
            "total_max": 0.0,
            "average_percentage": 0.0,
            "grade": "N/A",
            "standing": "No marks recorded yet"
        }

    # Accumulator variables
    total_obtained = 0.0
    total_max = 0.0

    # For loop to calculate cumulative sums
    for item in marks:
        total_obtained += item["Marks Obtained"]
        total_max += item["Max Marks"]

    # Calculate percentage safely
    if total_max > 0:
        overall_percentage = (total_obtained / total_max) * 100.0
    else:
        overall_percentage = 0.0

    grade, standing = calculate_grade(overall_percentage)

    return {
        "has_data": True,
        "subject_count": len(marks),
        "total_obtained": round(total_obtained, 2),
        "total_max": round(total_max, 2),
        "average_percentage": round(overall_percentage, 2),
        "grade": grade,
        "standing": standing
    }


def get_all_marks_records() -> list[dict]:
    """
    Retrieves all marks records across all students, joined with student names.
    
    Demonstrates:
    - SQL INNER JOIN: Combines rows from two tables ('marks' and 'students') based
      on a matching column ('student_id').
    """
    records = []
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                m.id,
                s.student_id,
                s.name,
                s.department,
                m.subject,
                m.marks_obtained,
                m.max_marks
            FROM marks m
            INNER JOIN students s ON m.student_id = s.student_id
            ORDER BY s.student_id ASC, m.subject ASC;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            obtained = float(row["marks_obtained"])
            maximum = float(row["max_marks"])
            pct = (obtained / maximum) * 100.0 if maximum > 0 else 0.0
            grade, _ = calculate_grade(pct)

            records.append({
                "Mark ID": row["id"],
                "Student ID": row["student_id"],
                "Name": row["name"],
                "Department": row["department"],
                "Subject": row["subject"],
                "Marks Obtained": obtained,
                "Max Marks": maximum,
                "Percentage (%)": round(pct, 2),
                "Grade": grade
            })

        return records
    except sqlite3.Error as error:
        print(f"Error fetching all marks records: {error}")
        return []
    finally:
        if conn:
            conn.close()


def delete_mark_entry(mark_id: int) -> tuple[bool, str]:
    """
    Deletes a specific subject mark record by its primary key ID.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM marks WHERE id = ?;", (mark_id,))
        if cursor.rowcount == 0:
            return False, "Mark entry not found."
        conn.commit()
        return True, "Mark entry deleted successfully."
    except sqlite3.Error as error:
        return False, f"Database error: {error}"
    finally:
        if conn:
            conn.close()


def get_top_performing_students(limit: int = 5) -> list[dict]:
    """
    Computes the academic rankings and returns the top N performing students.
    
    Demonstrates:
    - Dictionaries used for grouping data
    - Python loops and conditional lookups
    - Higher-order sorting: sorted(list, key=lambda x: ..., reverse=True)
    - List slicing: [:limit]
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Step 1: Query all student IDs and names
        cursor.execute("SELECT student_id, name, department FROM students;")
        students = cursor.fetchall()

        leaderboard = []

        # Step 2: Loop through each student and calculate their summary
        for s in students:
            s_id = s["student_id"]
            summary = calculate_student_summary(s_id)
            
            # Only include students who have at least one subject mark recorded
            if summary["has_data"]:
                leaderboard.append({
                    "Student ID": s_id,
                    "Name": s["name"],
                    "Department": s["department"],
                    "Subjects": summary["subject_count"],
                    "Average (%)": summary["average_percentage"],
                    "Grade": summary["grade"]
                })

        # Step 3: Sort students in descending order of Average (%)
        # 'reverse=True' sorts from highest to lowest
        leaderboard.sort(key=lambda student: student["Average (%)"], reverse=True)

        # Step 4: Return only the top 'limit' students using list slicing
        return leaderboard[:limit]

    except sqlite3.Error as error:
        print(f"Error computing top students: {error}")
        return []
    finally:
        if conn:
            conn.close()
