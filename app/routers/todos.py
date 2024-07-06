from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, auth
from ..database import get_db

router = APIRouter()

@router.post("/todos/", response_model=schemas.Todo)
def create_todo(
    todo: schemas.TodoCreate, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(auth.get_current_user)
):
    return crud.create_user_todo(db=db, todo=todo, user_id=current_user.id)

@router.get("/todos/", response_model=List[schemas.Todo])
def read_todos(
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(auth.get_current_user)
):
    todos = crud.get_todos(db, user_id=current_user.id)
    if not todos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No todos found for the user")
    return todos

@router.get("/todos/{todo_id}", response_model=schemas.Todo)
def read_todo(
    todo_id: int, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(auth.get_current_user)
):
    todo = crud.get_todo_by_id(db, todo_id=todo_id, user_id=current_user.id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo

@router.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(
    todo_id: int, 
    todo: schemas.TodoCreate, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(auth.get_current_user)
):
    db_todo = crud.get_todo_by_id(db, todo_id=todo_id, user_id=current_user.id)
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return crud.update_todo(db=db, todo_id=todo_id, todo=todo)

@router.delete("/todos/{todo_id}", response_model=schemas.Todo)
def delete_todo(
    todo_id: int, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(auth.get_current_user)
):
    db_todo = crud.get_todo_by_id(db, todo_id=todo_id, user_id=current_user.id)
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return crud.delete_todo(db=db, todo_id=todo_id)
