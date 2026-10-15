-- Evening Checkout Part 1: JOIN queries
-- Run: sqlite3 school.db < queries.sql  (or sqlite3 -header -column school.db < queries.sql)

-- Q1: INNER JOIN — which student takes which course (with grade + instructor)
SELECT s.name AS student, c.title AS course, c.code, e.grade, i.name AS instructor
FROM enrollments e
INNER JOIN students s ON s.id = e.student_id
INNER JOIN courses c ON c.id = e.course_id
LEFT JOIN instructors i ON i.id = c.instructor_id
ORDER BY s.name, c.code;

-- Q2: LEFT JOIN — ALL courses with instructor (incl. unassigned CS401)
SELECT c.code, c.title, COALESCE(i.name, 'UNASSIGNED') AS instructor, i.department
FROM courses c
LEFT JOIN instructors i ON i.id = c.instructor_id
ORDER BY c.code;

-- Q3: Aggregation + JOIN — enrollment count per course
SELECT c.code, c.title, COUNT(e.id) AS total_students
FROM courses c
LEFT JOIN enrollments e ON e.course_id = c.id
GROUP BY c.id
ORDER BY total_students DESC;

-- Q4: Aggregation + JOIN — courses per instructor
SELECT i.name AS instructor, i.department, COUNT(c.id) AS courses_taught
FROM instructors i
LEFT JOIN courses c ON c.instructor_id = i.id
GROUP BY i.id
ORDER BY courses_taught DESC;

-- Q5: Triple JOIN + filter — all Computer Science students' enrollments
SELECT s.name AS student, c.title AS course, e.grade
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = e.course_id
JOIN instructors i ON i.id = c.instructor_id
WHERE i.department = 'Computer Science'
ORDER BY s.name;
