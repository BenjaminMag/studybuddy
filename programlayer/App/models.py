import enum
from datetime import datetime, date
from sqlalchemy import (
    String, Integer, DateTime, ForeignKey, Boolean, Text, Enum, UniqueConstraint, Date
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class UserRole(str, enum.Enum):
    student = "STUDENT"
    admin = "ADMIN"

class UserStatus(str, enum.Enum):
    active = "ACTIVE"
    deactivated = "DEACTIVATED"

class GroupStatus(str, enum.Enum):
    active = "ACTIVE"
    archived = "ARCHIVED"

class MembershipRole(str, enum.Enum):
    owner = "OWNER"
    moderator = "MODERATOR"
    member = "MEMBER"

class MembershipStatus(str, enum.Enum):
    pending = "PENDING"
    active = "ACTIVE"
    rejected = "REJECTED"
    left = "LEFT"

class TaskStatus(str, enum.Enum):
    open = "OPEN"
    in_progress = "IN_PROGRESS"
    completed = "COMPLETED"

class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True)  # UUID string
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.student)
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus), default=UserStatus.active)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

class StudyGroup(Base):
    __tablename__ = "study_groups"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text)
    module_code: Mapped[str] = mapped_column(String, index=True)
    max_members: Mapped[int] = mapped_column(Integer, default=6)
    status: Mapped[GroupStatus] = mapped_column(Enum(GroupStatus), default=GroupStatus.active)
    created_by: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    memberships = relationship("GroupMembership", back_populates="group", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="group", cascade="all, delete-orphan")
    messages = relationship("ChatMessage", back_populates="group", cascade="all, delete-orphan")
    files = relationship("FileResource", back_populates="group", cascade="all, delete-orphan")

class GroupMembership(Base):
    __tablename__ = "group_memberships"
    __table_args__ = (UniqueConstraint("group_id", "user_id", name="uq_membership"),)

    id: Mapped[str] = mapped_column(String, primary_key=True)
    group_id: Mapped[str] = mapped_column(String, ForeignKey("study_groups.id"))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    role: Mapped[MembershipRole] = mapped_column(Enum(MembershipRole), default=MembershipRole.member)
    status: Mapped[MembershipStatus] = mapped_column(Enum(MembershipStatus), default=MembershipStatus.pending)
    joined_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    group = relationship("StudyGroup", back_populates="memberships")

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    group_id: Mapped[str] = mapped_column(String, ForeignKey("study_groups.id"), index=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text, default="")
    due_date: Mapped[date] = mapped_column(Date)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.open)
    created_by: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    group = relationship("StudyGroup", back_populates="tasks")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    group_id: Mapped[str] = mapped_column(String, ForeignKey("study_groups.id"), index=True)
    sender_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    deleted_flag: Mapped[bool] = mapped_column(Boolean, default=False)

    group = relationship("StudyGroup", back_populates="messages")

class FileResource(Base):
    __tablename__ = "file_resources"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    group_id: Mapped[str] = mapped_column(String, ForeignKey("study_groups.id"), index=True)
    uploader_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    file_name: Mapped[str] = mapped_column(String)
    file_size: Mapped[int] = mapped_column(Integer)
    file_type: Mapped[str] = mapped_column(String)
    upload_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    storage_path: Mapped[str] = mapped_column(String)

    group = relationship("StudyGroup", back_populates="files")