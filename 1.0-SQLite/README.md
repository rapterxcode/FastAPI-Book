# FastAPI Book Management API - SQLite Version (Best Practice Structure)

A FastAPI application for managing books with SQLite database using the best practice structure with separated modules.

## 🏗️ Project Structure

```
FastAPI-Book/1.0-SQLite/
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── database.py        # Database connection and session
│   ├── models.py          # SQLModel database models
│   ├── schemas.py         # Pydantic request/response schemas
│   ├── crud.py           # CRUD operations
│   └── api/
│       ├── __init__.py
│       ├── deps.py        # Dependencies
│       ├── health.py      # Health check endpoints
│       └── v1/
│           ├── __init__.py
│           ├── api.py     # API router
│           └── endpoints/
│               ├── __init__.py
│               └── books.py  # Book endpoints
├── main.py               # FastAPI application entry point
├── config.env           # Environment variables
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## ✨ Features

- **🏗️ Best Practice Structure**: Separated modules for better maintainability
- **⚙️ Configuration Management**: Pydantic Settings for type-safe configuration
- **🗄️ Database Layer**: SQLModel for ORM with SQLite
- **📝 Schema Validation**: Pydantic for request/response validation
- **🔍 CRUD Operations**: Separated business logic
- **🌐 API Versioning**: v1 API structure for future scalability
- **🔧 Dependency Injection**: Clean dependency management
- **📊 Health Monitoring**: Built-in health check endpoint
- **🔍 Search Functionality**: Full-text search across multiple fields
- **📄 Auto Documentation**: Swagger UI and ReDoc

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python main.py
# or
uvicorn main:app --reload
```

### 3. Access the API
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/
- **API Base URL**: http://localhost:8000/books

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check and server status |
| GET | `/docs` | Swagger UI documentation |
| GET | `/redoc` | ReDoc documentation |
| **POST** | **`/books`** | **Create a new book** |
| **GET** | **`/books`** | **Get all books (with pagination)** |
| **GET** | **`/books/search`** | **Search books by term** |
| **GET** | **`/books/{book_id}`** | **Get a book by ID** |
| **PUT** | **`/books/{book_id}`** | **Update a book** |
| **DELETE** | **`/books/{book_id}`** | **Delete a book** |

## 🔧 Configuration

### Environment Variables (`config.env`)
```env
DB_NAME=bookstore.db
PORT=8000
ENVIRONMENT=development
```

### Configuration Management (`app/config.py`)
```python
class Settings(BaseSettings):
    db_name: str = "bookstore.db"
    port: int = 8000
    environment: str = "development"
    app_name: str = "FastAPI Book Management API"
    app_version: str = "1.0.0"
```

## 📊 Database Schema

### Book Model (`app/models.py`)
```python
class Book(SQLModel, table=True):
    __tablename__ = "books"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, max_length=255, nullable=False)
    author: str = Field(index=True, max_length=255, nullable=False)
    published_year: Optional[int] = Field(index=True, nullable=True)
    genre: Optional[str] = Field(index=True, max_length=100, nullable=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
```

## 🔍 Usage Examples

### Create a Book
```bash
curl -X POST "http://localhost:8000/books" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "published_year": 1925,
    "genre": "Fiction"
  }'
```

### Search Books
```bash
curl "http://localhost:8000/books/search?q=Fitzgerald"
```

### Get All Books with Pagination
```bash
curl "http://localhost:8000/books?skip=0&limit=10"
```

## 🏗️ Architecture Benefits

### 1. **Separation of Concerns**
- **Models**: Database structure
- **Schemas**: API contracts
- **CRUD**: Business logic
- **Endpoints**: API routes
- **Config**: Application settings

### 2. **Scalability**
- **API Versioning**: Easy to add v2, v3 APIs
- **Modular Design**: Easy to add new features
- **Dependency Injection**: Clean testing

### 3. **Maintainability**
- **Clear Structure**: Easy to navigate
- **Type Safety**: Pydantic validation
- **Documentation**: Auto-generated docs

### 4. **Testing**
- **Isolated Components**: Easy to unit test
- **Mock Dependencies**: Clean test setup
- **CRUD Separation**: Test business logic separately

## 🔧 Development

### Adding New Endpoints
1. Create new endpoint in `app/api/v1/endpoints/`
2. Add CRUD operations in `app/crud.py`
3. Include router in `app/api/v1/api.py`

### Adding New Models
1. Define model in `app/models.py`
2. Create schemas in `app/schemas.py`
3. Add CRUD operations in `app/crud.py`

### Configuration Changes
1. Update `app/config.py`
2. Add environment variables to `config.env`

## 📦 Dependencies

- **FastAPI**: Modern web framework
- **SQLModel**: SQL toolkit and ORM
- **Pydantic**: Data validation
- **Pydantic Settings**: Configuration management
- **SQLite**: Lightweight database
- **Uvicorn**: ASGI server

## 🚀 Production Deployment

### Environment Variables
```env
ENVIRONMENT=production
PORT=8000
DB_NAME=production.db
```

### Run with Uvicorn
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📝 License

This project follows best practices for FastAPI applications with a clean, maintainable, and scalable architecture.
