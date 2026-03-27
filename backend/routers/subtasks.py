from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Subtask, Assignment
from schemas import Subtask as SubtaskSchema, SubtaskCreate, SubtaskUpdate
from routers.auth import get_current_user
from typing import List

router = APIRouter()

@router.post("/", response_model=SubtaskSchema)
def create_subtask(assignment_id: int, subtask: SubtaskCreate, token: str = None, db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    
    # Verify assignment belongs to user
    assignment = db.query(Assignment).filter(
        (Assignment.id == assignment_id) & (Assignment.user_id == current_user.id)
    ).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    # Get next order
    max_order = db.query(Subtask).filter(Subtask.assignment_id == assignment_id).count()
    
    db_subtask = Subtask(
        assignment_id=assignment_id,
        order=max_order,
        **subtask.dict()
    )
    db.add(db_subtask)
    db.commit()
    db.refresh(db_subtask)
    return db_subtask

@router.get("/{assignment_id}", response_model=List[SubtaskSchema])
def get_subtasks(assignment_id: int, token: str = None, db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    
    # Verify assignment belongs to user
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
def update_subtask(subtask_id: int, subtask_update: SubtaskUpdate, token: str = None, db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    
    subtask = db.query(Subtask).first()
    if subtask:
        assignment = db.query(Assignment).filter(Assignment.id == subtask.assignment_id).first()
        if assignment and assignment.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized"
            )
    
    subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()
    
    if not subtask:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subtask not found"
        )
    
    for key, value in subtask_update.dict().items():
        setattr(subtask, key, value)
    
    db.commit()
    db.refresh(subtask)
    return subtask

@router.delete("/{subtask_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subtask(subtask_id: int, token: str = None, db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    
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
