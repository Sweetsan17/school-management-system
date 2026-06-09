from app.extensions import db


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    enrollent_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(
        db.Integer, db.ForeignKey("students.student_id"), nullable=False
    )
    course_id = db.Column(
        db.Integer, db.ForeignKey("courses.course_id"), nullable=False
    )
    status = db.Column(db.Boolean, default=True, nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            "enrollent_id": self.enrollent_id,
            "student_id": self.student_id,
            "course_id": self.course_id,
            "status": self.status,
            "enrollment_date": self.enrollment_date,
        }
