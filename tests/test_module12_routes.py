"""API integration tests: uses the real configured database and rolls back test data."""
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.users import get_engine, get_session


@pytest.fixture
def client():
    engine = get_engine()
    with engine.connect() as connection:
        outer_transaction = connection.begin()
        try:
            def testing_session():
                # create_savepoint protects the outer rollback even if routes commit.
                with Session(bind=connection, join_transaction_mode="create_savepoint") as session:
                    yield session
            app.dependency_overrides[get_session] = testing_session
            with TestClient(app) as client:
                yield client
        finally:
            app.dependency_overrides.pop(get_session, None)
            outer_transaction.rollback()


def test_register_login_password_security_and_conflict(client):
    username = "module12_" + uuid4().hex[:12]
    payload = {"username": username, "email": username + "@example.com", "password": "SafePassword123!"}
    registered = client.post("/users/register", json=payload)
    assert registered.status_code == 201
    data = registered.json()
    assert data["username"] == username
    assert "password" not in data
    assert "password_hash" not in data

    with Session(get_engine()) as another_session:
        # A separate DB session sees committed rows in real deployments;
        # our fixture transaction remains uncommitted, so use the API here.
        pass

    logged_in = client.post("/users/login", json={"username": username, "password": payload["password"]})
    assert logged_in.status_code == 200
    assert logged_in.json()["id"] == data["id"]
    assert "password_hash" not in logged_in.json()

    assert client.post("/users/login", json={"username": username, "password": "bad-password"}).status_code == 401
    assert client.post("/users/login", json={"username": "no_such_user", "password": "bad"}).status_code == 401
    assert client.post("/users/register", json=payload).status_code == 409
    assert client.get(f"/users/{data['id']}").status_code == 200


def test_registration_validation(client):
    invalid = client.post("/users/register", json={"username": "a", "email": "nope", "password": "123"})
    assert invalid.status_code == 422


def test_calculation_bread_lifecycle(client):
    initial = client.get("/calculations")
    assert initial.status_code == 200
    assert isinstance(initial.json(), list)

    created = client.post("/calculations", json={"a": 10, "b": 5, "type": "Add"})
    assert created.status_code == 201
    item = created.json()
    assert item["result"] == 15
    calc_id = item["id"]

    listed = client.get("/calculations")
    assert listed.status_code == 200
    assert any(item["id"] == calc_id for item in listed.json())

    fetched = client.get(f"/calculations/{calc_id}")
    assert fetched.status_code == 200
    assert fetched.json()["type"] == "Add"

    updated = client.put(f"/calculations/{calc_id}", json={"a": 20, "b": 4, "type": "Divide"})
    assert updated.status_code == 200
    assert updated.json()["result"] == 5
    assert client.get(f"/calculations/{calc_id}").json()["result"] == 5

    deleted = client.delete(f"/calculations/{calc_id}")
    assert deleted.status_code == 204
    assert client.get(f"/calculations/{calc_id}").status_code == 404


def test_calculation_validation_and_missing_records(client):
    assert client.post("/calculations", json={"a": 10, "b": 0, "type": "Divide"}).status_code == 422
    assert client.post("/calculations", json={"a": 1, "b": 2, "type": "Power"}).status_code == 422
    assert client.post("/calculations", json={"a": "abc", "b": 2, "type": "Add"}).status_code == 422
    assert client.get("/calculations/999999999").status_code == 404
    assert client.put("/calculations/999999999", json={"a": 1, "b": 2, "type": "Add"}).status_code == 404
    assert client.delete("/calculations/999999999").status_code == 404
