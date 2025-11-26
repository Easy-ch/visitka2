from pathlib import Path

DATABASE_URL    = "postgresql+asyncpg://super_user:xDdmZeUxFYrlE83zbyBT7XH-hBSpNN07k6UjQicOejA@localhost:5432/office_db"

def load_secret_data():
    key_file = Path("secret.key")

    if not key_file.exists():
        return None
    
    return key_file.read_text()


SECRET_KEY = load_secret_data()
