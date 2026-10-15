"""CRUD demo: proves Python method calls map to SQL DML. Run: python3 demo_orm.py"""
from models import Student, Instructor, Course, Enrollment

print("=== CREATE (INSERT) ===")
s = Student.create(name="Demo Student", email="demo.student@student.ac.ke", enrollment_year=2024)
print("Created:", s)

print("\n=== READ (SELECT) ===")
print("Fetched:", Student.get(s.id))
print(f"Total students: {len(Student.all())}")

print("\n=== UPDATE ===")
s.update(name="Demo Student Updated")
print("After update:", Student.get(s.id))

print("\n=== JOIN via model method ===")
first = Student.all()[0]
print(f"{first.name} takes:")
for row in first.courses_with_grades():
    print(f"  {row['code']} {row['title']} grade={row['grade']} instructor={row['instructor']}")

print("\n=== DELETE ===")
s.delete()
print("Deleted. Fetch returns:", Student.get(s.id))
print("\nAll CRUD operations mapped to DML successfully.")
