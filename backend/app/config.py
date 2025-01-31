# app/config.py
import os

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./house_management.db")

settings = Settings()