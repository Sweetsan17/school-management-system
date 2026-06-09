from app.routes.student_routes import student_bp


def register_blueprints(app):
    app.register_blueprint(student_bp)
