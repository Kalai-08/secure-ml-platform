# Secure ML Prediction Platform

A learning project that combines **secure authentication and role-based access control** with a **machine learning prediction service**, built with FastAPI and scikit-learn.

Users register and log in, receive a short-lived JWT, and (once the prediction endpoint is wired up) use a trained breast-cancer classifier. Every sensitive action is written to an audit log.

## Features

- **Registration and login** with email validation and argon2 password hashing
- **JWT access tokens** (15 minute expiry by default), verified on each request
- **Role-based access control** (`admin`, `analyst`, `viewer`), with the role loaded from the database on every request
- **Audit logging** of register, login and admin actions (event, user, email, IP, success, detail)
- **User-enumeration protection**: identical error message and dummy-hash verification for unknown users
- **Strict config validation**: the app refuses to start with a weak `SECRET_KEY`
- **ML model**: logistic regression (scikit-learn) trained on the breast cancer dataset, loaded through a cached predictor
- **Tests** with pytest

## Tech stack

| Layer | Choice |
|---|---|
| Backend | FastAPI (Python) |
| Database | SQLAlchemy (SQLite by default via `DATABASE_URL`, other databases supported) |
| Auth | PyJWT + argon2-cffi, built from scratch |
| ML | scikit-learn, pandas, joblib |
| Testing | pytest, httpx |

## Project structure

```
secure-ml-platform/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app, CORS, routers, /health
│   │   ├── deps.py            # get_current_user, require_roles
│   │   ├── core/              # config, database, security (hash/JWT), audit
│   │   ├── models/            # User, Role, AuditLog (SQLAlchemy)
│   │   ├── schemas/           # Pydantic schemas (user, predict)
│   │   ├── routes/            # auth.py, admin.py
│   │   └── ml/                # train.py, predictor.py, model.joblib
│   ├── tests/                 # conftest.py, test_auth.py
│   ├── requirements.txt
│   └── .env.example
├── docs/
│   └── threat-model.md
└── README.md
```

## Getting started

Run all commands from the `backend/` directory.

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env            # then edit .env
```

Set a strong `SECRET_KEY` in `.env` (at least 32 characters). `change-me` is rejected. You can generate one with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | required | JWT signing key, at least 32 characters |
| `DATABASE_URL` | `sqlite:///./dev.db` | SQLAlchemy database URL |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `15` | Access token lifetime |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `CORS_ORIGIN` | `["http://localhost:5173"]` | Allowed browser origins |

```bash
# 4. (Optional) retrain the model; writes app/ml/model.joblib
python -m app.ml.train

# 5. Start the API
uvicorn app.main:app --reload
```

Interactive docs are available at http://127.0.0.1:8000/docs.

## API endpoints

| Method | Path | Access | Description |
|---|---|---|---|
| GET | `/health` | public | Health check |
| POST | `/auth/register` | public | Create an account (role is always `viewer`) |
| POST | `/auth/login` | public | Log in with form fields `username` (email) and `password`; returns a bearer token |
| GET | `/auth/me` | authenticated | Current user profile |
| GET | `/admin/users` | admin only | List all users (audited) |

## ML model

`app/ml/train.py` trains a `StandardScaler` + `LogisticRegression` pipeline on four features of the scikit-learn breast cancer dataset: `mean radius`, `mean texture`, `mean perimeter`, `mean area`. It prints test accuracy and saves the model bundle to `app/ml/model.joblib`.

`app/ml/predictor.py` loads the bundle once (cached) and exposes `predict(values)`, which returns the predicted label (`malignant` or `benign`) and the probability of the `benign` class.

> Status: the model and predictor are ready, but the HTTP prediction route is not yet exposed. This is educational only, not medical advice.

## Running tests

```bash
pytest
```

Tests cover registration (including role-escalation and duplicate attempts), weak passwords, login success and failure, identical errors for unknown users, token requirement and tampering, and viewer access to admin routes.

## Security

Design decisions and known gaps are documented in [docs/threat-model.md](docs/threat-model.md). Highlights:

- Passwords are hashed with argon2 and never stored in plain text
- The role is never accepted from the client and is not stored in the token
- Secrets live in `.env`, which is excluded from Git
- Not yet covered: login rate limiting, refresh tokens and revocation, HTTPS enforcement, input validation on the predict endpoint, dependency scanning

## Roadmap

- [x] Project setup and folder structure
- [x] User model, registration, argon2 hashing
- [x] Login, JWT, `/auth/me`, tests
- [x] RBAC and admin routes
- [x] Audit logging
- [x] Model training and predictor
- [ ] Authenticated `/predict` endpoint with input validation
- [ ] Rate limiting, refresh tokens
- [ ] React frontend (login and prediction pages)
