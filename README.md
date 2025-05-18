# 🔐 FastAPI Authentication Template

A secure, modular FastAPI starter with:

- ✅ Email & password-based user registration
- 🔐 Password hashing with bcrypt
- 🪪 JWT authentication (configurable expiration)
- 🔐 Protected routes via OAuth2 bearer tokens
- 🗃️ SQLite by default (easily swappable via `DATABASE_URL`)
- 🧪 Full test coverage with `pytest`
- 🧱 Clean and scalable project structure

---

## 🗂️ Project Structure

```
app/
├── auth/
│   ├── routers/
|   |   ├── __init__.py
│   │   └── auth_routes.py
│   ├── utils/
|   |   ├── __init__.py
│   |   └── jwt_utils.py
│   ├── __init__.py
|   ├── init_db.py
|   └── models.py
├── __init__.py
├── database.py
└── main.py
tests/
└── test_auth.py
```

## ⚙️ Getting Started

### 1. Create virtual environment & install dependencies

```bash
python -m venv venv
.\venv\Scripts\activate           # On Windows
# source venv/bin/activate       # On macOS/Linux

pip install -r requirements.txt
```

### 2. Create `.env` file

```env
JWT_SECRET_KEY=your_super_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./auth.db
```

### 3. Initialize database

```bash
python app/auth/utils/init_db.py
```

### 4. Run the app

```bash
uvicorn app.main:app --reload
```

## 🧪 Running Tests

```bash
pytest -v
```

## 📌 Notes

- Use EmailStr for validation and stricter user inputs.

- Easily extend the User model with fields like name, created_at, etc.

- To switch to PostgreSQL, update DATABASE_URL and install psycopg2.

- Always keep .env secrets out of version control (.gitignore already handles this).
