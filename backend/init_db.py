"""Database initialization script."""
import sys
sys.path.insert(0, '/app')

from app.database import init_db
from app.models import Base

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")
