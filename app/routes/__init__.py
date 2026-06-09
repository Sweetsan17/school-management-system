from app.routes.student_routes import student_bp
from app.routes.lecture_routes import lecture_bp
from app.routes.course_routes import course_bp


def register_blueprints(app):
    app.register_blueprint(student_bp)
    app.register_blueprint(lecture_bp)
    app.register_blueprint(course_bp)
