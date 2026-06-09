from flask import jsonify, request
from datetime import datetime, date
from app.extensions import db
from app.models.student import Student


def _parse_date_of_birth(value):
    if not value:
        return None, "date_of_birth is required."

    try:
        dob = datetime.strptime(str(value), "%Y-%m-%d").date()
        return dob, None
    except ValueError:
        return None, "date_of_birth must be in YYYY-MM-DD format."


def _validate_student_payload(data, student_id=None):
    errors = []

    if not data:
        return ["Request body is required."]

    first_name = data.get("first_name")
    if not first_name or str(first_name).strip() == "":
        errors.append("first_name is required.")
    elif not str(first_name).replace(" ", "").isalpha():
        errors.append("first_name must contain only letters.")

    last_name = data.get("last_name")
    if not last_name or str(last_name).strip() == "":
        errors.append("last_name is required.")
    elif not str(last_name).replace(" ", "").isalpha():
        errors.append("last_name must contain only letters.")

    email = data.get("email")
    if not email or str(email).strip() == "":
        errors.append("email is required.")
    else:
        email = str(email).strip()

        q = Student.query.filter(Student.email == email)

        if student_id:
            q = q.filter(Student.student_id != student_id)

        if q.first():
            errors.append("Email address already exists.")

    date_of_birth = data.get("date_of_birth")

    if not date_of_birth or str(date_of_birth).strip() == "":
        errors.append("date_of_birth is required.")
    else:
        dob, dob_error = _parse_date_of_birth(date_of_birth)

        if dob_error:
            errors.append(dob_error)
        elif dob > date.today():
            errors.append("date_of_birth cannot be a future date.")

    return errors


def create_student():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_student_payload(data)

    if errors:
        return jsonify({"errors": errors}), 400

    date_of_birth, date_err = _parse_date_of_birth(data.get("date_of_birth"))

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

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "error": "Internal server error",
                    "details": str(e),
                }
            ),
            500,
        )


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

    errors = _validate_student_payload(data, student_id)

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

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "error": "Internal server error",
                    "details": str(e),
                }
            ),
            500,
        )


def delete_student(student_id):
    student = Student.query.get(student_id)

    if not student:
        return jsonify({"error": "Student not found."}), 404

    try:
        db.session.delete(student)
        db.session.commit()

        return jsonify({"message": "Student deleted successfully."}), 200

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "error": "Internal server error",
                    "details": str(e),
                }
            ),
            500,
        )
