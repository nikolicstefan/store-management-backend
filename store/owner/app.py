from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from common.config import Config
from common.extensions import db, jwt


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from owner.routes import owner_bp
    app.register_blueprint(owner_bp)

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        if isinstance(e, HTTPException):
            return e
        return jsonify(message="Internal server error."), 500

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
