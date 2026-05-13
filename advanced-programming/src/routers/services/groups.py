from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..uploads.database import get_db
from ..uploads.logic import Group, User, GroupCreate, GroupUpdate

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.post("/")
def create_group(data: GroupCreate, db: Session = Depends(get_db)):
    group = Group(name=data.name, description=data.description)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


@router.get("/")
def get_groups(db: Session = Depends(get_db)):
    return db.query(Group).all()


@router.get("/{group_id}")
def get_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    return group


@router.put("/{group_id}")
def update_group(group_id: int, data: GroupUpdate, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    if data.name is not None:
        group.name = data.name

    if data.description is not None:
        group.description = data.description

    db.commit()
    db.refresh(group)
    return group


@router.delete("/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    db.delete(group)
    db.commit()

    return {"message": "Group deleted"}


@router.post("/{group_id}/add-user/{user_id}")
def add_user_to_group(group_id: int, user_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    user = db.query(User).filter(User.id == user_id).first()

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user in group.members:
        return {"message": "User already in group"}

    group.members.append(user)
    db.commit()

    return {"message": "User added to group"}