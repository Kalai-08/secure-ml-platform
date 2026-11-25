from types import SimpleNamespace

from app.deps import get_current_user
from app.models import Role

VALID = {
    "mean_radius" : 22,
    "mean_texture": 25,
    "mean_perimeter": 150,
    "mean_area": 1500
}

def register_and_login(client, email="viewer@example.com", password="StrongPass123"):
    client.post(
        "/auth/register",
        json={
            "email" : email,
            "password": password
        }
    )
    r = client.post(
        "/auth/login",
        data={
            "username": email,
            "password" : password
        }
    )

    return{
        "Authorization": f"Bearer {r.json()['access_token']}"
    }

def fake_analyst():
    return SimpleNamespace(
        id=1,
        email="viewer@example.com",
        role = Role.analyst
    )

def test_predict_requires_login(client):
    assert client.post(
        "/predict",
        json=VALID
    ).status_code == 401

def test_viewer_cannot_predict(client):
    headers = register_and_login(client)
    r = client.post(
        "/predict",
        json=VALID,
        headers=headers
    )
    assert r.status_code == 403

def test_analyst_can_predict(client):
    register_and_login(client)
    client.app.dependency_overrides[get_current_user] = fake_analyst
    try:
        r = client.post("/predict", json=VALID)
        assert r.status_code == 200
        assert r.json()["prediction"] in ("benign", "malignant")
    finally:
        client.app.dependency_overrides.pop(get_current_user, None)

def test_predict_rejects_bad_input(client):
    register_and_login(client)
    client.app.dependency_overrides[get_current_user] = fake_analyst
    try:
        bad = {**VALID, "mean_radius" : -5}
        assert client.post("/predict", json=bad).status_code == 422
    finally:
        client.app.dependency_overrides.pop(get_current_user, None)