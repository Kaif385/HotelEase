import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Config:
    # Security Key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key_fallback'
    
    # Database Connection URI
    # Format: mysql+pymysql://user:password@host/db_name
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}"
        f"@{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False # Set to True if you want to see raw SQL in terminal