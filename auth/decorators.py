from functools import wraps

from flask import g, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from services import find_user


def user_required():
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            email = get_jwt_identity()
            user = find_user(email)

            if not user:
                return jsonify(message="Unknown user."), 400

            g.user = user

            return fn(*args, **kwargs)

        return wrapper

    return decorator
