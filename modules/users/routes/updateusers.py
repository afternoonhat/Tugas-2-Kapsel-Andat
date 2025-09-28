from fastapi import APIRouter, HTTPException, Header, status
from typing import Annotated
from datetime import datetime
from ..schema.schemas import UserCreate, UserResponse
from ..db import db_users, get_password_hash

router = APIRouter()

@router.put("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def update_user(user_id: int, user_update: UserCreate, x_user_role: Annotated[str, Header()]):
    if x_user_role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Hanya admin yang bisa mengakses resource ini")

    user_index = next((i for i, u in enumerate(db_users) if u.id == user_id), -1)
    
    if user_index == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User tidak ditemukan")

    updated_user = db_users[user_index]
    updated_user.username = user_update.username
    updated_user.email = user_update.email
    updated_user.role = user_update.role
    updated_user.hashed_password = get_password_hash(user_update.password)
    updated_user.updated_at = datetime.utcnow()

    db_users[user_index] = updated_user
    return updated_user