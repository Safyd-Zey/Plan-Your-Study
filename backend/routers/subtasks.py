from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Subtask, Assignment, TaskStatus, User
from schemas import Subtask as SubtaskSchema, SubtaskCreate, SubtaskUpdate, SubtaskStatusUpdate
from routers.auth import get_current_user
from typing import List

router = APIRouter()

@router.post("/", response_model=SubtaskSchema)
def create_subtask(assignment_id: int, subtask: SubtaskCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(
        (Assignment.id == assignment_id) & (Assignment.user_id == current_user.id)
    ).first()

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )

    max_order = db.query(Subtask).filter(Subtask.assignment_id == assignment_id).count()

    db_subtask = Subtask(
        assignment_id=assignment_id,
        order=max_order,
        **subtask.dict()
    )
    db.add(db_subtask)

    if assignment.status == TaskStatus.NOT_STARTED:
        assignment.status = TaskStatus.IN_PROGRESS

    db.commit()
    db.refresh(db_subtask)
    db.refresh(assignment)

    return db_subtask

@router.get("/{assignment_id}", response_model=List[SubtaskSchema])
def get_subtasks(assignment_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(
        (Assignment.id == assignment_id) & (Assignment.user_id == current_user.id)
    ).first()

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )

    subtasks = db.query(Subtask).filter(Subtask.assignment_id == assignment_id).order_by(Subtask.order).all()
    return subtasks

@router.put("/{subtask_id}", response_model=SubtaskSchema)
def update_subtask(subtask_id: int, subtask_update: SubtaskUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()

    if not subtask:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subtask not found"
        )

    assignment = db.query(Assignment).filter(Assignment.id == subtask.assignment_id).first()
    if assignment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    for key, value in subtask_update.dict().items():
        if value is not None:
            setattr(subtask, key, value)

    db.commit()

    # Update assignment status when subtasks change
    subtasks = db.query(Subtask).filter(Subtask.assignment_id == assignment.id).all()
    if subtasks and all(s.status == TaskStatus.COMPLETED for s in subtasks):
        assignment.status = TaskStatus.COMPLETED
    elif any(s.status in [TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED] for s in subtasks):
        assignment.status = TaskStatus.IN_PROGRESS
    else:
        assignment.status = TaskStatus.NOT_STARTED

    db.commit()
    db.refresh(subtask)
    db.refresh(assignment)

    return subtask

@router.delete("/{subtask_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subtask(subtask_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()

    if not subtask:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subtask not found"
        )

    assignment = db.query(Assignment).filter(Assignment.id == subtask.assignment_id).first()
    if assignment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    db.delete(subtask)
    db.commit()

@router.patch("/{subtask_id}", response_model=SubtaskSchema)
def patch_subtask_status(subtask_id: int, status_update: SubtaskStatusUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()

    if not subtask:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subtask not found"
        )

    assignment = db.query(Assignment).filter(Assignment.id == subtask.assignment_id).first()
    if assignment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    subtask.status = status_update.status
    db.commit()

    # Update assignment status based on subtasks
    subtasks = db.query(Subtask).filter(Subtask.assignment_id == assignment.id).all()
    if subtasks and all(s.status == TaskStatus.COMPLETED for s in subtasks):
        assignment.status = TaskStatus.COMPLETED
    elif any(s.status in [TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED] for s in subtasks):
        assignment.status = TaskStatus.IN_PROGRESS
    else:
        assignment.status = TaskStatus.NOT_STARTED

    db.commit()
    db.refresh(subtask)
    db.refresh(assignment)

    return subtask
