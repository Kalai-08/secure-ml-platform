import pytest #pytest is a testing framework for Python that allows you to write test cases for the code.
from fastapi.testclient import TestClient
from sqlalchemy import create_engine #create_engine is used to create a new database engine instance
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool #StaticPool for used same connection everywhere in this project

import app.models
from app.core.database import Base, get_db
from app.main import app

@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass= StaticPool
    )

    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c #it will yield the TestClient instance to the test function, allowing it to make requests to the FastAPI application.
    app.dependency_overrides.clear()
    engine.dispose()