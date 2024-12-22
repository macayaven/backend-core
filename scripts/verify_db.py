# scripts/verify_db.py
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from backend_core.core.config import settings
from backend_core.db.base import engine


def verify_database() -> None:
    """Verify database connection and migrations."""
    print(f"Attempting to connect to database at: {settings.DATABASE_URL}")

    try:
        print("Opening connection...")
        with engine.connect() as conn:
            print("Connection established, checking version...")
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"Successfully connected to PostgreSQL. Version: {version}")

            print("\nChecking for users table...")
            result = conn.execute(
                text("SELECT EXISTS (" "SELECT FROM information_schema.tables " "WHERE table_name = 'users'" ")")
            )
            if result.scalar():
                print("✅ Users table exists - migrations successful!")
            else:
                print("❌ Users table not found - migrations may have failed!")

    except SQLAlchemyError as e:
        print(f"❌ Database connection error: {str(e)}")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")


if __name__ == "__main__":
    print("Starting database verification...")
    verify_database()
    print("\nVerification complete.")
