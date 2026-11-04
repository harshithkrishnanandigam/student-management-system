# ==============================================================================
# File: modules/attendance_management.py
# Purpose: Business Logic for Recording & Analyzing Student Attendance
# ==============================================================================
#
# PYTHON CONCEPTS DEMONSTRATED IN THIS FILE:
# 1. Date Handling: Formatting and querying ISO date strings (YYYY-MM-DD).
# 2. Loops & Counting: Counting occurrences of 'Present' vs 'Absent'.
# 3. Ratio & Percentage Arithmetic: Calculating attendance percentages.
# 4. UPSERT Logic: Handling duplicate attendance entries for the same student on the same date.
# 5. SQL Joins & Aggregations: Joining attendance with student profile data.
# ==============================================================================

import sqlite3
from database import get_connection


def mark_attendance(student_id: str, date_str: str, status: str) -> tuple[bool, str]:
    """
    Records or updates a student's attendance for a given date.
    
    Parameters:
        student_id (str): The unique ID of the student.
        date_str (str): Date in 'YYYY-MM-DD' format.
        status (str): Either 'Present' or 'Absent'.
        
    Returns:
        tuple (bool, str): (Success flag, descriptive message).
    """
    cleaned_id = str(student_id).strip()
    cleaned_date = str(date_str).strip()
    cleaned_status = str(status).strip()

    # Validation
    if not cleaned_id:
        return False, "Student ID cannot be empty."
    if not cleaned_date:
        return False, "Date cannot be empty."
    if cleaned_status not in ["Present", "Absent"]:
        return False, "Attendance status must be either 'Present' or 'Absent'."

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check if attendance is already recorded for this student on this date
        check_query = "SELECT id FROM attendance WHERE student_id = ? AND date = ?;"
        cursor.execute(check_query, (cleaned_id, cleaned_date))
        existing_record = cursor.fetchone()

        if existing_record:
            # Update the existing status
            update_query = "UPDATE attendance SET status = ? WHERE id = ?;"
            cursor.execute(update_query, (cleaned_status, existing_record["id"]))
            action = "updated to"
        else:
            # Insert a new attendance record
            insert_query = "INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?);"
            cursor.execute(insert_query, (cleaned_id, cleaned_date, cleaned_status))
            action = "marked as"

        conn.commit()
        return True, f"Attendance for Student {cleaned_id} on {cleaned_date} {action} {cleaned_status}."

    except sqlite3.IntegrityError:
        return False, f"Integrity error: Ensure Student ID '{cleaned_id}' exists in the database."
    except sqlite3.Error as error:
        return False, f"Database error while recording attendance: {error}"
    finally:
        if conn:
            conn.close()


def get_attendance_for_student(student_id: str) -> list[dict]:
    """
    Retrieves all attendance date records for a specific student.
    
    Returns:
        list of dicts sorted by date in descending order (most recent first).
    """
    cleaned_id = str(student_id).strip()
    records = []
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT id, date, status 
            FROM attendance 
            WHERE student_id = ? 
            ORDER BY date DESC;
        """
        cursor.execute(query, (cleaned_id,))
        rows = cursor.fetchall()

        for row in rows:
            records.append({
                "Record ID": row["id"],
                "Date": row["date"],
                "Status": row["status"]
            })

        return records
    except sqlite3.Error as error:
        print(f"Error fetching attendance for student: {error}")
        return []
    finally:
        if conn:
            conn.close()


def calculate_attendance_percentage(student_id: str) -> dict:
    """
    Calculates the attendance statistics for a single student.
    
    Demonstrates:
    - Counting loop over a list of records
    - Computing percentage: (present / total) * 100
    - Returning structured summary dictionary
    """
    records = get_attendance_for_student(student_id)

    total_sessions = len(records)
    if total_sessions == 0:
        return {
            "has_data": False,
            "total_days": 0,
            "present_days": 0,
            "absent_days": 0,
            "percentage": 0.0
        }

    # Count present days using a Python loop
    present_count = 0
    for record in records:
        if record["Status"] == "Present":
            present_count += 1

    absent_count = total_sessions - present_count
    percentage = (present_count / total_sessions) * 100.0

    return {
        "has_data": True,
        "total_days": total_sessions,
        "present_days": present_count,
        "absent_days": absent_count,
        "percentage": round(percentage, 2)
    }


def get_all_attendance_records() -> list[dict]:
    """
    Retrieves all attendance logs across all students, joined with student names.
    
    Demonstrates:
    - SQL INNER JOIN between 'attendance' and 'students'
    """
    records = []
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                a.id,
                s.student_id,
                s.name,
                s.department,
                a.date,
                a.status
            FROM attendance a
            INNER JOIN students s ON a.student_id = s.student_id
            ORDER BY a.date DESC, s.student_id ASC;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            records.append({
                "ID": row["id"],
                "Student ID": row["student_id"],
                "Name": row["name"],
                "Department": row["department"],
                "Date": row["date"],
                "Status": row["status"]
            })

        return records
    except sqlite3.Error as error:
        print(f"Error fetching all attendance records: {error}")
        return []
    finally:
        if conn:
            conn.close()


def get_all_students_attendance_summary() -> list[dict]:
    """
    Generates a consolidated attendance summary for every student in the system.
    
    Useful for class-wide attendance inspection tables.
    """
    summary_list = []
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT student_id, name, department FROM students ORDER BY student_id ASC;")
        students = cursor.fetchall()

        for s in students:
            s_id = s["student_id"]
            stats = calculate_attendance_percentage(s_id)

            summary_list.append({
                "Student ID": s_id,
                "Name": s["name"],
                "Department": s["department"],
                "Present Days": stats["present_days"],
                "Absent Days": stats["absent_days"],
                "Total Days": stats["total_days"],
                "Attendance (%)": stats["percentage"]
            })

        return summary_list
    except sqlite3.Error as error:
        print(f"Error generating attendance summary: {error}")
        return []
    finally:
        if conn:
            conn.close()


def get_overall_average_attendance() -> float:
    """
    Calculates the grand average attendance percentage across all enrolled students.
    Used for the metric card on the Dashboard.
    """
    summaries = get_all_students_attendance_summary()
    if not summaries:
        return 0.0

    valid_percentages = [item["Attendance (%)"] for item in summaries if item["Total Days"] > 0]
    if not valid_percentages:
        return 0.0

    # Demonstrates sum() and len() built-in Python functions
    average = sum(valid_percentages) / len(valid_percentages)
    return round(average, 2)
