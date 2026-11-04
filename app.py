# ==============================================================================
# File: app.py
# Purpose: Main Streamlit Application - Student Management System
# UI Theme: Modern Monochrome Dark Minimalist Interface (No Emojis, No Logos)
# ==============================================================================
#
# TECH STACK: Python, Streamlit, SQLite, Object-Oriented Programming (OOP)
#
# PYTHON & STREAMLIT CONCEPTS DEMONSTRATED IN THIS FILE:
# 1. Custom UI Theming & Styling via injected CSS (High-Contrast Monochrome Dark).
# 2. Streamlit UI Elements:
#      - Sidebar navigation (st.sidebar.radio)
#      - Layouts: Columns (st.columns), Tabs (st.tabs), Containers (st.container)
#      - Form controls: st.form, st.text_input, st.number_input, st.selectbox, st.date_input
#      - Metric Cards: st.metric
#      - Tables and DataFrames: st.dataframe
#      - Status Messages: st.success, st.error, st.warning, st.info
# 3. State & Session Management: Handling UI refreshes and form submissions.
# 4. Modular Code Integration: Importing functions and classes from custom packages.
# ==============================================================================

import datetime
import os
import sys
import pandas as pd
import streamlit as st

# Ensure project root directory is included in Python's module search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import database initialization and business logic modules
from database import initialize_database, seed_sample_data
from models.student import Student
from modules.ui_theme import apply_minimal_dark_theme, render_minimal_header
import modules.student_management as sm
import modules.marks_management as mm
import modules.attendance_management as am

# ------------------------------------------------------------------------------
# 1. Page Configuration & Minimalist Dark Theme Activation
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Student Management System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Monochrome Dark Minimalist Design (Pure text, no emojis)
apply_minimal_dark_theme()

# Automatically create database tables and seed starter data if needed
initialize_database()
seed_sample_data()

# ------------------------------------------------------------------------------
# 2. Minimalist Sidebar Navigation (Text-Only)
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="padding: 12px 0 16px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 18px;">
        <div style="font-size: 0.72rem; font-weight: 600; color: #71717a; text-transform: uppercase; letter-spacing: 1.2px;">Academic System</div>
        <div style="font-size: 1.1rem; font-weight: 700; color: #ffffff; letter-spacing: -0.3px; margin-top: 2px;">Student Portal</div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation menu (Pure text, no emojis)
    menu_selection = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Student Management",
            "Marks and Grades",
            "Attendance Tracker",
            "Learning Guide"
        ]
    )

    st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
    
    # System info card in sidebar (clean, typographic)
    total_students_count = sm.get_total_student_count()
    st.markdown(f"""
    <div style="
        background-color: #121215;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 14px;
        font-size: 0.82rem;
    ">
        <div style="color: #71717a; text-transform: uppercase; letter-spacing: 0.8px; font-size: 0.7rem; margin-bottom: 6px;">System Information</div>
        <div style="color: #ffffff; margin-bottom: 4px;">Enrolled Students: <span style="font-weight: 600;">{total_students_count}</span></div>
        <div style="color: #ffffff; margin-bottom: 4px;">Database: <span style="font-weight: 600;">SQLite</span></div>
        <div style="color: #71717a; font-size: 0.75rem; margin-top: 8px;">Computer Science Edition</div>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# SECTION 1: DASHBOARD
# ==============================================================================
if menu_selection == "Dashboard":
    render_minimal_header(
        "Dashboard",
        "Overview of student enrollments, academic performance, and institutional attendance."
    )

    # Metric Cards (Monochrome High-Contrast)
    col1, col2, col3, col4 = st.columns(4)

    # Metric 1: Total Students
    col1.metric("Total Students", total_students_count)

    # Metric 2: Average Attendance
    avg_attendance = am.get_overall_average_attendance()
    col2.metric("Average Attendance", f"{avg_attendance}%")

    # Metric 3: Top Performer
    top_students = mm.get_top_performing_students(limit=1)
    if top_students:
        top_name = top_students[0]["Name"]
        top_avg = f"{top_students[0]['Average (%)']}% ({top_students[0]['Grade']})"
    else:
        top_name = "N/A"
        top_avg = "No records"
    col3.metric("Top Performer", top_name, top_avg)

    # Metric 4: Active Departments
    dept_dist = sm.get_department_distribution()
    col4.metric("Departments", len(dept_dist))

    st.write("")

    # Dashboard Content Layout: Two Main Columns
    dash_col_left, dash_col_right = st.columns([1.2, 1])

    with dash_col_left:
        st.subheader("Top Performing Students")
        top_5 = mm.get_top_performing_students(limit=5)
        if top_5:
            df_top = pd.DataFrame(top_5)
            st.dataframe(df_top, use_container_width=True, hide_index=True)
        else:
            st.info("No marks data recorded yet.")

    with dash_col_right:
        st.subheader("Department Distribution")
        if dept_dist:
            df_dept = pd.DataFrame(list(dept_dist.items()), columns=["Department", "Students"])
            st.bar_chart(df_dept.set_index("Department"))
        else:
            st.info("No students enrolled yet.")


# ==============================================================================
# SECTION 2: STUDENT MANAGEMENT
# ==============================================================================
elif menu_selection == "Student Management":
    render_minimal_header(
        "Student Management",
        "Register, view, search, update, and manage student profiles."
    )

    tab_view, tab_add, tab_search, tab_update, tab_delete = st.tabs([
        "View All",
        "Add Student",
        "Search",
        "Update",
        "Delete"
    ])

    # --------------------------------------------------------------------------
    # Tab 1: View All Students
    # --------------------------------------------------------------------------
    with tab_view:
        st.subheader("Registered Students")
        all_students = sm.get_all_students()

        if all_students:
            df_students = pd.DataFrame(all_students)
            
            all_depts = ["All Departments"] + sorted(list(set(df_students["Department"].dropna())))
            selected_dept = st.selectbox("Department Filter", all_depts)
            
            if selected_dept != "All Departments":
                filtered_df = df_students[df_students["Department"] == selected_dept]
            else:
                filtered_df = df_students

            st.write(f"Displaying {len(filtered_df)} student record(s):")
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        else:
            st.warning("No students currently in the database.")

    # --------------------------------------------------------------------------
    # Tab 2: Add Student
    # --------------------------------------------------------------------------
    with tab_add:
        st.subheader("Register New Student")
        st.info("Enter the student details below. All fields are validated before submission.")

        with st.form("add_student_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)

            with col_a:
                input_id = st.text_input("Student ID", placeholder="e.g. CS106")
                input_name = st.text_input("Full Name", placeholder="e.g. Jane Doe")
                input_age = st.number_input("Age", min_value=15, max_value=80, value=19, step=1)
                input_gender = st.selectbox("Gender", ["Female", "Male", "Other", "Prefer not to say"])

            with col_b:
                input_dept = st.selectbox(
                    "Department",
                    ["Computer Science", "Electronics", "Mechanical", "Civil", "Information Tech", "Biotechnology"]
                )
                input_email = st.text_input("Email Address", placeholder="jane.doe@university.edu")
                input_phone = st.text_input("Phone Number", placeholder="e.g. 555-0199")

            submit_add = st.form_submit_button("Register Student", use_container_width=True)

            if submit_add:
                new_student = Student(
                    student_id=input_id,
                    name=input_name,
                    age=input_age,
                    gender=input_gender,
                    department=input_dept,
                    email=input_email,
                    phone=input_phone
                )

                success, message = sm.add_student(new_student)
                if success:
                    st.success(message)
                else:
                    st.error(message)

    # --------------------------------------------------------------------------
    # Tab 3: Search Student
    # --------------------------------------------------------------------------
    with tab_search:
        st.subheader("Search Records")
        search_type = st.radio("Search Criteria", ["Student ID", "Student Name"], horizontal=True)

        if search_type == "Student ID":
            search_id = st.text_input("Enter Student ID", placeholder="e.g. CS101")
            if st.button("Search by ID"):
                if search_id.strip():
                    found_student = sm.search_student_by_id(search_id)
                    if found_student:
                        st.success(f"Record found for Student ID: {search_id}")
                        
                        with st.container(border=True):
                            c1, c2 = st.columns(2)
                            c1.write(f"**Student ID:** {found_student['student_id']}")
                            c1.write(f"**Name:** {found_student['name']}")
                            c1.write(f"**Age:** {found_student['age']}")
                            c1.write(f"**Gender:** {found_student['gender']}")

                            c2.write(f"**Department:** {found_student['department']}")
                            c2.write(f"**Email:** {found_student['email']}")
                            c2.write(f"**Phone:** {found_student['phone']}")
                    else:
                        st.error(f"No student found with ID '{search_id}'.")
                else:
                    st.warning("Please enter a Student ID to search.")

        else:
            search_name = st.text_input("Enter Student Name", placeholder="e.g. Alex")
            if st.button("Search by Name"):
                if search_name.strip():
                    results = sm.search_students_by_name(search_name)
                    if results:
                        st.success(f"Found {len(results)} matching record(s):")
                        st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
                    else:
                        st.error(f"No students found matching '{search_name}'.")
                else:
                    st.warning("Please enter a name to search.")

    # --------------------------------------------------------------------------
    # Tab 4: Update Student
    # --------------------------------------------------------------------------
    with tab_update:
        st.subheader("Update Student Information")
        student_options = sm.get_all_student_ids()

        if student_options:
            selected_option = st.selectbox("Select Student to Update", student_options, key="update_select")
            selected_id = selected_option.split(" - ")[0]
            current_data = sm.search_student_by_id(selected_id)

            if current_data:
                with st.form("update_student_form"):
                    st.write(f"Editing: **{current_data['name']}** (ID: `{selected_id}`)")
                    u_col1, u_col2 = st.columns(2)

                    with u_col1:
                        new_name = st.text_input("Full Name", value=current_data["name"])
                        new_age = st.number_input("Age", min_value=15, max_value=80, value=int(current_data["age"]))
                        
                        gender_list = ["Female", "Male", "Other", "Prefer not to say"]
                        default_gender_idx = gender_list.index(current_data["gender"]) if current_data["gender"] in gender_list else 0
                        new_gender = st.selectbox("Gender", gender_list, index=default_gender_idx)

                    with u_col2:
                        dept_list = ["Computer Science", "Electronics", "Mechanical", "Civil", "Information Tech", "Biotechnology"]
                        default_dept_idx = dept_list.index(current_data["department"]) if current_data["department"] in dept_list else 0
                        new_dept = st.selectbox("Department", dept_list, index=default_dept_idx)

                        new_email = st.text_input("Email", value=current_data["email"])
                        new_phone = st.text_input("Phone", value=current_data["phone"])

                    submit_update = st.form_submit_button("Save Changes", use_container_width=True)

                    if submit_update:
                        updated_student = Student(
                            student_id=selected_id,
                            name=new_name,
                            age=new_age,
                            gender=new_gender,
                            department=new_dept,
                            email=new_email,
                            phone=new_phone
                        )
                        success, msg = sm.update_student(updated_student)
                        if success:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
        else:
            st.info("No students available to update.")

    # --------------------------------------------------------------------------
    # Tab 5: Delete Student
    # --------------------------------------------------------------------------
    with tab_delete:
        st.subheader("Delete Student")
        st.warning("Warning: Removing a student permanently deletes their associated marks and attendance records.")

        del_options = sm.get_all_student_ids()
        if del_options:
            selected_del = st.selectbox("Select Student to Delete", del_options, key="delete_select")
            del_id = selected_del.split(" - ")[0]

            confirm_check = st.checkbox(f"Confirm permanent deletion of {selected_del}")
            if st.button("Delete Student", type="primary", disabled=not confirm_check):
                success, msg = sm.delete_student(del_id)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
        else:
            st.info("No students available to delete.")


# ==============================================================================
# SECTION 3: MARKS AND GRADES MANAGEMENT
# ==============================================================================
elif menu_selection == "Marks and Grades":
    render_minimal_header(
        "Marks and Grades",
        "Record subject marks, calculate student averages, and generate academic report cards."
    )

    tab_add_marks, tab_report_card, tab_all_marks = st.tabs([
        "Record Marks",
        "Report Card",
        "Marks Ledger"
    ])

    # --------------------------------------------------------------------------
    # Tab 1: Record Marks
    # --------------------------------------------------------------------------
    with tab_add_marks:
        st.subheader("Record Subject Marks")
        students_list = sm.get_all_student_ids()

        if students_list:
            with st.form("marks_form", clear_on_submit=False):
                col_m1, col_m2 = st.columns(2)

                with col_m1:
                    chosen_student = st.selectbox("Select Student", students_list)
                    subject_choice = st.selectbox(
                        "Subject",
                        [
                            "Python Programming",
                            "Data Structures",
                            "Mathematics I",
                            "Digital Logic",
                            "Database Systems",
                            "Web Development",
                            "Computer Networks",
                            "Operating Systems",
                            "Other (Custom)"
                        ]
                    )
                    if subject_choice == "Other (Custom)":
                        custom_subject = st.text_input("Enter Subject Name")
                    else:
                        custom_subject = subject_choice

                with col_m2:
                    marks_val = st.number_input("Marks Obtained", min_value=0.0, max_value=100.0, value=75.0, step=1.0)
                    max_val = st.number_input("Maximum Marks", min_value=10.0, max_value=500.0, value=100.0, step=10.0)

                submit_marks = st.form_submit_button("Save Marks", use_container_width=True)

                if submit_marks:
                    stud_id = chosen_student.split(" - ")[0]
                    subject_to_save = custom_subject.strip() if custom_subject else ""
                    success, msg = mm.add_or_update_marks(stud_id, subject_to_save, marks_val, max_val)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
        else:
            st.info("Please register students first before recording marks.")

    # --------------------------------------------------------------------------
    # Tab 2: Report Card
    # --------------------------------------------------------------------------
    with tab_report_card:
        st.subheader("Academic Report Card")
        students_list = sm.get_all_student_ids()

        if students_list:
            chosen_rep = st.selectbox("Select Student", students_list, key="rep_card_select")
            selected_rep_id = chosen_rep.split(" - ")[0]

            student_info = sm.search_student_by_id(selected_rep_id)
            summary = mm.calculate_student_summary(selected_rep_id)
            subject_marks = mm.get_student_marks(selected_rep_id)

            if summary["has_data"]:
                with st.container(border=True):
                    col_info1, col_info2 = st.columns(2)
                    col_info1.write(f"**Student ID:** `{student_info['student_id']}`")
                    col_info1.write(f"**Name:** {student_info['name']}")
                    col_info1.write(f"**Department:** {student_info['department']}")

                    col_info2.write(f"**Total Subjects:** {summary['subject_count']}")
                    col_info2.write(f"**Email:** {student_info['email']}")
                    col_info2.write(f"**Phone:** {student_info['phone']}")

                st.write("")
                met1, met2, met3, met4 = st.columns(4)
                met1.metric("Marks Scored", f"{summary['total_obtained']} / {summary['total_max']}")
                met2.metric("Overall Percentage", f"{summary['average_percentage']}%")
                met3.metric("Final Grade", summary["grade"])
                met4.metric("Standing", summary["standing"])

                st.write("### Subject Breakdown")
                st.dataframe(pd.DataFrame(subject_marks), use_container_width=True, hide_index=True)
            else:
                st.info(f"No marks recorded yet for Student ID: {selected_rep_id}")
        else:
            st.info("No students enrolled.")

    # --------------------------------------------------------------------------
    # Tab 3: Marks Ledger
    # --------------------------------------------------------------------------
    with tab_all_marks:
        st.subheader("Marks Ledger")
        all_marks = mm.get_all_marks_records()
        if all_marks:
            st.dataframe(pd.DataFrame(all_marks), use_container_width=True, hide_index=True)
        else:
            st.info("No marks records exist in the database.")


# ==============================================================================
# SECTION 4: ATTENDANCE TRACKER
# ==============================================================================
elif menu_selection == "Attendance Tracker":
    render_minimal_header(
        "Attendance Tracker",
        "Record and monitor daily student attendance rates and requirements."
    )

    tab_mark_att, tab_student_att, tab_all_att = st.tabs([
        "Mark Attendance",
        "Student History",
        "Class Summary"
    ])

    # --------------------------------------------------------------------------
    # Tab 1: Mark Attendance
    # --------------------------------------------------------------------------
    with tab_mark_att:
        st.subheader("Daily Attendance")
        students_list = sm.get_all_student_ids()

        if students_list:
            with st.form("mark_attendance_form"):
                col_at1, col_at2 = st.columns(2)

                with col_at1:
                    att_student = st.selectbox("Select Student", students_list)
                    att_date = st.date_input("Date", value=datetime.date.today())

                with col_at2:
                    att_status = st.radio("Status", ["Present", "Absent"], horizontal=True)

                submit_att = st.form_submit_button("Record Attendance", use_container_width=True)

                if submit_att:
                    att_id = att_student.split(" - ")[0]
                    date_str = att_date.strftime("%Y-%m-%d")
                    success, msg = am.mark_attendance(att_id, date_str, att_status)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
        else:
            st.info("No students enrolled. Add students to record attendance.")

    # --------------------------------------------------------------------------
    # Tab 2: Individual Student Attendance History
    # --------------------------------------------------------------------------
    with tab_student_att:
        st.subheader("Student Attendance History")
        students_list = sm.get_all_student_ids()

        if students_list:
            chosen_att_stud = st.selectbox("Select Student", students_list, key="ind_att_select")
            stud_id = chosen_att_stud.split(" - ")[0]

            stats = am.calculate_attendance_percentage(stud_id)
            records = am.get_attendance_for_student(stud_id)

            if stats["has_data"]:
                c_stat1, c_stat2, c_stat3, c_stat4 = st.columns(4)
                c_stat1.metric("Attendance Rate", f"{stats['percentage']}%")
                c_stat2.metric("Total Sessions", stats["total_days"])
                c_stat3.metric("Present Days", stats["present_days"])
                c_stat4.metric("Absent Days", stats["absent_days"])

                if stats["percentage"] < 75.0:
                    st.warning("Notice: Attendance is below the required 75% threshold.")
                else:
                    st.success("Good Standing: Attendance meets standard institutional requirements.")

                st.write("### Attendance Logs")
                st.dataframe(pd.DataFrame(records), use_container_width=True, hide_index=True)
            else:
                st.info(f"No attendance records logged for Student ID: {stud_id}")
        else:
            st.info("No students enrolled.")

    # --------------------------------------------------------------------------
    # Tab 3: Class Attendance Summary
    # --------------------------------------------------------------------------
    with tab_all_att:
        st.subheader("Class Attendance Summary")
        summary_table = am.get_all_students_attendance_summary()
        if summary_table:
            st.dataframe(pd.DataFrame(summary_table), use_container_width=True, hide_index=True)
        else:
            st.info("No attendance data found.")


# ==============================================================================
# SECTION 5: LEARNING GUIDE
# ==============================================================================
elif menu_selection == "Learning Guide":
    render_minimal_header(
        "Python Programming Learning Guide",
        "Overview of how core Computer Science and Python concepts are implemented in this application."
    )

    concept_tab1, concept_tab2, concept_tab3, concept_tab4, concept_tab5 = st.tabs([
        "1. Classes & OOP",
        "2. SQLite CRUD",
        "3. Lists & Dictionaries",
        "4. Conditionals & Loops",
        "5. Exception Handling"
    ])

    with concept_tab1:
        st.subheader("1. Object-Oriented Programming (OOP)")
        st.markdown("""
        ### Why do we use Classes?
        In Python, a **Class** is a blueprint for creating objects.
        Instead of keeping 7 separate variables for every student, we bundle data and methods together:
        """)
        st.code("""
# From models/student.py:
class Student:
    def __init__(self, student_id, name, age, gender, department, email, phone):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.gender = gender
        self.department = department
        self.email = email
        self.phone = phone

    def validate(self):
        # Encapsulates data validation inside the class
        if not self.student_id:
            return False, "Student ID cannot be empty."
        return True, "Valid"
        """, language="python")

    with concept_tab2:
        st.subheader("2. SQLite & CRUD Operations")
        st.markdown("""
        **CRUD** stands for **Create, Read, Update, Delete**:
        - **C**reate: `INSERT INTO students (...) VALUES (?, ...)`
        - **R**ead: `SELECT * FROM students WHERE student_id = ?`
        - **U**pdate: `UPDATE students SET name = ? WHERE student_id = ?`
        - **D**elete: `DELETE FROM students WHERE student_id = ?`
        
        ### Security Best Practice: Parameterized Queries
        Arguments are passed with `?` placeholders instead of concatenating strings to prevent SQL Injection.
        """)
        st.code("""
# Safe Parameterized Execution:
cursor.execute("SELECT * FROM students WHERE student_id = ?;", (student_id,))
        """, language="python")

    with concept_tab3:
        st.subheader("3. Lists and Dictionaries")
        st.markdown("""
        - **List (`[]`)**: Ordered collection used to hold multiple student records or subject marks.
        - **Dictionary (`{}`)**: Key-value pairs used to represent each student's attributes.
        """)
        st.code("""
# Converting database rows into a list of dictionaries:
students_list = []
for row in cursor.fetchall():
    student_dict = {
        "Student ID": row["student_id"],
        "Name": row["name"],
        "Department": row["department"]
    }
    students_list.append(student_dict)
        """, language="python")

    with concept_tab4:
        st.subheader("4. Conditionals & Loops")
        st.markdown("""
        - **Conditional Statements (`if-elif-else`)**: Used to determine academic letter grades and validation checks.
        - **Loops (`for` / `while`)**: Used to accumulate totals, calculate average marks, and count present attendance days.
        """)
        st.code("""
# From modules/marks_management.py:
if percentage >= 90.0:
    grade = "A+"
elif percentage >= 80.0:
    grade = "A"
elif percentage >= 70.0:
    grade = "B"
else:
    grade = "F"
        """, language="python")

    with concept_tab5:
        st.subheader("5. Exception Handling")
        st.markdown("""
        Using `try-except-finally` blocks prevents the application from crashing
        when unexpected errors occur (such as duplicate primary keys or database disconnects).
        """)
        st.code("""
conn = None
try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(...)
    conn.commit()
except sqlite3.IntegrityError:
    # Handles duplicate primary keys gracefully
    return False, "Record already exists."
except sqlite3.Error as error:
    return False, f"Database error: {error}"
finally:
    # The finally block always runs to close connections and prevent resource leaks
    if conn:
        conn.close()
        """, language="python")
