from fastapi import APIRouter, HTTPException, Header, status
from typing import List, Annotated
from ..schema.schemas import UserResponse
from ..db import db_users

router = APIRouter()

@router.get("/users/", response_model=List[UserResponse], tags=["Users"])
def get_all_users(x_user_role: Annotated[str, Header()]):
    if x_user_role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Hanya admin yang bisa mengakses resource ini")
    return db_users

@router.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def get_user_by_id(user_id: int, x_user_role: Annotated[str, Header()], x_user_id: Annotated[int, Header()]):
    user = next((u for u in db_users if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User tidak ditemukan")

    if x_user_role == "staff" and user.id != x_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Anda tidak punya hak akses")
    
    return user