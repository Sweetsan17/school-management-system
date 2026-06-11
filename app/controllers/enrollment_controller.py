from flask import jsonify, request
from app.extensions import db
from app.models.enrollment import Enrollment
from app.models.student import Student
from app.models.course import Course
from datetime import datetime


def _validate_enrollment_payload(data, enrollment_id=None):
    errors = []

    if not data:
        return ["Request body is required."]

    student_id = data.get("student_id")
    if student_id is None:
        errors.append("student_id is required.")
    else:
        try:
            if not Student.query.get(int(student_id)):
                errors.append("Invalid student selected.")
        except (ValueError, TypeError):
            errors.append("student_id must be a valid integer.")

    course_id = data.get("course_id")
    if course_id is None:
        errors.append("course_id is required.")
    else:
        try:
            if not Course.query.get(int(course_id)):
                errors.append("Invalid course selected.")
        except (ValueError, TypeError):
            errors.append("course_id must be a valid integer.")

    enrollment_date = data.get("enrollment_date")
    if not enrollment_date:
        errors.append("Enrollment date is required.")
    else:
        try:
            datetime.strptime(str(enrollment_date), "%Y-%m-%d")
        except ValueError:
            errors.append("Enrollment date must be in YYYY-MM-DD format.")

    status = data.get("status")
    if status is None:
        errors.append("status is required.")
    elif str(status).strip() not in Enrollment.VALID_STATUSES:
        errors.append(f"Status must be one of: {', '.join(Enrollment.VALID_STATUSES)}.")

    return errors


def create_enrollment():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_enrollment_payload(data)

    if errors:
        return jsonify({"errors": errors}), 400

    try:
        enrollment = Enrollment(
            student_id=int(data.get("student_id")),
            course_id=int(data.get("course_id")),
            enrollment_date=datetime.strptime(
                str(data.get("enrollment_date")), "%Y-%m-%d"
            ).date(),
            status=str(data.get("status")).strip(),
        )

        db.session.add(enrollment)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Enrollment created successfully.",
                    "enrollment": enrollment.to_dict(),
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


def get_enrollments():
    enrollments = Enrollment.query.all()
    return jsonify({"enrollments": [e.to_dict() for e in enrollments]}), 200


def get_enrollment(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)

    if not enrollment:
        return jsonify({"error": "Enrollment not found."}), 404

    return jsonify({"enrollment": enrollment.to_dict()}), 200


def update_enrollment(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)

    if not enrollment:
        return jsonify({"error": "Enrollment not found."}), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "No data provided to update."}), 400

    errors = _validate_enrollment_payload(data, enrollment_id)

    if errors:
        return jsonify({"errors": errors}), 400

    try:
        enrollment.student_id = int(data.get("student_id"))
        enrollment.course_id = int(data.get("course_id"))
        enrollment.enrollment_date = datetime.strptime(
            str(data.get("enrollment_date")), "%Y-%m-%d"
        ).date()
        enrollment.status = str(data.get("status")).strip()

        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Enrollment updated successfully.",
                    "enrollment": enrollment.to_dict(),
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


def delete_enrollment(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)

    if not enrollment:
        return jsonify({"error": "Enrollment not found."}), 404

    try:
        db.session.delete(enrollment)
        db.session.commit()

        return jsonify({"message": "Enrollment deleted successfully."}), 200

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
