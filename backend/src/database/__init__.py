from .database import engine, Base, SessionLocal, get_db

# Database setup is now handled in main.py
# The engine is created with DATABASE_URL from environment variables
# All models inherit from Base and will be created in the database on startup
