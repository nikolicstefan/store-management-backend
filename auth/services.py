from typing import Optional

from sqlalchemy.exc import SQLAlchemyError

from extensions import db
from models import User
from security import hash_password, verify_password


class ServiceError(Exception):
    pass


def get_user_by_email(email: str) -> Optional[User]:
    return User.query.filter_by(email=email).first()


def create_user(forename: str, surname: str, email: str, password: str, role: str) -> User:
    if get_user_by_email(email):
        raise ServiceError("Email already exists.")

    user = User(
        forename=forename,
        surname=surname,
        email=email,
        password=hash_password(password),
        role=role
    )

    db.session.add(user)

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        if get_user_by_email(email):
            raise ServiceError("Email already exists.") from e
        raise ServiceError("Failed to create user.") from e

    return user


def authenticate_user(email: str, password: str) -> User:
    user = get_user_by_email(email)
    if not user or not verify_password(pwhash=user.password, password=password):
        raise ServiceError("Invalid credentials.")
    return user
