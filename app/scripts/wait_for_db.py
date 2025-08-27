import time
from sqlalchemy import create_engine, text  # Добавьте импорт text
from app.config import settings

if __name__ == "__main__":
    engine = create_engine(settings.database_url, pool_pre_ping=True)
    for i in range(60):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))  # Исправьте эту строку
            print("Database is up!")
            break
        except Exception as e:
            print(f"Waiting for DB... ({i+1}/60) {e}")
            time.sleep(1)
    else:
        raise RuntimeError("Database is not reachable after 60 seconds.")