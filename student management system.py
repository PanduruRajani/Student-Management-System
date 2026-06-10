

-- 1. Create and Initialize Database
CREATE DATABASE IF NOT EXISTS StudentManagementDB;
USE StudentManagementDB;

-- 2. Create Students Table
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    enrollment_date DATE DEFAULT (CURRENT_DATE)
);

-- 3. Create Courses Table
CREATE TABLE IF NOT EXISTS courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    course_code VARCHAR(10) UNIQUE NOT NULL,
    credits INT DEFAULT 3
);

-- 4. Create Enrollments & Grades Table
CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    grade VARCHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    UNIQUE KEY unique_student_course (student_id, course_id)
);


________________________________________
3. Application Source Code (Python Script)
Prerequisites
Before running the code, install the official MySQL driver for Python using your terminal:

Bash

pip install mysql-connector-python


Python Implementation (main.py)
Replace "your_password_here" in the connection configuration block with your actual local MySQL root password.

Python

import mysql.connector
from mysql.connector import Error

class StudentManagementSystem:
    def __init__(self):
        """Initialize database connection parameters and attempt link."""
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="your_password_here",  # <-- Update with your MySQL password
                database="StudentManagementDB"
            )
            self.cursor = self.connection.cursor()
            print("[SUCCESS] Connected securely to StudentManagementDB.")
        except Error as e:
            print(f"[CRITICAL ERROR] Database Connection Failed: {e}")
            exit(1)

    # ==================== STUDENT MANAGMENT METHODS ====================
    def add_student(self, first_name, last_name, email, phone):
        """Insert a new student profile into the system."""
        query = "INSERT INTO students (first_name, last_name, email, phone) VALUES (%s, %s, %s, %s)"
        try:
            self.cursor.execute(query, (first_name, last_name, email, phone))
            self.connection.commit()
            print(f"[SUCCESS] Student '{first_name} {last_name}' registered successfully.")
        except Error as e:
            print(f"[ERROR] Could not insert student: {e}")

    def view_all_students(self):
        """Fetch and print out all student profiles."""
        query = "SELECT * FROM students"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
        if not results:
            print("\n--- No Student Records Found ---")
            return
            
        print("\n" + "="*70 + "\nSTUDENT DIRECTORY\n" + "="*70)
        print(f"{'ID':<5} | {'First Name':<12} | {'Last Name':<12} | {'Email':<25} | {'Phone':<12}")
        print("-" * 70)
        for row in results:
            print(f"{row[0]:<5} | {row[1]:<12} | {row[2]:<12} | {row[3]:<25} | {row[4]:<12}")

    # ==================== COURSE MANAGEMENT METHODS ====================
    def add_course(self, course_name, course_code, credits):
        """Introduce a brand new curriculum track into the database."""
        query = "INSERT INTO courses (course_name, course_code, credits) VALUES (%s, %s, %s)"
        try:
            self.cursor.execute(query, (course_name, course_code, credits))
            self.connection.commit()
            print(f"[SUCCESS] Course '{course_name}' stored with code [{course_code}].")
        except Error as e:
            print(f"[ERROR] Could not insert course: {e}")

    # ==================== ENROLLMENT & GRADING METHODS ====================
    def enroll_student_in_course(self, student_id, course_id):
        """Map a student to a specific academic course code."""
        query = "INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)"
        try:
            self.cursor.execute(query, (student_id, course_id))
            self.connection.commit()
            print(f"[SUCCESS] Student ID {student_id} assigned to Course ID {course_id}.")
        except Error as e:
            print(f"[ERROR] Enrollment execution failed: {e}")

    def assign_grade(self, student_id, course_id, grade):
        """Assign or update a grade for an existing student enrollment."""
        query = "UPDATE enrollments SET grade = %s WHERE student_id = %s AND course_id = %s"
        try:
            self.cursor.execute(query, (grade, student_id, course_id))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                print(f"[SUCCESS] Grade '{grade}' registered for Student {student_id}.")
            else:
                print("[WARNING] Record matching provided Student and Course criteria not found.")
        except Error as e:
            print(f"[ERROR] Grade updates failed: {e}")

    def get_student_report_card(self, student_id):
        """Generate a complete breakdown of courses and performance for a student."""
        query = """
            SELECT s.first_name, s.last_name, c.course_name, c.course_code, e.grade 
            FROM enrollments e
            JOIN students s ON e.student_id = s.student_id
            JOIN courses c ON e.course_id = c.course_id
            WHERE s.student_id = %s
        """
        self.cursor.execute(query, (student_id,))
        results = self.cursor.fetchall()
        
        if not results:
            print(f"\n--- No enrollment or performance profile found for Student ID {student_id} ---")
            return
            
        print(f"\nReport Card For: {results[0][0]} {results[0][1]} (ID: {student_id})")
        print("-" * 50)
        for row in results:
            grade = row[4] if row[4] else "Not Assigned"
            print(f"Code: {row[3]:<8} | Course: {row[2]:<20} | Grade: {grade}")

    def __del__(self):
        """Ensures connections are gracefully closed when system shuts down."""
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("\n[INFO] Database connection terminated gracefully.")

# ==================== INTERACTIVE USER INTERFACE ====================
def main():
    sms = StudentManagementSystem()
    
    while True:
        print("\n" + "#"*40)
        print("  STUDENT MANAGEMENT SYSTEM PORTAL  ")
        print("#"*40)
        print("1. Add New Student")
        print("2. Display All Students")
        print("3. Create New Course")
        print("4. Enroll Student in Course")
        print("5. Input/Update Student Grade")
        print("6. Print Student Report Card")
        print("7. Exit Application")
        
        choice = input("\nEnter system selection index (1-7): ").strip()
        
        if choice == '1':
            fn = input("Enter First Name: ")
            ln = input("Enter Last Name: ")
            em = input("Enter Email Address: ")
            ph = input("Enter Phone Number: ")
            sms.add_student(fn, ln, em, ph)
            
        elif choice == '2':
            sms.view_all_students()
            
        elif choice == '3':
            cn = input("Enter Course Name: ")
            cc = input("Enter Unique Course Code: ")
            cr = int(input("Enter Academic Credit Value (e.g. 3, 4): "))
            sms.add_course(cn, cc, cr)
            
        elif choice == '4':
            sid = int(input("Enter target Student ID: "))
            cid = int(input("Enter target Course ID: "))
            sms.enroll_student_in_course(sid, cid)
            
        elif choice == '5':
            sid = int(input("Enter target Student ID: "))
            cid = int(input("Enter target Course ID: "))
            g = input("Enter Academic Grade Symbol (e.g. A, B+, F): ").upper()
            sms.assign_grade(sid, cid, g)
            
        elif choice == '6':
            sid = int(input("Enter Student ID to review performance: "))
            sms.get_student_report_card(sid)
            
        elif choice == '7':
            print("\nExiting System Interface... Goodbye.")
            break
        else:
            print("[INVALID ENTRY] Please select an option between 1 and 7.")

if __name__ == "__main__":
    main()
