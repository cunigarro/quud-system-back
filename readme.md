#### Description
Backend services to quality code

- Posgressql
- Python 3.12

## Features

- **User Registration**: Register a new user with name, email, and password.
- **User Login**: Authenticate a user and generate a JWT access token.
- **Project creation**: Create repositories
- **Generate inspections**: evaluate the rules for the repositories
- **JWT Authentication**: Secure endpoints with token-based authentication.
- **Component-Based Design**: Modular structure to make it easy to maintain and extend.

## Run the project

1. Install the dependencies:  ```pip install -r requirements.txt```
2. Execute file ```start.sh```

## Documentation

http://127.0.0.1:8000/docs

## Project Structure

```plaintext
project/
│
├── app/
│   ├── api/                
│   │   ├── auth.py              # API endpoints for authentication
│   │
│   ├── db/                 
│   │   ├── database.py          # Database connection setup
│   │   ├── models.py            # SQLAlchemy models
│   │
│   ├── repositories/       
│   │   ├── user_repository.py    # Database operations for User model
│   │
│   ├── services/           
│   │   ├── auth_service.py       # Business logic for registration and login
│   │
│   ├── schemas/            
│   │   ├── user.py               # Pydantic schemas for request/response models
│   │
│   ├── core/
│   │   ├── config.py             # Application configuration (e.g., environment variables)
│   │   ├── security.py           # Security utilities (e.g., password hashing, JWT creation)
│   │
└── .env                          # Environment variables
└── main.py                       # Main FastAPI application entry point
