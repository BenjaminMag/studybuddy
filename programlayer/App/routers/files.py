from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
import services

router = APIRouter(prefix="/files", tags=["files"])

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Hier speichern wir später die Metadaten in der Datenbank
    return {"filename": file.filename, "status": "hochgeladen"}

@router.get("/")
async def list_files(db: Session = Depends(get_db)):
    # Hier listen wir später alle Dateien auf
    return {"files": []}