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
def update_task(db: Session, task_id: int,  task_update:schemas.taskupdate):
    db_task = get_task(db. task.id)
    if not db_task:
        return None
    update_data = task_update.dict(exclude_unset= True)

    for key, value in update_data.items():
        setattr(db_task, key, value)

def delete_task(db:Session, task_id: int):
        db_task = get_task(db, task_id)
        if not db_task:
            return None
        db.delete(db_task)
        db.commit()
        return db_task

