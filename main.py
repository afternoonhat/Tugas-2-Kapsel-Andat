from fastapi import FastAPI

# 1. Impor setiap router dari modul users
from modules.users.routes import createusers, readusers, updateusers, deleteusers
from modules.items.routes import createitem, readitem, updateitem, deleteitem
# 2. Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="API Tugas 2 - Users Module",
    description="API untuk mengelola data user.",
    version="1.0.0"
)

# 3. Daftarkan setiap router ke aplikasi utama
# FastAPI akan otomatis menggabungkan semua endpoint dari setiap router
app.include_router(createusers.router)
app.include_router(readusers.router)
app.include_router(updateusers.router)
app.include_router(deleteusers.router)

# --- Daftarkan Router Items ---
# Pastikan baris-baris ini ada dan tidak di-comment
app.include_router(createitem.router)
app.include_router(readitem.router)
app.include_router(updateitem.router)
app.include_router(deleteitem.router)

# 4. (Opsional) Buat endpoint root untuk pengetesan
@app.get("/")
def root():
    """
    Endpoint utama untuk mengecek apakah server berjalan.
    """
    return {"message": "Ini adalah API untuk Tugas 2"}

