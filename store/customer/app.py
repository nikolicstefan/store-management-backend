from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from common.config import Config
from common.extensions import db, jwt, migrate
from common.services import ServiceError
from common.validation import ValidationError


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from customer.routes import customer_bp
    app.register_blueprint(customer_bp)

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify(message=str(e)), 400

    @app.errorhandler(ServiceError)
    def handle_service_error(e):
        return jsonify(message=str(e)), 400

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        if isinstance(e, HTTPException):
            return e
        return jsonify(message="Internal server error."), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
