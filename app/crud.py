from sqlalchemy.orm import Session
from app import models, schemas

def get_task(db: Session, task_id: int):
    return db.query(models.Task), filter(models.Task.id == task_id).first()
def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()
def create_task(db: Session, task:schemas.createtask):
    db_task = models.Task(**task.dict())

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

