from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base, Note

app = FastAPI(title="Notes API")
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/notes")
def create_note(text: str, db: Session = Depends(get_db)):
    note = Note(text=text)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@app.get("/notes")
def get_notes(db: Session = Depends(get_db)):
    return db.query(Note).all()
