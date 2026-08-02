from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Cloud Sentinel API", version="0.1.0")


@app.get("/")
def read_root():
    return {"message": "Welcome to cloud sentinel!"}
@app.get("/health")
def health_check():
    return {"status": "healthy", "Version": "0.1.0"}

@app.post("/tasks/",
        response_model=schemas.taskresponse,
        status_code=status.HTTP_201_CREATED,)
def create_task(task: schemas.createtask, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

@app.get("/tasks/",
        response_model = List[schemas.taskresponse])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks

@app.get("/task/{task_id}", response_model=schemas.taskresponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task in None:
        raise HTTPException(
                status_code=status.HTTP_404_not_FOUND, detail="Task not found")
        return db_task

