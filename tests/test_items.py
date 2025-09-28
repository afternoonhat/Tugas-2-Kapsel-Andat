from fastapi.testclient import TestClient
from main import app # Asumsi main.py adalah entrypoint aplikasimu

client = TestClient(app)

def test_create_item():
    """Tes ini sudah benar jika hanya membuat item."""
    response = client.post("/items/", json={"name": "Meja", "price": 500})
    assert response.status_code == 201 # Gunakan 201 untuk create
    data = response.json()
    assert data["name"] == "Meja"
    assert "id" in data

def test_read_item():
    """Perbaikan: Buat item dulu, baru dibaca."""
    # 1. Buat item baru untuk tes ini
    response_create = client.post("/items/", json={"name": "Kursi", "price": 150})
    assert response_create.status_code == 201
    item_id = response_create.json()["id"]

    # 2. Sekarang baca item yang baru saja dibuat
    response_read = client.get(f"/items/{item_id}")
    assert response_read.status_code == 200
    assert response_read.json()["name"] == "Kursi"

def test_update_item():
    """Perbaikan: Buat item dulu, baru di-update."""
    # 1. Buat item baru
    response_create = client.post("/items/", json={"name": "Lampu", "price": 75})
    item_id = response_create.json()["id"]

    # 2. Update item tersebut
    response_update = client.put(f"/items/{item_id}", json={"name": "Lampu LED", "price": 100})
    assert response_update.status_code == 200
    assert response_update.json()["name"] == "Lampu LED"

def test_delete_item():
    """Perbaikan: Buat item dulu, baru dihapus."""
    # 1. Buat item baru
    response_create = client.post("/items/", json={"name": "Buku", "price": 10})
    item_id = response_create.json()["id"]

    # 2. Hapus item tersebut
    response_delete = client.delete(f"/items/{item_id}")
    assert response_delete.status_code == 200 # atau 204, sesuaikan dengan API-mu

    # 3. (Opsional) Pastikan item sudah tidak ada
    response_get = client.get(f"/items/{item_id}")
    assert response_get.status_code == 404