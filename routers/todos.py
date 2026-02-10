from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
from auth import get_current_user
from database import get_db
from models import User
from schemas import TodoCreate, TodoResponse, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud.create_todo(db=db, todo=todo, user_id=current_user.id)


@router.get("/", response_model=list[TodoResponse])
def read_todos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud.get_todos(db=db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{todo_id}", response_model=TodoResponse)
def read_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_todo = crud.get_todo(db=db, todo_id=todo_id, user_id=current_user.id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_todo = crud.update_todo(db=db, todo_id=todo_id, todo=todo, user_id=current_user.id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = crud.delete_todo(db=db, todo_id=todo_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return None
