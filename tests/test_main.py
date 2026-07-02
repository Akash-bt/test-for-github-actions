from fastapi.testclient import TestClient
from main import app, todos

client = TestClient(app)


def setup_function():
    """
    This runs before every test function.

    Since our app uses an in-memory list as a fake database,
    we clear it before every test so that one test does not affect another test.
    """
    todos.clear()


def test_root_api():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the FastAPI Todo API"
    }


def test_create_todo():
    payload = {
        "id": 1,
        "title": "Learn FastAPI",
        "completed": False
    }

    response = client.post("/todos", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Todo created successfully"
    assert response.json()["todo"] == payload


def test_get_all_todos():
    client.post("/todos", json={
        "id": 1,
        "title": "Learn FastAPI",
        "completed": False
    })

    response = client.get("/todos")

    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert response.json()["todos"][0]["title"] == "Learn FastAPI"


def test_get_todo_by_id():
    client.post("/todos", json={
        "id": 1,
        "title": "Learn FastAPI",
        "completed": False
    })

    response = client.get("/todos/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Learn FastAPI"
    assert response.json()["completed"] is False


def test_get_todo_not_found():
    response = client.get("/todos/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_create_duplicate_todo_id():
    payload = {
        "id": 1,
        "title": "Learn FastAPI",
        "completed": False
    }

    client.post("/todos", json=payload)
    response = client.post("/todos", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Todo ID already exists"


def test_update_todo():
    client.post("/todos", json={
        "id": 1,
        "title": "Learn FastAPI",
        "completed": False
    })

    updated_payload = {
        "id": 1,
        "title": "Learn FastAPI with Docker",
        "completed": True
    }

    response = client.put("/todos/1", json=updated_payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Todo updated successfully"
    assert response.json()["todo"] == updated_payload


def test_update_todo_not_found():
    updated_payload = {
        "id": 999,
        "title": "This todo does not exist",
        "completed": True
    }

    response = client.put("/todos/999", json=updated_payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_delete_todo():
    client.post("/todos", json={
        "id": 1,
        "title": "Learn FastAPI",
        "completed": False
    })

    response = client.delete("/todos/1")

    assert response.status_code == 200
    assert response.json()["message"] == "Todo deleted successfully"
    assert response.json()["todo"]["id"] == 1

    get_response = client.get("/todos/1")
    assert get_response.status_code == 404


def test_delete_todo_not_found():
    response = client.delete("/todos/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"

def test_intentional_failure_wrong_root_message():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "This message is intentionally wrong"
    }


def test_intentional_failure_wrong_todo_count():
    response = client.get("/todos")

    assert response.status_code == 200
    assert response.json()["count"] == 999