# Threat Model: Secure ML Prediction Platform

## 1. What we protect (assets)
- User accounts and password hashes
- JWT access tokens
- Prediction data and the ML model
- Audit logs (evidence of what happened)

## 2. Who might attack (actors)
- Anonymous internet user (no account)
- Registered low-privilege user (viewer) trying to do admin things
- Attacker with a stolen token or leaked database

## 3. Threats and mitigations

| # | Threat | Example | Mitigation (implemented) |
|---|--------|---------|--------------------------|
| 1 | Password theft from DB leak | Attacker reads the users table | Passwords hashed with **argon2**, never stored in plain text |
| 2 | Brute-force or credential guessing | Many login attempts | Lockout: 5 failed logins per email (or 20 per IP) in 15 minutes returns HTTP 429 with `Retry-After`. Counted from the audit log, blocks are logged as `login_blocked` |
| 3 | User enumeration | Timing or message difference reveals which emails exist | Dummy-hash verification when the user is not found, identical error message |
| 4 | Privilege escalation at signup | Sending `"role": "admin"` in register | Role is never read from the request, default is `viewer` |
| 5 | Accessing admin APIs as a normal user | viewer calls `/admin/users` | **RBAC**: `require_roles(Role.admin)`, role read from the DB on every request |
| 6 | Token forgery or tampering | Edit the JWT payload | HS256 signature check, algorithms pinned, `exp`, `sub`, `iat` required |
| 7 | Stolen token reuse | Token leaked from a log | Short expiry (`exp`), token never logged |
| 8 | Role change not taking effect | Demoted user keeps old role in token | Role is **not** in the token, loaded fresh from the DB |
| 9 | No evidence after an incident | Cannot tell who did what | **Audit log**: event, user, email, IP, success flag, detail |
| 10 | Cross-origin abuse | Unknown website calls the API from a browser | CORS allows only `CORS_ORIGINS` from settings |
| 11 | Invalid or malicious input | Bad email, short password | Pydantic validation (EmailStr, password 8 to 128 chars) |
| 12 | Malformed or extreme ML input | Negative or huge feature values | Pydantic range checks on `/predict`, role check (analyst/admin only), every prediction audit-logged |

## 4. Not yet covered (known gaps / future work)
- Login rate limiting or account lockout
- Token revocation and refresh tokens
- HTTPS enforcement (needed in deployment)
- Secrets in a proper secret manager (not a local `.env`)
- Input validation on the ML predict endpoint
- Dependency vulnerability scanning

## 5. Assumptions
- The app is deployed behind HTTPS.
- `SECRET_KEY` is long, random and kept out of Git.