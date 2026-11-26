def login(client, email, password):
    return client.post(
        "/auth/login",
        data={
            "username" : email,
            "password" : password
        }
    )

def register(client, email, password="StrongPass123"):
    client.post(
        "/auth/register",
        json={
            "email" : email,
            "password" : password
        }
    )

def test_locked_after_5_failures(client):
    register(client, "victim@example.com")
    for _ in range(5):
        assert login(client, "victim@example.com", "WrongPass123").status_code == 401
    r = login(client, "victim@example.com", "WrongPass123")
    assert r.status_code == 429
    assert "retry-after" in r.headers

def test_correct_password_blocked_during_lockout(client):
    register(client, "victim@example.com")
    for _ in range(5):
        assert login(client, "victim@example.com", "WrongPass123")
    assert login(client, "victim@example.com", "StrongPass123").status_code == 429

def test_unknown_email_is_locked_too(client):
    for _ in range(5):
        assert login(client, "ghost@example.com", "WrongPass123").status_code == 401
    assert login(client, "ghost@example.com", "WrongPass123").status_code == 429

def test_other_account_not_affected(client):
    register(client, "victim@example.com")
    register(client, "other@example.com")

    for _ in range(5):
        login(client, "victim@example.com", "WrongPass123")
    assert login(client, "other@example.com", "StrongPass123").status_code == 200