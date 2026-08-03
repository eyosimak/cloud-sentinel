from fastapi import FastAPI, Depends, HTTPException, status, Request
import time
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

START_TIME = time.time()
REQUEST_COUNT = 0

@app.middleware("http")
async def track_metrics(request: Request, call_next):
    global REQUEST_COUNT
    REQUEST_COUNT += 1
    response = await call_next(request)
    return response

@app.get("/metrics")
def get_metrics():
    uptime_seconds = time.time() - START_TIME
    return { "uptime_seconds": round(uptime_seconds, 2),
            "request_count": REQUEST_COUNT}

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
@app.put("/tasks/{id}", response_model=schemas.taskresponse)
def update_task(task_id: int, task_update: schemas.taskupdate, db: Session = Depends(get_db),):
    db_task = crud.update_task(db, task_id=task_id, task_update=task_update)
    if db_task is None:
        raise HTTPException(
                status_code=status.HTTP_4O4_NOT_FOUND, detail="Task not found")
    return db_task

@app.delete("/tasks/{id}", response_model=schemas.taskresponse)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return db_task

@app.get("/stats/")
def get_task_stats(db: Session=Depends(get_db)):
        tasks = crud.get_tasks(db, skip=0, limit=10000)
        total = len(tasks)
        completed  = sum(1 for t in tasks if t.status.lower() == "completed")
        pending = sum(1 for i in tasks if i.status.lower() == "pending")

        return {"total": total, "completed":completed, "pending":pending}

