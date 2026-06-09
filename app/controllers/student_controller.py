from flask import jsonify, request
from datetime import datetime
from app.extensions import db
from app.models.student import Student


def _parse_date_of_birth(value):
    if not value:
        return None, "date_of_birth is required."
    try:
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d").date(), None
        return value, None
    except ValueError:
        return None, "date_of_birth must be in YYYY-MM-DD format."


def _validate_student_payload(data, student_id=None):
    errors = []
    if not data:
        return ["Request body is required."]

    first_name = data.get("first_name")
    if first_name is None or str(first_name).strip() == "":
        errors.append("first_name must contain only letter")

    last_name = data.get("last_name")
    if last_name is None or str(last_name).strip() == "":
        errors.append("last_name must contain only letter")

    email = data.get("email")
    if email is None or str(email).strip() == "":
        errors.append("please enter the vaild email address")
    elif str(email).strip():
        q = Student.query.filter(Student.email == str(email).strip())
        if student_id:
            q = q.filter(Student.id != student_id)
        if q.first():
            errors.append("Email address already exists.")

    date_of_birth_raw = data.get("date_of_birth")
    if date_of_birth_raw is None or str(date_of_birth_raw).strip() == "":
        errors.append("date_of_birth cannot be a future date.")

    return errors


def create_student():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_student_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    date_of_birth, date_err = _parse_date_of_birth(data.get("date_of_birth_raw"))
    if date_err:
        return jsonify({"error": date_err}), 400

    try:
        student = Student(
            first_name=data.get("first_name").strip(),
            last_name=data.get("last_name").strip(),
            email=data.get("email").strip(),
            date_of_birth=date_of_birth,
        )
        db.session.add(student)
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Student created successfully.",
                    "student": student.to_dict(),
                }
            ),
            201,
        )
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def get_students():
    students = Student.query.all()
    return jsonify({"students": [s.to_dict() for s in students]}), 200


def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found."}), 404
    return jsonify({"student": student.to_dict()}), 200


def update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found."}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided to update."}), 400

    errors = _validate_student_payload(data, student_id=student_id)
    if errors:
        return jsonify({"errors": errors}), 400

    date_of_birth, date_err = _parse_date_of_birth(data.get("date_of_birth"))
    if date_err:
        return jsonify({"error": date_err}), 400

    try:
        student.first_name = data.get("first_name").strip()
        student.last_name = data.get("last_name").strip()
        student.email = data.get("email").strip()
        student.date_of_birth = date_of_birth
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Student updated successfully.",
                    "student": student.to_dict(),
                }
            ),
            200,
        )
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found."}), 404
    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Student deleted successfully."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500
