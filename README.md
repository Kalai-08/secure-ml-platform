# secure-ml-platform
This program is for learning ml with auth.
**First step: stack-a final pannitu, repo + environment setup pannu, apram basic register/login.** Idha 3 naal-la mudikkalaam.

## Stack (recommended) ✅

| Layer | Choice | Why |
|---|---|---|
| Backend | **FastAPI (Python)** | ML-um auth-um oru language-la, easy integration |
| Database | **PostgreSQL** | Users, roles, audit logs |
| Frontend | **React (Vite) or Next.js** | Full-stack skill-ku |
| Auth | Scratch-la (JWT + argon2/bcrypt) | Learning-ku |
| ML | scikit-learn | Week 3-ku apram |
| Dev tools | Git, Docker (optional), VS Code | |

## Day 1: Setup

1. ✅ Project name decide pannu (e.g., `secure-ml-platform`).
2. ✅ GitHub repo create pannu, README-la goal-a 3 lines-la eludhu.
3. ✅ Folder structure:

```
secure-ml-platform/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── core/        # security, config
│   │   └── ml/          # later
│   └── requirements.txt
├── frontend/
├── docs/
│   └── threat-model.md
└── README.md
```

4. ✅ Python virtual env create pannu, `fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2-binary`, `passlib[argon2]`, `python-jose` install pannu.
5. ✅ PostgreSQL install (or Docker) pannu.

## Day 2: User model + Register

1. ✅ `users` table: `id, email, password_hash, role, created_at`.
2. ✅ `POST /auth/register`: email validate pannu, password-a **argon2-la hash** pannu (plain text store pannaadha).
3. ✅ Duplicate email check.
4. ✅ Postman/Swagger UI (`/docs`)-la test pannu.

## Day 3: Login + JWT

1. ✅ `POST /auth/login`: password verify pannu, **access token (15 min)** return pannu.
2. ✅ `GET /me`: token-a verify panni current user-a return pannu.
3. ✅ Wrong password, expired token-ku tests ezhudhu.
4. ✅ `docs/threat-model.md`-la first notes: "enna attacks possible (brute force, token theft)?"

## Day 3-ku apram

- Refresh tokens, roles (RBAC), simple React login page.
- Same time-la ML Week 1: Python, NumPy, Pandas.

## Rules ✅

- Daily commit pannu.
- Secrets (`SECRET_KEY`, DB password) `.env`-la vai, **GitHub-ku push pannaadha** (`.gitignore` add pannu).
- Ovvoru step-um enna panna, enna risk-nu 2 lines README-la ezhudhu.

Venumna naan **starter code (FastAPI register + login with argon2 and JWT)** workspace-la ready panni tharen, nee un machine-la run panni paaru. Venuma?