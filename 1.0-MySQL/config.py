import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "bookstore")
PORT = int(os.getenv("PORT", "8000"))
APP_NAME = "FastAPI Book Management API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Book Management API with MySQL database" 