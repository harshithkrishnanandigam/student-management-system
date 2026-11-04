# ==============================================================================
# File: tests/test_core.py
# Purpose: Automated Unit Tests for Student Management System
# ==============================================================================

import os
import sys
import unittest

# Ensure project root is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.student import Student
import modules.marks_management as mm
import modules.attendance_management as am


class TestStudentModel(unittest.TestCase):
    """Unit tests for the Student OOP class and data validation."""

    def test_student_valid_creation(self):
        student = Student(
            student_id="CS901",
            name="Alice Smith",
            age=20,
            gender="Female",
            department="Computer Science",
            email="alice@university.edu",
            phone="555-1234"
        )
        is_valid, msg = student.validate()
        self.assertTrue(is_valid)
        self.assertEqual(student.name, "Alice Smith")

    def test_student_invalid_email(self):
        student = Student("CS902", "Bob", 19, "Male", "IT", "invalid-email", "555-1234")
        is_valid, msg = student.validate()
        self.assertFalse(is_valid)
        self.assertIn("email", msg.lower())

    def test_student_invalid_age(self):
        student = Student("CS903", "Charlie", -5, "Male", "IT", "c@uni.edu", "555-1234")
        is_valid, msg = student.validate()
        self.assertFalse(is_valid)
        self.assertIn("age", msg.lower())


class TestGradeCalculation(unittest.TestCase):
    """Unit tests for academic grade evaluation logic."""

    def test_grade_boundaries(self):
        grade_a_plus, _ = mm.calculate_grade(95.0)
        grade_a, _ = mm.calculate_grade(85.0)
        grade_b, _ = mm.calculate_grade(75.0)
        grade_c, _ = mm.calculate_grade(65.0)
        grade_d, _ = mm.calculate_grade(55.0)
        grade_f, _ = mm.calculate_grade(45.0)

        self.assertEqual(grade_a_plus, "A+")
        self.assertEqual(grade_a, "A")
        self.assertEqual(grade_b, "B")
        self.assertEqual(grade_c, "C")
        self.assertEqual(grade_d, "D")
        self.assertEqual(grade_f, "F")


if __name__ == "__main__":
    unittest.main()
