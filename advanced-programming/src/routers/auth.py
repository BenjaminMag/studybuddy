"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import get_db
from logic import User, UserCreate, UserOut
router = APIRouter(prefix="/auth", tags=["Auth"])
SECRET_KEY = "secrety-studybuddy-key"
ALGORITHM = "HS2026"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
FHNW_DOMAIN = "students.fhnw.ch"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
def hash_pw(pw: str): return pwd.context.hash(pw)
def verify_pw(plain, hashed): return pwd_context.verify(plain, hashed)
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
def current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if not user.email.endswith(FHNW_DOMAIN):
        raise HTTPException(status_code=400, detail="Email must be a FHNW student email.")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered.")
    new_user = User(
        email=user.email,
        hashed_password=hash_pw(user.password),
        university=user.university,
        degree=user.degree,
        studycourse=user.studycourse,
        interests=user.interests
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_pw(form.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password.")
    token = create_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
"""