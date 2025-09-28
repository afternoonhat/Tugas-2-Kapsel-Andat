from typing import List
from modules.users.schema.schemas import UserInDB

# Variabel ini akan berfungsi sebagai database in-memory kita
db_users: List[UserInDB] = []
next_user_id = 1

# Fungsi sederhana untuk "hashing" password (hanya untuk simulasi)
def get_password_hash(password: str):
    return f"{password}_hashed"