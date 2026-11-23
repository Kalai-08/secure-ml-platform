EMAIL = "kavi@example.com"
PASSWORD = "VeryStrong123"

def register(client, email=EMAIL, password=PASSWORD, **extra):
    return client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            **extra
        }
    )

def login(client, email=EMAIL, password=PASSWORD):
    return client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password
        }
    )

def auth_header(client):
    register(client)
    token = login(client).json()["access_token"]
    return{
        "Authorization": f"Bearer {token}"
    }

def test_register_success(client):
    r = register(client)
    assert r.status_code == 201 #assert means
    body = r.json()
    assert body["email"] == EMAIL
    assert body["role"] == "viewer"
    assert "password" not in body and "password_hash" not in body

def test_register_cannot_choose_role(client):
    r = register(client, role="admin")
    assert r.status_code == 201
    assert r.json()["role"] == "viewer"

def test_register_duplicate(client):
    register(client)
    assert register(client).status_code == 409

def test_register_weak_password(client):
    assert register(client, password="short").status_code == 422

def test_login_success(client):
    register(client)
    r = login(client)
    assert r.status_code == 200
    assert r.json()["token_type"] == "bearer"

def test_login_wrong_password(client):
    register(client)
    assert login(client, password="WrongPass123").status_code == 401

def test_login_unknown_user_same_message(client):
    register(client)
    a = login(client, password="WrongPass123")
    b = login(client, email="nobody@example.com")
    assert a.status_code == b.status_code == 401
    assert a.json() == b.json()

def test_me_requires_token(client):
    assert client.get("/auth/me").status_code == 401

def test_me_with_token(client):
    r = client.get("/auth/me", headers=auth_header(client))
    assert r.status_code == 200
    assert r.json()["email"] == EMAIL

def test_tampered_token_rejected(client):
    headers = auth_header(client)
    headers["Authorization"] += "x"
    assert client.get("/auth/me", headers=headers).status_code == 401

def test_viewer_cannot_access_admin(client):
    r = client.get("/admin/users", headers = auth_header(client))
    assert r.status_code == 403