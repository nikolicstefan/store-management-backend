from typing import Optional

from extensions import db
from models import User


def get_user_by_email(email: str) -> Optional[User]:
    return User.query.filter_by(email=email).first()


def create_user(forename: str, surname: str, email: str, password: str, role: str) -> User:
    user = User(
        forename=forename,
        surname=surname,
        email=email,
        password = password,
        role=role
    )
    db.session.add(user)
    db.session.commit()
    return user
