from fastapi.testclient import TestClient
from main import app

# TestClient memungkinkan kita untuk memanggil API di dalam kode Python
client = TestClient(app)

def test_create_user_success():
    """Tes skenario berhasil membuat user baru."""
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "role": "staff",
            "password": "ValidPassword1!"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_create_user_invalid_password():
    """Tes skenario gagal karena password tidak memenuhi syarat."""
    response = client.post(
        "/users/",
        json={
            "username": "testuser2",
            "email": "test2@example.com",
            "role": "staff",
            "password": "salah" # Password tidak valid
        }
    )
    assert response.status_code == 422 # Unprocessable Entity


def test_get_all_users_as_admin():
    """Tes skenario berhasil mendapatkan semua user sebagai admin."""
    headers = {"X-User-Role": "admin"}
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    # Memastikan responsenya adalah sebuah list (daftar)
    assert isinstance(response.json(), list)

def test_get_all_users_as_staff_forbidden():
    """Tes skenario gagal mendapatkan semua user sebagai staff."""
    headers = {"X-User-Role": "staff"}
    response = client.get("/users/", headers=headers)
    assert response.status_code == 403 # Forbidden


def test_get_own_user_as_staff():
    """Tes skenario staff berhasil melihat datanya sendiri."""
    # 1. Buat user baru untuk mendapatkan ID yang pasti
    new_user_data = {
        "username": "selfgetter",
        "email": "self@example.com",
        "role": "staff",
        "password": "PasswordSelf1!"
    }
    response_create = client.post("/users/", json=new_user_data)
    assert response_create.status_code == 201
    user_id = response_create.json()["id"]

    # 2. Minta data user tersebut dengan header yang sesuai
    headers = {"X-User-Role": "staff", "X-User-Id": str(user_id)}
    response_get = client.get(f"/users/{user_id}", headers=headers)
    
    assert response_get.status_code == 200
    assert response_get.json()["id"] == user_id

def test_get_other_user_as_staff_forbidden():
    """Tes skenario staff gagal melihat data user lain."""
    # ID user yang akan dilihat (misalnya 999, yang pasti bukan milik si staff)
    target_user_id = 999
    
    # Header untuk staff dengan ID 1
    headers = {"X-User-Role": "staff", "X-User-Id": "1"}
    
    response = client.get(f"/users/{target_user_id}", headers=headers)
    assert response.status_code == 403 # Forbidden

def test_delete_user_as_admin():
    """Tes skenario admin berhasil menghapus user."""
    # 1. Buat user yang akan dihapus
    response_create = client.post("/users/", json={
        "username": "todelete", "email": "delete@me.com", "role": "staff", "password": "PasswordDelete1!"
    })
    assert response_create.status_code == 201
    user_id = response_create.json()["id"]

    # 2. Hapus user tersebut sebagai admin
    headers = {"X-User-Role": "admin"}
    response_delete = client.delete(f"/users/{user_id}", headers=headers)
    assert response_delete.status_code == 200

    # 3. Pastikan user sudah benar-benar tidak ada
    headers_get = {"X-User-Role": "admin", "X-User-Id": "0"} # Id admin tidak relevan di sini
    response_get = client.get(f"/users/{user_id}", headers=headers_get)
    assert response_get.status_code == 404 # Not Found