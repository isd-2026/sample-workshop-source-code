# Week 7 — Model of MVC: DAL, Blueprints, Routes & API Key

## What's new this week

Week 6 created the database connection and schema. Week 7 builds everything on top — CRUD operations, API routes, authentication, and access control. This is the **Model** layer of MVC.

### Changes from week 6

| Component | Week 6 | Week 7 |
|-----------|--------|--------|
| `app.py` | Single route (`POST /welcome`) | Factory pattern + Blueprints |
| Data access | `db_connect.py` + `db_init.py` only | Adds `db_crud.py` with full CRUD |
| Routes | None | `auth.py` (login/register) + `users.py` (admin CRUD) |
| Access control | None | API key decorator |
| Tests | Frontend E2E only | Backend DAL tests + route tests |
| Frontend | — | Unchanged from week 6 |

---

## Setup

### 1. Install dependencies (if not done previously)

```bash
pip install -r requirements.txt
```

### 2. Create the `db/` folder and initialise the database

```bash
cd week7
mkdir db
python -m backend.models.db_init
```

Verify:

```bash
sqlite3 db/app.db "SELECT * FROM users;"
```

> If you get `UNIQUE constraint failed`, see the Troubleshooting section below.

---

## Running the servers

### Terminal 1 — Backend

```bash
cd week7
python -m backend.app
```

### Terminal 2 — Frontend

```bash
cd week7
python -m http.server 8000 --directory ./frontend/
```

---

## API endpoints

Week 7 replaces the single `/welcome` route with a full set of RESTful endpoints:

### Authentication (`/auth`)

| Method | Endpoint | Description | Request body |
|--------|----------|-------------|-------------|
| POST | `/auth/login` | User login | `{"email": "...", "password": "..."}` |
| POST | `/auth/register` | User registration | `{"name": "...", "email": "...", "password": "...", "gender": "...", "favcol": "..."}` |

### User management (`/users`)

| Method | Endpoint | Description | Request body | Access |
|--------|----------|-------------|-------------|--------|
| GET | `/users/list` | List all users | — | Requires API key |
| GET | `/users/view` | View single user | `{"email": "..."}` | Public |
| POST | `/users/add` | Add new user | `{"name": "...", "email": "...", ...}` | Public |
| POST | `/users/update` | Update user | `{"email": "...", "name": "..."}` | Public |
| DELETE | `/users/delete` | Delete user | `{"email": "..."}` | Public |

---

## Testing with Postman

### Register a new user

```
POST http://127.0.0.1:8080/auth/register
Body → raw → JSON:
{
    "name": "Alice",
    "email": "alice@email.com",
    "password": "pw",
    "gender": "f",
    "favcol": "blue"
}
```

Expected response (`201 Created`):

```json
{
    "status": "success",
    "message": "User Alice added successfully",
    "user": { "name": "Alice", "email": "alice@email.com", "gender": "f", "favcol": "blue" }
}
```

### Login

```
POST http://127.0.0.1:8080/auth/login
Body → raw → JSON:
{
    "email": "alice@email.com",
    "password": "pw"
}
```

Expected response (`200 OK`):

```json
{
    "status": "success",
    "message": "Login successful",
    "user": { "name": "Alice", "email": "alice@email.com", "gender": "f", "favcol": "blue" }
}
```

### Things to try — error cases

| Experiment | Expected status | Expected message |
|-----------|----------------|-----------------|
| Login with wrong password | 401 | "Incorrect password." |
| Login with non-existent email | 404 | "Email doesn't exist. Please register." |
| Register with existing email | 409 | "Email '...' already exists" |
| Login with empty email | 400 | "Email and password required" |

### List all users (requires API key)

```
GET http://127.0.0.1:8080/users/list
```

**Without** the API key header → `401 "Invalid or missing API key"`

**With** the API key header:

In Postman, click the **Headers** tab and add:

| Key | Value |
|-----|-------|
| x-api-key | admin-secret-key |

Then send → `200` with full user list.

### curl equivalents (Windows PowerShell)

```powershell
# Register
Invoke-RestMethod -Uri http://127.0.0.1:8080/auth/register -Method POST -ContentType "application/json" -Body '{"name":"Alice","email":"alice@email.com","password":"pw","gender":"f","favcol":"blue"}'

# Login
Invoke-RestMethod -Uri http://127.0.0.1:8080/auth/login -Method POST -ContentType "application/json" -Body '{"email":"alice@email.com","password":"pw"}'

# List users (with API key)
Invoke-RestMethod -Uri http://127.0.0.1:8080/users/list -Method GET -Headers @{"x-api-key"="admin-secret-key"}
```

---

## Running tests

All test commands from the `week7/` directory. No server needed — tests use Flask's built-in test client.

### DAL tests (tests `db_crud.py` functions directly)

```bash
python -m unittest backend.tests.test_db
python -m unittest -v backend.tests.test_db    # verbose
```

### Route/API tests (tests HTTP endpoints)

```bash
python -m unittest backend.tests.test_app
python -m unittest -v backend.tests.test_app   # verbose
```

### Run all backend tests

```bash
python -m unittest discover -s backend/tests
```

### Frontend E2E tests (unchanged from week 6, needs both servers running)

```bash
python -m unittest frontend.tests.e2e.test_register_e2e
```

---

## File overview

```
week7/
├── backend/
│   ├── __init__.py
│   ├── app.py                          ← CHANGED: factory pattern + Blueprint registration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── db_connect.py               ← SQLite connection factory (unchanged)
│   │   ├── db_init.py                  ← Creates users table + seeds data (unchanged)
│   │   └── db_crud.py                  ← NEW: CRUD functions (add, get, update, delete)
│   ├── routes/                         ← NEW FOLDER
│   │   ├── auth.py                     ← NEW: POST /auth/login, POST /auth/register
│   │   ├── users.py                    ← NEW: GET /users/list, POST /users/add, etc.
│   │   └── api_key_decorator.py        ← NEW: @require_api_key decorator
│   └── tests/                          ← NEW FOLDER
│       ├── test_db.py                  ← NEW: DAL unit tests (6 tests)
│       └── test_app.py                 ← NEW: Route/API tests (10 tests)
├── db/
│   └── app.db                          ← Created by db_init.py
└── frontend/                           ← Unchanged from week 6
```

---

## Key concepts this week

### MVC (Model-View-Controller)

An architectural pattern that separates an application into three layers:

- **View** — the frontend (HTML/CSS/JS), presents data to the user
- **Model** — the data layer (`db_crud.py`, `db_connect.py`), manages database access and business rules
- **Controller** — the routes (`auth.py`, `users.py`), receives requests, calls Model functions, returns responses

In ISD, the View is a separate frontend app. The Controller and Model live in the backend.

### Flask Blueprints

Blueprints organise routes into modular groups. Each Blueprint is defined in its own file and registered with the app:

```python
# In auth.py
auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/login', methods=["POST"])
def login():
    ...

# In app.py
app.register_blueprint(auth_bp, url_prefix="/auth")
# Result: POST /auth/login
```

The `url_prefix` prepends to every route in that Blueprint.

### Data Access Layer (DAL)

A set of functions that handle all database operations. Routes call DAL functions instead of writing SQL directly:

```
Route receives request → calls DAL function → DAL executes SQL → returns result → Route formats response
```

This is not an ORM — we still write raw SQL with parameterised queries (`?` placeholders).

### CRUD

The four basic database operations:

| Operation | SQL | DAL function | HTTP method |
|-----------|-----|-------------|-------------|
| **C**reate | `INSERT INTO` | `add_user()` | POST |
| **R**ead | `SELECT` | `get_user_by_email()`, `get_all_users()` | GET |
| **U**pdate | `UPDATE` | `update_user()` | POST |
| **D**elete | `DELETE FROM` | `delete_user()` | DELETE |

### API key authentication

A simple access control mechanism — the client must send a secret key in the request header:

```
x-api-key: admin-secret-key
```

The `@require_api_key` decorator checks this header before allowing access to the endpoint. In this codebase, the key is hardcoded. In production, keys would be generated dynamically and stored securely.

### HTTP status codes

| Code | Meaning | When used |
|------|---------|-----------|
| 200 | OK | Successful read/update/delete |
| 201 | Created | Successful registration / user creation |
| 400 | Bad Request | Missing fields, invalid data |
| 401 | Unauthorized | Wrong password, missing/invalid API key |
| 404 | Not Found | User/email doesn't exist |
| 409 | Conflict | Email already registered |

### Response format

All endpoints return a consistent JSON structure:

```json
{
    "status": "success" or "error",
    "message": "Human-readable description",
    "user": { ... }    // optional, included when relevant
}
```

### What's coming next

- **Week 8:** Controllers separate business logic from routes → full MVC separation
- **Week 9:** Frontend connects to backend with `fetch()` → the form finally writes to the database

---

## Stopping servers

Press `Ctrl+C` in the terminal. If the port is stuck:

**Windows:**
```powershell
netstat -ano | findstr :8080
taskkill /PID <PID_number> /F
```

**Mac/Linux:**
```bash
lsof -i :8080
kill -9 <PID>
```

---

## Troubleshooting

### `sqlite3.IntegrityError: UNIQUE constraint failed: users.email`

Running `db_init.py` more than once tries to re-insert the seed users. Fix:

```bash
sqlite3 db/app.db "DROP TABLE IF EXISTS users;"
python -m backend.models.db_init
```

Or delete the database file and re-initialise:

```powershell
Remove-Item db\app.db          # Windows
# rm db/app.db                 # Mac/Linux
python -m backend.models.db_init
```

### `ModuleNotFoundError: No module named 'backend'`

Make sure you're running from the `week7/` directory.

### Tests fail with database errors

The tests modify the database. If tests leave stale data, reset:

```bash
sqlite3 db/app.db "DELETE FROM users WHERE name LIKE 'TU%';"
```

Or drop and re-init the table.

### `ResourceWarning: unclosed database in <sqlite3.Connection ...>`

These warnings appear because `db_init.py` runs `init_db()` automatically when imported, and some connections don't get cleanly closed during the import chain. They are **warnings, not errors** — your tests still run. To suppress them, change the bottom of `db_init.py` from:

```python
init_db()
```

To:

```python
if __name__ == "__main__":
    init_db()
```

Then initialise manually with `python -m backend.models.db_init` instead of relying on auto-import.

### `test_list_users_route` fails with `KeyError: 'user_list'`

The test calls `GET /users/list` without the API key header, so the `@require_api_key` decorator rejects the request with a 401 error — the response has no `user_list` key. Fix line 61 in `test_app.py`:

```python
# Before (missing API key)
response3 = self.app.get('/users/list')

# After (with API key)
response3 = self.app.get('/users/list', headers={"x-api-key": "admin-secret-key"})
```

### `test_login_session_variable` fails with `KeyError: 'user_email'` or `RuntimeError: Session backend did not open a session`

This test requires two things that are commented out by default:

**1. Uncomment `secret_key` in `app.py`:**

```python
# Before
# app.secret_key = "test-secret-key"

# After
app.secret_key = "test-secret-key"
```

**2. Uncomment the session write and add `session` to the import in `auth.py`:**

```python
# At the top of auth.py — add session to the import
from flask import Blueprint, jsonify, request, session

# Inside the login() function — uncomment the session line
session["user_email"] = user_row[2]
```

### `test_logout_route` fails with `AssertionError: 404 != 200`

There is no `/auth/logout` route defined in `auth.py`. Add it at the bottom of the file (at the **top level**, not indented inside another function):

```python
@auth_bp.route('/logout', methods=["GET"])
def logout():
    session.clear()
    return jsonify({"status": "success", "message": "Logged out successfully"}), 200
```

Make sure `session` is imported at the top of the file (see the fix above).

### Debugging: check what routes Flask has registered

If a route returns 404 but you think it should exist, check the route map:

```bash
python -c "from backend.app import create_app; app = create_app(); print([str(r) for r in app.url_map.iter_rules()])"
```

This prints all registered URLs. Look for your missing route in the output. If it's not there, the route definition isn't being loaded — check the file is saved, the decorator indentation is correct, and the Blueprint is registered in `app.py`.

### Run a single test to isolate failures

Instead of running all tests, target one specific test:

```bash
python -m unittest backend.tests.test_app.AppTestCase.test_logout_route
```

The dotted path is: `module.Class.method`. This helps you fix tests one at a time without noise from other failures.

### VS Code shows `Import "flask" could not be resolved`

Press `Ctrl+Shift+P` → **Python: Select Interpreter** → pick the interpreter where Flask is installed.
