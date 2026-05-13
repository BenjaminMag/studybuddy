from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from .database import Base

# Relational Tables

group_members = Table(
    "group_members",
    Base.metadata,
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True)
)

# SQLAlchemy Models

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    university = Column(String, default="FHNW")
    degree = Column(String, nullable=True)
    studycourse = Column(String, nullable=True)
    interests = Column(String, nullable=True)
    groups = relationship("Group", secondary=group_members, back_populates="members")


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    members = relationship("User", secondary=group_members, back_populates="groups")


class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    filepath = Column(String)
    tag = Column(String, nullable=True)
    uploader_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    upload_time = Column(DateTime, default=datetime.utcnow)
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    done = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

# Pydantic Schemes

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    university: Optional[str] = "FHNW"
    degree: Optional[str] = None
    studycourse: Optional[str] = None
    interests: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: str
    university: Optional[str]
    class Config:
        from_attributes = True


class GroupCreate(BaseModel):
    name: str
    description: Optional[str] = None
class GroupOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    class Config:
        from_attributes = True

class FileOut(BaseModel):
    id: int
    filename: str
    uploaded_at: datetime
    uploader_id: Optional[int]
    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    done: bool
    class Config:
        from_attributes = True