from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()
#permet de selectionner les adresse qui peuvent jouer avec la bdd
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration de la base de données
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modèle Todo
class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    done = Column(Boolean, default=False)
    text = Column(String)

# Créer les tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# READ - Lire toutes les tâches
@app.get("/todos")
def get_todos():
    db = next(get_db())
    todos = db.query(Todo).all()
    return [{"id": t.id, "text":t.text, "done":t.done} for t in todos]


# CREATE - Créer une tâche
@app.post("/todos")
def create_todo(text: str):
    db = next(get_db())
    new_todo = Todo(text=text,done=False)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return {"id":new_todo.id, "text":new_todo.text,"done":new_todo.done}

# UPDATE - Marquer comme fait/pas fait
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, done: bool = None, text: str = None):
    db = next(get_db())
    todo = db.query(Todo).filter(Todo.id == todo.id).first()
    if done is not None:
        todo.done=done
    if text is not None:
        todo.text=text
    db.commit()
    return {"id":todo.id,"done":todo.done, "text":todo.text}

# DELETE - Supprimer une tâche
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    db=next(get_db())
    todo=db.query(Todo).filter(Todo.id == todo.id).first()
    db.delete(todo)
    db.commit()
    return {"deleted": todo_id}

