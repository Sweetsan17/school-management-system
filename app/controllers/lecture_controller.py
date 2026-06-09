from flask import jsonify, request
from app.extensions import db
from app.models.lecture import Lecture


def _validate_lecture_payload(data, lecture_id=None):
    errors = []

    if not data:
        return ["Request body is Required."]

    first_name = data.get("first_name")
    if not first_name or str(first_name).strip() == "":
        errors.append("lecture first_name is required.")

    last_name = data.get("last_name")
    if not last_name or str(last_name).strip() == "":
        errors.append("lecture last_name is required.")

    email = data.get("email")
    if not email or str(email).strip() == "":
        errors.append("invalid lecture email address.")
    else:
        email = str(email).strip()

    q = Lecture.query.filter(Lecture.email == email)

    if lecture_id:
        q = q.filter(Lecture.lecture_id != lecture_id)

    if q.first():
        errors.append("Lecture ID already exists.")

    department = data.get("department")
    if not department or str(department).strip() == "":
        errors.append("department is required.")


def create_lecture():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_lecture_payload(data)

    if errors:
        return jsonify({"errors": errors}), 400

    try:
        lecture = Lecture(
            first_name=data.get("first_name").strip(),
            last_name=data.get("last_name").strip(),
            email=data.get("email").strip(),
            department=data.get("department").strip(),
        )

        db.session.add(lecture)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Lecture created successfully.",
                    "lecture": lecture.to_dict(),
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


def get_lectures():
    lectures = Lecture.query.all()
    return jsonify({"lectures": [s.to_dict() for s in lectures]}), 200


def get_lecture(lecture_id):
    lecture = Lecture.query.get(lecture_id)

    if not lecture:
        return jsonify({"error": "Lecture not found."}), 404

    return jsonify({"lecture": lecture.to_dict()}), 200


def update_lecture(lecture_id):
    lecture = Lecture.query.get(lecture_id)

    if not lecture:
        return jsonify({"error": "Lecture not found."}), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "No data provided to update."}), 400

    errors = _validate_lecture_payload(data, lecture_id)

    if errors:
        return jsonify({"errors": errors}), 400

    try:
        lecture.first_name = data.get("first_name").strip()
        lecture.last_name = data.get("last_name").strip()
        lecture.email = data.get("email").strip()
        lecture.department = data.get("department").strip()

        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Lecture updated successfully.",
                    "lecture": lecture.to_dict(),
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


def delete_lecture(lecture_id):
    lecture = Lecture.query.get(lecture_id)

    if not lecture:
        return jsonify({"error": "Lecture not found."}), 404

    try:
        db.session.delete(lecture)
        db.session.commit()

        return jsonify({"message": "Lecture deleted successfully."}), 200

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
