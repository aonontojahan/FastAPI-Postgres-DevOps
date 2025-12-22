from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base, Todo

app = FastAPI(title="Todo API")
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/todos")
def create_todo(title: str, db: Session = Depends(get_db)):
    todo = Todo(title=title)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()
