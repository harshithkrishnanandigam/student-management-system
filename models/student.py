# ==============================================================================
# File: models/student.py
# Purpose: Student Data Model (Object-Oriented Programming)
# ==============================================================================
#
# PYTHON CONCEPTS DEMONSTRATED IN THIS FILE:
# 1. Classes and Objects: Defining a blueprint (class) and creating instances (objects).
# 2. Encapsulation: Grouping student attributes and related methods into a single unit.
# 3. Special Methods (Dunder Methods): '__init__' for initialization, '__str__' for printing.
# 4. Data Types: Strings, Integers, Dictionaries, and Lists.
# 5. Conditional Statements: Data validation logic using if-elif-else.
# ==============================================================================

class Student:
    """
    The Student class represents a real-world student in an academic institution.
    
    Why use a Class?
    ----------------
    Without classes, we would have to manage multiple separate variables for every student:
        student1_id, student1_name, student1_age, student2_id, student2_name...
    With a class, we define a blueprint once, and we can create as many Student objects
    as we need, each holding its own state and behavior.
    """

    def __init__(self, student_id: str, name: str, age: int, gender: str, 
                 department: str, email: str, phone: str):
        """
        The Constructor Method (__init__):
        Automatically runs whenever a new Student object is created.
        
        'self':
            Refers to the specific instance of the class being created.
            It allows us to attach variables directly to that individual object.
        """
        # Instance Attributes (Variables belonging to this specific student)
        self.student_id = str(student_id).strip()
        self.name = str(name).strip()
        self.age = int(age)
        self.gender = str(gender).strip()
        self.department = str(department).strip()
        self.email = str(email).strip()
        self.phone = str(phone).strip()

    def validate(self) -> tuple[bool, str]:
        """
        Validates the student's data fields before saving to the database.
        
        Concept Demonstrated:
        - Conditional statements (if / not)
        - Basic string operations (.isdigit(), in operator)
        - Returning tuples (is_valid: bool, error_message: str)
        """
        if not self.student_id:
            return False, "Student ID cannot be empty."

        if not self.name:
            return False, "Student Name cannot be empty."

        if self.age <= 0 or self.age > 120:
            return False, "Age must be a valid positive number between 1 and 120."

        if not self.gender:
            return False, "Please select a gender."

        if not self.department:
            return False, "Department cannot be empty."

        # Simple email format check
        if "@" not in self.email or "." not in self.email:
            return False, "Please enter a valid email address (e.g., student@university.edu)."

        # Simple phone number validation (must contain at least 7 digits)
        digits_only = [char for char in self.phone if char.isdigit()]
        if len(digits_only) < 7:
            return False, "Phone number must contain at least 7 digits."

        return True, "Validation successful."

    def to_dict(self) -> dict:
        """
        Converts the Student object's attributes into a standard Python dictionary.
        
        Why is this useful?
        -------------------
        Dictionaries are very easy to pass into pandas DataFrames, JSON serializers,
        and Streamlit display tables.
        """
        return {
            "Student ID": self.student_id,
            "Name": self.name,
            "Age": self.age,
            "Gender": self.gender,
            "Department": self.department,
            "Email": self.email,
            "Phone": self.phone
        }

    @classmethod
    def from_row(cls, row):
        """
        Class Method (Factory Pattern):
        Constructs a Student instance directly from a database row tuple or sqlite3.Row.
        
        Expected row order:
        (student_id, name, age, gender, department, email, phone)
        """
        return cls(
            student_id=row[0],
            name=row[1],
            age=row[2],
            gender=row[3],
            department=row[4],
            email=row[5],
            phone=row[6]
        )

    def __str__(self) -> str:
        """
        String Representation:
        Defines how this object is printed when passed to print(student_obj) or str(student_obj).
        """
        return f"Student(ID: {self.student_id}, Name: '{self.name}', Dept: {self.department})"
