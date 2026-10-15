"""Pretty-print the JOIN queries. Run: python3 run_queries.py"""
import sqlite3
from pathlib import Path

DB = Path(__file__).with_name("school.db")

QUERIES = {
    "Q1: Students + their courses (INNER JOIN)": """
        SELECT s.name AS student, c.title AS course, e.grade, COALESCE(i.name,'UNASSIGNED') AS instructor
        FROM enrollments e
        JOIN students s ON s.id = e.student_id
        JOIN courses c ON c.id = e.course_id
        LEFT JOIN instructors i ON i.id = c.instructor_id
        ORDER BY s.name, c.code LIMIT 10""",
    "Q2: All courses with instructor (LEFT JOIN)": """
        SELECT c.code, c.title, COALESCE(i.name,'UNASSIGNED') AS instructor
        FROM courses c LEFT JOIN instructors i ON i.id = c.instructor_id ORDER BY c.code""",
    "Q3: Enrollment count per course": """
        SELECT c.code, COUNT(e.id) AS total
        FROM courses c LEFT JOIN enrollments e ON e.course_id = c.id
        GROUP BY c.id ORDER BY total DESC""",
    "Q4: Courses per instructor": """
        SELECT i.name, COUNT(c.id) AS courses_taught
        FROM instructors i LEFT JOIN courses c ON c.instructor_id = i.id
        GROUP BY i.id ORDER BY courses_taught DESC""",
}

def main():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    for title, sql in QUERIES.items():
        print(f"\n=== {title} ===")
        rows = conn.execute(sql).fetchall()
        if not rows:
            print("(no rows)"); continue
        print(" | ".join(rows[0].keys()))
        for r in rows:
            print(" | ".join(str(v) for v in r))
    conn.close()

if __name__ == "__main__":
    main()
