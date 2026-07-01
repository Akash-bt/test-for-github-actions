from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Simple FastAPI REST API")


# -----------------------------
# Data Model
# -----------------------------
class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False


# Temporary in-memory database
todos: List[Todo] = []


# -----------------------------
# Root API
# -----------------------------
@app.get("/")
def root():
    return {
        "message": "Welcome to the FastAPI Todo API"
    }


# -----------------------------
# Create Todo
# POST /todos
# -----------------------------
@app.post("/todos")
def create_todo(todo: Todo):
    for existing_todo in todos:
        if existing_todo.id == todo.id:
            raise HTTPException(status_code=400, detail="Todo ID already exists")

    todos.append(todo)
    return {
        "message": "Todo created successfully",
        "todo": todo
    }


# -----------------------------
# Get All Todos
# GET /todos
# -----------------------------
@app.get("/todos")
def get_all_todos():
    return {
        "count": len(todos),
        "todos": todos
    }


# -----------------------------
# Get Todo By ID
# GET /todos/{todo_id}
# -----------------------------
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo

    raise HTTPException(status_code=404, detail="Todo not found")


# -----------------------------
# Update Todo
# PUT /todos/{todo_id}
# -----------------------------
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated_todo
            return {
                "message": "Todo updated successfully",
                "todo": updated_todo
            }

    raise HTTPException(status_code=404, detail="Todo not found")


# -----------------------------
# Delete Todo
# DELETE /todos/{todo_id}
# -----------------------------
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            deleted_todo = todos.pop(index)
            return {
                "message": "Todo deleted successfully",
                "todo": deleted_todo
            }

    raise HTTPException(status_code=404, detail="Todo not found")