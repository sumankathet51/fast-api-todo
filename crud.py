from sqlalchemy.orm import Session

from auth import hash_password
from models import Todo, User
from schemas import TodoCreate, TodoUpdate, UserCreate


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_todo(db: Session, todo: TodoCreate, user_id: int) -> Todo:
    db_todo = Todo(**todo.model_dump(), user_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todos(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Todo]:
    return db.query(Todo).filter(Todo.user_id == user_id).offset(skip).limit(limit).all()


def get_todo(db: Session, todo_id: int, user_id: int) -> Todo | None:
    return db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()


def update_todo(db: Session, todo_id: int, todo: TodoUpdate, user_id: int) -> Todo | None:
    db_todo = get_todo(db, todo_id, user_id)
    if db_todo is None:
        return None

    update_data = todo.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)

    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int, user_id: int) -> bool:
    db_todo = get_todo(db, todo_id, user_id)
    if db_todo is None:
        return False

    db.delete(db_todo)
    db.commit()
    return True
