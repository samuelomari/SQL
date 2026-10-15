"""Tables -> Python classes. Each model maps 1:1 to a DB table."""
from orm import Model, db


class Instructor(Model):
    __table__ = "instructors"
    __fields__ = ("name", "email", "department")

    @property
    def courses(self):
        from models import Course  # local import avoids cycles
        return Course.filter("instructor_id=?", (self.id,))


class Student(Model):
    __table__ = "students"
    __fields__ = ("name", "email", "enrollment_year")

    @property
    def enrollments(self):
        return Enrollment.filter("student_id=?", (self.id,))

    def courses_with_grades(self):
        """JOIN via raw SQL but returned as dicts — shows ORM + JOIN together."""
        return db.fetch_all(
            """SELECT c.code, c.title, e.grade, i.name AS instructor
               FROM enrollments e
               JOIN courses c ON c.id = e.course_id
               LEFT JOIN instructors i ON i.id = c.instructor_id
               WHERE e.student_id=? ORDER BY c.code""",
            (self.id,),
        )


class Course(Model):
    __table__ = "courses"
    __fields__ = ("title", "code", "credits", "instructor_id")


class Enrollment(Model):
    __table__ = "enrollments"
    __fields__ = ("student_id", "course_id", "grade", "enrolled_on")

    def __init__(self, id=None, **kwargs):
        # enrolled_on has a DB default; allow None on construction
        super().__init__(id, **kwargs)
