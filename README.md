# FastAPI Authentication Template 🚀

A production-ready FastAPI template that supports:

- User registration and login with hashed passwords (bcrypt)
- JWT authentication with token expiry
- Protected routes
- SQLite database integration (easy to swap with PostgreSQL/MySQL)
- Modular code structure
- Fully tested with `pytest`

## 📁 Project Structure

```
app/
├── auth/
│   ├── models.py
│   ├── routers/
│   │   └── auth_routes.py
│   └── utils/
│       └── jwt_utils.py
├── database.py
├── main.py
tests/
└── test_auth.py
```

## 🚀 Getting Started

1. **Install dependencies**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # or source venv/bin/activate on Mac/Linux
   pip install -r requirements.txt
   ```

2. **Create `.env`**

   ```env
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=sqlite:///./auth.db
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```

3. **Initialize database**

   ```bash
   python -m app/auth/init_db.py
   ```

4. **Run the app**
   ```bash
   uvicorn app.main:app --reload
   ```

## 🧪 Running Tests

```bash
pytest -v
```

## 📌 Notes

- You can easily switch out SQLite for another database by updating `DATABASE_URL` in `.env`.
- For production, make sure to configure secure secret keys and HTTPS.
