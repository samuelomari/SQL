-- Evening Checkout Part 1: ERD -> SQL Schema
-- Domain: School Management System
-- Run: sqlite3 school.db < schema.sql

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS instructors;

CREATE TABLE instructors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    department TEXT NOT NULL
);

CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    enrollment_year INTEGER NOT NULL CHECK (enrollment_year >= 2000)
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    credits INTEGER NOT NULL DEFAULT 3 CHECK (credits > 0),
    instructor_id INTEGER REFERENCES instructors(id) ON DELETE SET NULL
);

CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    grade TEXT CHECK (grade IN ('A','B','C','D','F', NULL)),
    enrolled_on TEXT NOT NULL DEFAULT (date('now')),
    UNIQUE (student_id, course_id)
);

CREATE INDEX idx_courses_instructor ON courses(instructor_id);
CREATE INDEX idx_enroll_student ON enrollments(student_id);
CREATE INDEX idx_enroll_course ON enrollments(course_id);
