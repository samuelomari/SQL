"""Seed the SQLite DB with AI-generated sample data. Run: python3 seed.py"""
import sqlite3
from pathlib import Path

DB = Path(__file__).with_name("school.db")

INSTRUCTORS = [
    ("Dr. Alice Wanjiku", "alice.wanjiku@school.ac.ke", "Computer Science"),
    ("Prof. Brian Otieno", "brian.otieno@school.ac.ke", "Mathematics"),
    ("Ms. Carol Njeri", "carol.njeri@school.ac.ke", "Physics"),
    ("Mr. David Kamau", "david.kamau@school.ac.ke", "Computer Science"),
]

STUDENTS = [
    ("Julius Mwangi", "julius.mwangi@student.ac.ke", 2023),
    ("Faith Achieng", "faith.achieng@student.ac.ke", 2023),
    ("Peter Njoroge", "peter.njoroge@student.ac.ke", 2024),
    ("Grace Wambui", "grace.wambui@student.ac.ke", 2022),
    ("Samuel Omari", "samuel.omari@student.ac.ke", 2024),
    ("Lucy Atieno", "lucy.atieno@student.ac.ke", 2023),
    ("Kevin Barasa", "kevin.barasa@student.ac.ke", 2024),
    ("Diana Chebet", "diana.chebet@student.ac.ke", 2022),
]

COURSES = [
    # title, code, credits, instructor_index (None = unassigned, for LEFT JOIN demo)
    ("Intro to Python", "CS101", 3, 0),
    ("Databases & SQL", "CS201", 4, 0),
    ("Calculus I", "MATH101", 4, 1),
    ("Linear Algebra", "MATH201", 3, 1),
    ("Physics I", "PHY101", 4, 2),
    ("Web Development", "CS301", 3, 3),
    ("Data Science Basics", "CS401", 3, None),
]

ENROLLMENTS = [
    # student_index, course_index, grade
    (0, 0, "A"), (0, 1, "B"), (0, 2, "A"),
    (1, 0, "B"), (1, 4, "A"),
    (2, 0, "C"), (2, 5, "B"),
    (3, 2, "A"), (3, 3, "B"),
    (4, 0, "A"), (4, 1, "A"), (4, 5, "B"),
    (5, 1, "B"), (5, 4, "C"),
    (6, 5, "A"), (6, 0, "B"),
    (7, 3, "A"), (7, 4, "B"),
]

def main():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON;")
    cur = conn.cursor()
    cur.executemany("INSERT OR IGNORE INTO instructors(name,email,department) VALUES (?,?,?)", INSTRUCTORS)
    cur.executemany("INSERT OR IGNORE INTO students(name,email,enrollment_year) VALUES (?,?,?)", STUDENTS)
    instructor_ids = [r[0] for r in cur.execute("SELECT id FROM instructors ORDER BY id").fetchall()]
    cur.executemany(
        "INSERT OR IGNORE INTO courses(title,code,credits,instructor_id) VALUES (?,?,?,?)",
        [(t, c, cr, (instructor_ids[i] if i is not None else None)) for t, c, cr, i in COURSES],
    )
    student_ids = [r[0] for r in cur.execute("SELECT id FROM students ORDER BY id").fetchall()]
    course_ids = [r[0] for r in cur.execute("SELECT id FROM courses ORDER BY id").fetchall()]
    cur.executemany(
        "INSERT OR IGNORE INTO enrollments(student_id,course_id,grade) VALUES (?,?,?)",
        [(student_ids[s], course_ids[c], g) for s, c, g in ENROLLMENTS],
    )
    conn.commit()
    print(f"Seeded: {cur.execute('SELECT COUNT(*) FROM students').fetchone()[0]} students, "
          f"{cur.execute('SELECT COUNT(*) FROM instructors').fetchone()[0]} instructors, "
          f"{cur.execute('SELECT COUNT(*) FROM courses').fetchone()[0]} courses, "
          f"{cur.execute('SELECT COUNT(*) FROM enrollments').fetchone()[0]} enrollments.")
    conn.close()

if __name__ == "__main__":
    main()
