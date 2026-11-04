# Student Management System (SMS) - Minimalist Dark Edition

A modular, beginner-friendly **Student Management System** built with **Python**, **Streamlit**, and **SQLite**, styled with a high-contrast **Monochrome Dark Interface** inspired by modern developer products (Linear, Raycast, Vercel). Designed specifically for Computer Science students learning Python fundamentals, software architecture, and UI engineering.

---

## UI Design: Minimalist Monochrome Dark
The application interface is styled after modern editorial dark interfaces:
- **Obsidian Dark Canvas**: Deep matte black backdrop (`#09090b`) with subtle ambient gradients.
- **High-Contrast Actions**: Crisp pure-white primary buttons with bold typography.
- **Refined Typography**: Zero emojis and zero cartoon logos; clean text-first hierarchy using modern sans-serif typography.
- **Subtle Hairline Borders**: Fine borders (`rgba(255, 255, 255, 0.08)`) and structured card containers.

## 📖 Project Overview

The **Student Management System** is an educational yet practical desktop web application that allows educational institutions to manage student records, record academic marks, evaluate grades, and monitor daily attendance.

This project avoids unnecessary complexity and over-engineering. Instead, it prioritizes **clean code**, **readability**, and **thorough documentation** so that any beginner can examine the source code and immediately understand how core Python concepts combine to form a real-world software product.

---

## 🌟 Key Features

### 1. 👨‍🎓 Student Management
- **Add Student**: Register students with Student ID, Name, Age, Gender, Department, Email, and Phone Number.
- **View All Students**: Interactive table with sorting and department filtering.
- **Search Student**: Search by **Student ID** or **Name** (case-insensitive substring match).
- **Update Student**: Edit existing student details directly through pre-filled forms.
- **Delete Student**: Safely remove student records with relational cascading deletion (removes associated marks and attendance).

### 2. 📝 Marks & Grade Management
- **Multi-Subject Marks**: Record marks for any subject (Python Programming, Mathematics, Data Structures, etc.).
- **Automated Grade Calculation**: Computes total marks obtained, maximum possible marks, overall percentage, and assigns letter grades:
  - **A+ (>= 90%)**: Outstanding
  - **A (>= 80%)**: Excellent
  - **B (>= 70%)**: Very Good
  - **C (>= 60%)**: Good
  - **D (>= 50%)**: Pass
  - **F (< 50%)**: Fail
- **Student Report Card**: Clean academic summary card displaying detailed subject breakdown and performance standing.

### 3. 📅 Attendance Tracking
- **Daily Attendance Marking**: Mark students as **Present** or **Absent** for any date.
- **Attendance Percentage Calculation**: Automatically computes:
  $$\text{Attendance Rate} = \left( \frac{\text{Present Days}}{\text{Total Sessions}} \right) \times 100$$
- **Low Attendance Warning**: Automatically warns students whose attendance drops below 75%.
- **Class-wide Attendance Summary**: View a class roster with total sessions, present days, and attendance rates.

### 4. 📊 Administrative Dashboard
- **Live Key Metrics**: Total enrolled students, average class attendance percentage, top-performing student, and active department count.
- **Top Performers Leaderboard**: Ranks the highest-achieving students across the institution.
- **Department Distribution Chart**: Visual bar chart representing student count by department.

### 5. 💡 Interactive Learning Mode
- Built-in educational guide in the app UI explaining how each Python concept (OOP, CRUD, Lists, Dictionaries, Conditionals, Loops, Exception Handling) is implemented in this codebase.

---

## 🛠️ Technologies Used

| Technology | Purpose | Why It Was Chosen |
|---|---|---|
| **Python 3.10+** | Core Programming Language | Clean syntax, beginner-friendly, and powerful standard library. |
| **Streamlit** | Web Interface / UI Framework | Turns Python scripts into interactive web apps without needing HTML/CSS/JavaScript. |
| **SQLite3** | Relational Database | Built into Python; serverless, zero configuration, stores data in a single local file. |
| **Pandas** | Tabular Data Handling | Formats database query results into interactive, sortable tables. |

---

## 🗄️ Database Design

The system uses an SQLite relational database located at `database/students.db`. The tables are automatically generated on first launch.

```
       +--------------------+
       |      students      |
       +--------------------+
       | PK: student_id     |<---------+
       |     name           |          |
       |     age            |          |
       |     gender         |          |
       |     department     |          |
       |     email          |          |
       |     phone          |          |
       +--------------------+          |
                 |                     |
                 | (1 to Many)         | (1 to Many)
                 |                     |
                 v                     v
       +--------------------+ +--------------------+
       |       marks        | |     attendance     |
       +--------------------+ +--------------------+
       | PK: id             | | PK: id             |
       | FK: student_id     | | FK: student_id     |
       |     subject        | |     date           |
       |     marks_obtained | |     status         |
       |     max_marks      | +--------------------+
       +--------------------+
```

### 1. `students` Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| `student_id` | `TEXT` | `PRIMARY KEY` | Unique student roll / matriculation ID |
| `name` | `TEXT` | `NOT NULL` | Full student name |
| `age` | `INTEGER` | `NOT NULL` | Age in years |
| `gender` | `TEXT` | `NOT NULL` | Gender |
| `department` | `TEXT` | `NOT NULL` | Academic department / major |
| `email` | `TEXT` | `NOT NULL` | Contact email address |
| `phone` | `TEXT` | `NOT NULL` | Contact phone number |

### 2. `marks` Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Unique record ID |
| `student_id` | `TEXT` | `FOREIGN KEY REFERENCES students` | Associated student |
| `subject` | `TEXT` | `NOT NULL` | Subject name |
| `marks_obtained` | `REAL` | `NOT NULL` | Marks scored |
| `max_marks` | `REAL` | `NOT NULL DEFAULT 100` | Maximum possible marks |

### 3. `attendance` Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Unique record ID |
| `student_id` | `TEXT` | `FOREIGN KEY REFERENCES students` | Associated student |
| `date` | `TEXT` | `NOT NULL` | Date in `YYYY-MM-DD` |
| `status` | `TEXT` | `NOT NULL CHECK('Present' / 'Absent')`| Attendance status |

---

## 📂 Project Directory Structure

```
StudentManagementSystem/
│
├── app.py                      # Main Streamlit web application & UI navigation
├── database.py                 # SQLite connection manager & schema initialization
├── requirements.txt            # Python dependencies (streamlit, pandas)
├── README.md                   # Complete project documentation and guide
│
├── models/
│   ├── __init__.py             # Makes models a Python package
│   └── student.py              # Student OOP class definition with validation
│
├── modules/
│   ├── __init__.py             # Makes modules a Python package
│   ├── student_management.py   # Student CRUD operations
│   ├── marks_management.py     # Marks tracking & GPA/grade calculation
│   └── attendance_management.py# Attendance tracking & percentage logic
│
└── database/
    └── students.db             # Local SQLite database file (created automatically)
```

---

## 💻 Installation & Setup

### Prerequisites
Make sure you have **Python 3.10** or higher installed on your system. You can verify by opening a terminal and running:
```bash
python --version
```

### Step 1: Clone or Open the Project
Navigate into the project directory:
```bash
cd "c:/Users/Harshith Krishna/Desktop/python projects/StudentManagementSystem"
```

### Step 2: Install Required Dependencies
Run `pip` to install the required packages:
```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Application

To start the Student Management System, execute:

```bash
streamlit run app.py
```

Streamlit will launch a local web server and automatically open the application in your default web browser at:
```
http://localhost:8501
```

> **Note**: On the first run, the system automatically creates the database schema and seeds sample student profiles, marks, and attendance so you can explore the application immediately without manual data entry.

---

## 📚 Python Fundamentals Demonstrated in this Project

For students reviewing this code for exam preparation or interviews:

1. **Object-Oriented Programming (OOP)**:
   - File: `models/student.py`
   - Demonstrates: `class Student:`, `__init__(self, ...)`, instance variables, methods, and the `to_dict()` serialization method.

2. **SQLite Database Operations (CRUD)**:
   - Files: `database.py`, `modules/*.py`
   - Demonstrates: Connecting with `sqlite3.connect()`, executing SQL queries with cursors, transactions with `conn.commit()`, and preventing SQL injection with parameterized `?` placeholders.

3. **Data Structures (Lists & Dictionaries)**:
   - Converting database rows into dictionaries and accumulating them in lists for sorting and UI display.

4. **Functions & Modularity**:
   - Splitting responsibilities into separate files (`student_management.py`, `marks_management.py`, `attendance_management.py`) rather than writing all code in a single 1,000-line file.

5. **Control Flow (Loops & Conditionals)**:
   - `if-elif-else` ladders for academic grade calculation.
   - `for` loops for iterating through subject marks and accumulating totals.

6. **Exception Handling**:
   - `try-except-finally` blocks to handle duplicate keys (`sqlite3.IntegrityError`) and release database connections.

---

## 🔮 Future Improvements

Here are ideas for students who want to expand this project further:
- [ ] Export student report cards as downloadable PDF files using `reportlab`.
- [ ] Add student profile photo upload and storage.
- [ ] Add password authentication and role-based access control (Admin vs Student vs Teacher).
- [ ] Add email notifications to alert parents when attendance falls below 75%.
- [ ] Add semester/term filtering for marks.

---

## 📄 License
This project is open-source and intended for educational purposes. Feel free to use, modify, and build upon it for academic coursework and portfolio presentations!
