from fastapi import APIRouter, HTTPException, Header, status
from typing import Annotated
from ..db import db_users

router = APIRouter()

@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["Users"])
def delete_user(user_id: int, x_user_role: Annotated[str, Header()]):
    if x_user_role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Hanya admin yang bisa mengakses resource ini")

    user_to_delete = next((u for u in db_users if u.id == user_id), None)
    if user_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User tidak ditemukan")

    db_users.remove(user_to_delete)
    return {"message": f"User dengan ID {user_id} berhasil dihapus"}