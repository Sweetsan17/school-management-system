from flask import Blueprint

from app.controllers import lecture_controller as ctrl

lecture_bp = Blueprint("lectures", __name__, url_prefix="/api/lectures")


@lecture_bp.route("", methods=["POST"])
def create_lecture():
    return ctrl.create_lecture()


@lecture_bp.route("", methods=["GET"])
def get_lectures():
    return ctrl.get_lectures()


@lecture_bp.route("/<int:lecture_id>", methods=["GET"])
def get_lecture(lecture_id):
    return ctrl.get_lecture(lecture_id)


@lecture_bp.route("/<int:lecture_id>", methods=["PUT"])
def update_lecture(lecture_id):
    return ctrl.update_lecture(lecture_id)


@lecture_bp.route("/<int:lecture_id>", methods=["DELETE"])
def delete_lecture(lecture_id):
    return ctrl.delete_lecture(lecture_id)
