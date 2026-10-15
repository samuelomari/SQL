# Evening Checkout Group Work — ERD to SQL to Custom Python ORM
# Domain: School Management System

## ERD (Text Representation)

```
[instructors] 1 ───< [courses] >───< [enrollments] >─── [students]
     PK id                PK id                PK id                PK id
     name                 title                student_id FK        name
     email UNIQUE         code UNIQUE          course_id FK         email UNIQUE
     department           credits              grade                enrollment_year
                          instructor_id FK     enrolled_on
```

Relationships:
- One Instructor teaches Many Courses (1-M): courses.instructor_id -> instructors.id
- Many Students take Many Courses (M-M) via enrollments junction table
- enrollments.student_id -> students.id, enrollments.course_id -> courses.id
- UNIQUE(student_id, course_id) prevents double enrollment

## Part 1 Deliverables
1. `schema.sql` — ERD converted to SQL DDL
2. `school.db` — SQLITE database created from schema
3. `seed.py` — AI-generated seed data imported into DB
4. `queries.sql` + `run_queries.py` — JOIN queries on the data

## Part 2 Deliverables
5. `orm.py` — Custom Python ORM (Database + Model base class)
6. `models.py` — Python classes mapping tables (Student, Instructor, Course, Enrollment)
7. `demo_orm.py` — CRUD demo proving CRUD->DML mapping
8. This README for stand-up presentation

## How to run (in order)
```bash
cd ~/sql
sqlite3 school.db < schema.sql
python3 seed.py
sqlite3 -header -column school.db < queries.sql
python3 run_queries.py
python3 demo_orm.py
```

---

## How to Run in Beekeeper Studio

Beekeeper Studio is a free GUI for viewing/editing SQLite databases.
Use it to demo your tables live in the Google Meet / stand-up.

### 1. Install / open
- Download from https://www.beekeeperstudio.io, install, open.
- (You already have a `beekeeper-studio` entry in your home folder.)

### 2. Connect to school.db
1. Click New Connection (plug icon, top-left).
2. Connection Type -> choose SQLite.
3. Browse / Choose File -> navigate to `~/sql/school.db` -> Open.
4. Optional: name it `School DB`, pick a colour.
5. Click Connect.

### 3. Explore the schema (ERD check)
- Left sidebar shows 4 tables: courses, enrollments, instructors, students.
- Click any table -> Structure tab: columns, types, PK/FK, UNIQUE, CHECK.
- Confirm FKs: courses.instructor_id -> instructors.id,
  enrollments.student_id -> students.id,
  enrollments.course_id -> courses.id.

### 4. View / edit data (no SQL needed)
- Click a table -> Data tab -> browse rows.
- Add row: + Add Row, fill cells, Apply.
- Edit cell: double-click, type, Apply.
- Delete row: select row -> trash icon -> Apply.
- Refresh icon after running terminal scripts.

### 5. Run the JOIN queries
1. Click New Query (or Ctrl+T).
2. Open queries.sql, copy Q1-Q5 one at a time.
3. Paste into query tab -> Run (Ctrl+Enter).
4. Results appear in the grid - screenshot these for slides.
5. Tip: run each SELECT separately so every result grid shows.

### 6. Re-seeding after messing up data in the GUI
```bash
cd ~/sql
rm school.db
sqlite3 school.db < schema.sql
python3 seed.py
```
Then in Beekeeper: Disconnect -> Connect to see fresh data.

---

## Terminal Command Cheat-Sheet (data functions)

All commands assume `cd ~/sql` first.

### A. Database setup / reset
```bash
sqlite3 school.db < schema.sql
python3 seed.py
rm school.db && sqlite3 school.db < schema.sql && python3 seed.py
ls -lh school.db
```

### B. sqlite3 interactive shell
```bash
sqlite3 school.db
```
Inside the sqlite> prompt:
```
.tables
.schema
.schema students
.headers on
.mode column
.mode box
PRAGMA foreign_keys = ON;
PRAGMA table_info(students);
PRAGMA foreign_key_list(enrollments);
SELECT COUNT(*) FROM students;
.read queries.sql
.dump
.backup main backup.db
.restore main backup.db
.exit
```

### C. One-liner queries (no shell needed)
```bash
sqlite3 -header -column school.db "SELECT * FROM students;"
sqlite3 -header -column school.db "SELECT * FROM instructors;"
sqlite3 -header -column school.db "SELECT * FROM courses;"
sqlite3 -header -column school.db "SELECT * FROM enrollments LIMIT 5;"
sqlite3 -header -column school.db < queries.sql
sqlite3 school.db ".dump" > full_backup.sql
sqlite3 restored.db < full_backup.sql
sqlite3 school.db "VACUUM;"
sqlite3 school.db "PRAGMA integrity_check;"
```

### D. CRUD with raw SQL
```bash
sqlite3 school.db "INSERT INTO students(name,email,enrollment_year) VALUES ('Test User','test.user@student.ac.ke',2024);"
sqlite3 -header -column school.db "SELECT * FROM students WHERE enrollment_year=2024 ORDER BY name;"
sqlite3 school.db "UPDATE students SET name='Julius K. Mwangi' WHERE id=1;"
sqlite3 school.db "UPDATE enrollments SET grade='A' WHERE student_id=1 AND course_id=2;"
sqlite3 school.db "DELETE FROM enrollments WHERE student_id=9 AND course_id=1;"
sqlite3 school.db "DELETE FROM students WHERE email='test.user@student.ac.ke';"
sqlite3 school.db "SELECT (SELECT COUNT(*) FROM students) AS students, (SELECT COUNT(*) FROM courses) AS courses, (SELECT COUNT(*) FROM enrollments) AS enrollments;"
```

### E. JOINs from the terminal
```bash
sqlite3 -header -column school.db "SELECT s.name, c.title, e.grade FROM enrollments e JOIN students s ON s.id=e.student_id JOIN courses c ON c.id=e.course_id ORDER BY s.name LIMIT 10;"
sqlite3 -header -column school.db "SELECT c.code, c.title FROM courses c LEFT JOIN instructors i ON i.id=c.instructor_id WHERE i.id IS NULL;"
sqlite3 -header -column school.db "SELECT s.name FROM students s LEFT JOIN enrollments e ON e.student_id=s.id WHERE e.id IS NULL;"
sqlite3 -header -column school.db "SELECT c.code, COUNT(e.id) AS total FROM courses c LEFT JOIN enrollments e ON e.course_id=c.id GROUP BY c.id ORDER BY total DESC;"
```

### F. Python entry points
```bash
python3 seed.py
python3 run_queries.py
python3 demo_orm.py
python3 -c "from models import Student; print(Student.all()[0].courses_with_grades())"
```

### G. Files / sharing
```bash
ls -la ~/sql
cd ~/sql && zip -r ../sql.zip .
```

---

## OOP Principles Used (Module 4)
- Encapsulation: Model hides SQL/connection details, exposes save()/update()/delete()
- Inheritance: Student/Instructor/Course/Enrollment all inherit from Model
- Abstraction: Model defines abstract CRUD interface, Database abstracts sqlite3
- Polymorphism: Each model overrides tablename/fields/__repr__/to_dict but uses same CRUD API

## What SQLAlchemy Abstracts (for presentation)
Our custom ORM manually builds: `INSERT INTO {table} ...`, `SELECT ... WHERE id=?`,
`UPDATE ... SET ...`, `DELETE ...`. SQLAlchemy does the same + connection pooling,
dialects, sessions, relationships/lazy-loading, migrations (Alembic), query builder.
Understanding our 150-line ORM makes SQLAlchemy click.
