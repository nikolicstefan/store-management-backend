from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from config import Config
from extensions import db, jwt, migrate


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from routes import auth_bp
    app.register_blueprint(auth_bp)

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        if isinstance(e, HTTPException):
            return e
        return jsonify(message="Internal server error."), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
