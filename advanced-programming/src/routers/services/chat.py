from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..logic import ChatMessage, ChatMessageCreate, ChatMessageUpdate

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/")
def send_message(data: ChatMessageCreate, db: Session = Depends(get_db)):
    message = ChatMessage(
        message=data.message,
        sender_id=data.sender_id,
        group_id=data.group_id
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


@router.get("/group/{group_id}")
def get_group_messages(group_id: int, db: Session = Depends(get_db)):
    return db.query(ChatMessage).filter(ChatMessage.group_id == group_id).all()


@router.put("/{message_id}")
def edit_message(
    message_id: int,
    data: ChatMessageUpdate,
    db: Session = Depends(get_db)
):
    message = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()

    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    message.message = data.message
    db.commit()
    db.refresh(message)

    return message


@router.delete("/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()

    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    db.delete(message)
    db.commit()

    return {"message": "Message deleted"}