from app.extensions import db


class Lecture(db.Model):
    __tablename__ = "lectures"

    lecture_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    department = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "lecture_id": self.lecture_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "department": self.department,
        }
