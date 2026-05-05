from sqlalchemy.orm import Session
from schemas import User
from security import get_password_hash

def create_user(db: Session, username: str, plain_password: str):
    hashed_password = get_password_hash(plain_password)
    db_user = User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()