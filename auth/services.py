from sqlalchemy.exc import SQLAlchemyError

from extensions import db
from models.user import User
from security import hash_password, verify_password


class ServiceError(Exception):
    pass


def find_user(email: str) -> User | None:
    return User.query.filter_by(email=email).first()


def create_user(forename: str, surname: str, email: str, password: str, role: str) -> User:
    if find_user(email):
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
        if find_user(email):
            raise ServiceError("Email already exists.") from e
        raise

    return user


def authenticate_user(email: str, password: str) -> User:
    user = find_user(email)
    if not user or not verify_password(pwhash=user.password, password=password):
        raise ServiceError("Invalid credentials.")

    return user


def delete_user(email: str) -> None:
    user = find_user(email)
    if not user:
        raise ServiceError("Unknown user.")

    db.session.delete(user)
    db.session.commit()
