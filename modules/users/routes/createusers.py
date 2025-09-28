from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from ..schema.schemas import UserCreate, UserResponse, UserInDB
from ..db import db_users, next_user_id, get_password_hash

router = APIRouter()

@router.post(
    "/users/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"]
)
def create_user(user: UserCreate):
    for existing_user in db_users:
        if existing_user.username == user.username:
            raise HTTPException(status_code=400, detail="Username sudah terdaftar")
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email sudah terdaftar")

    global next_user_id
    user_in_db = UserInDB(
        id=next_user_id,
        username=user.username,
        email=user.email,
        role=user.role,
        hashed_password=get_password_hash(user.password),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db_users.append(user_in_db)
    next_user_id += 1
    return user_in_db
