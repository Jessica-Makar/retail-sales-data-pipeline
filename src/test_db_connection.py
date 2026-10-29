from pathlib import Path
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

database_url = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD or ''}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(database_url)

try:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_database(), current_user, version();")
        )
        database, user, version = result.fetchone()

        print("Connection successful!")
        print(f"Database: {database}")
        print(f"User: {user}")
        print(f"Version: {version}")

except Exception as error:
    print("Connection failed.")
    print(f"Error: {error}")

finally:
    engine.dispose()
