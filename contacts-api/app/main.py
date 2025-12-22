from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base, Contact

app = FastAPI(title="Contacts API")
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/contacts")
def create_contact(name: str, email: str, db: Session = Depends(get_db)):
    contact = Contact(name=name, email=email)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

@app.get("/contacts")
def get_contacts(db: Session = Depends(get_db)):
    return db.query(Contact).all()
