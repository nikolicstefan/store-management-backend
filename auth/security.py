from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from models import User


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(pwhash: str, password: str) -> bool:
    return check_password_hash(pwhash=pwhash, password=password)


def create_token(user: User) -> str:
    return create_access_token(
        identity=user.email,
        additional_claims={
            "forename": user.forename,
            "surname": user.surname,
            "role": user.role
        }
    )
