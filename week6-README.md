# Week 6 — Database Design, SQLite & E2E Testing

## What's new this week

Week 5 stored data in Python lists (in-memory) — it vanished when the server stopped. Week 6 introduces a **real database** using SQLite that persists data to a file on disk.

### Changes from week 5

| Component | Week 5 | Week 6 |
|-----------|--------|--------|
| Data storage | `DB` class with Python lists | SQLite database (`app.db` file) |
| Backend | `project_bidding.py` (domain logic) | `models/db_connect.py` + `models/db_init.py` |
| Frontend validation | None | `required` attributes + JS validation |
| Testing | Unit tests (`unittest`) | E2E tests (Selenium + real browser) |

---

## Setup

### 1. Install SQLite CLI (one-time)

The `sqlite3` Python module is built into Python and works without any extra install. However, to inspect your database from the command line (which is very useful for debugging), you need the **SQLite CLI tool**.

**Windows (PowerShell as Administrator):**

```powershell
winget install SQLite.SQLite
```

After installing, the `sqlite3` command is added to your system PATH — but only **new** terminal windows will pick it up. If you want to use it in your current terminal without restarting, run this once to refresh the PATH:

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

**Mac:**

SQLite CLI comes pre-installed on macOS. If for some reason it's missing or you want the latest version:

```bash
brew install sqlite
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt install sqlite3
```

**Verify it's working (all platforms):**

```bash
sqlite3 --version
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

For E2E tests, you also need **Chrome** installed on your machine.

### 3. Create the `db/` folder

The database file lives in `week6/db/`. This folder does not exist in the repo by default — you need to create it before initialising the database:

```bash
cd week6
mkdir db
```

### 4. Initialise the database

```bash
cd week6
python -m backend.models.db_init
```

This creates `week6/db/app.db` with a `users` table and 3 seed users (YH, LG, SG).

To verify it worked:

```bash
sqlite3 db/app.db "SELECT * FROM users;"
```

---

## Running the servers

You need **two terminals**, both from the `week6/` directory.

### Terminal 1 — Backend (Flask API on port 8080)

```bash
cd week6
python -m backend.app
```

### Terminal 2 — Frontend (static files on port 8000)

```bash
cd week6
python -m http.server 8000 --directory ./frontend/
```

### Frontend pages

| URL | Page |
|-----|------|
| http://127.0.0.1:8000/index.html | Home page |
| http://127.0.0.1:8000/register.html | Registration form (with validation) |
| http://127.0.0.1:8000/welcome.html | Welcome page |

> Note: you must include `.html` in the URL.

---

## Inspecting the database with SQLite CLI

The API endpoint (`POST /welcome`) is unchanged from week 5 — covered last week. This week's focus is on the **database layer**.

After initialising the database (step 4 above), you can interact with it directly using the SQLite CLI. This is useful for debugging and verifying your data.

### Open the database

```bash
cd week6
sqlite3 db/app.db
```

You'll enter the SQLite interactive shell (prompt changes to `sqlite>`).

### Useful commands

| Command | What it does |
|---------|-------------|
| `.tables` | List all tables in the database |
| `.schema users` | Show the `CREATE TABLE` statement for the `users` table |
| `SELECT * FROM users;` | Show all rows in the `users` table |
| `SELECT name, email FROM users;` | Show specific columns only |
| `SELECT * FROM users WHERE email = 'yh@email.com';` | Filter by condition |
| `.headers on` | Show column names in query results |
| `.mode column` | Format output in aligned columns (easier to read) |
| `.quit` | Exit the SQLite shell |

### Quick one-liner (without entering the shell)

```bash
sqlite3 db/app.db "SELECT * FROM users;"
```

### Try it — insert a user manually

```sql
INSERT INTO users (name, email, password, gender, favcol)
VALUES ('Test User', 'test@email.com', 'pw', 'f', 'blue');
```

Then verify:

```sql
SELECT * FROM users;
```

You should see 4 rows now (3 seeded + 1 you just added).

### Try it — test the UNIQUE constraint

```sql
INSERT INTO users (name, email, password, gender, favcol)
VALUES ('Duplicate', 'yh@email.com', 'pw', 'm', 'red');
```

This will fail with `UNIQUE constraint failed: users.email` because `yh@email.com` already exists. This is the database enforcing data integrity — even if the application code has bugs, the database won't allow duplicate emails.

### Important: commit vs rollback

If you close the connection (`conn.close()` in Python) **without** calling `conn.commit()`, SQLite automatically rolls back all uncommitted changes. Nothing gets saved. This is a safety mechanism — if your code crashes mid-operation, the database stays consistent.

> **Note:** The frontend registration form does NOT write to this database in week 6. The form still saves to `sessionStorage` only. The frontend → database connection is built across weeks 7–9.

---

## Running E2E tests

E2E (End-to-End) tests use **Selenium** to automate a real Chrome browser. Unlike unit tests, E2E tests require both servers to be running.

### Prerequisites

- Chrome browser installed
- ChromeDriver matching your Chrome version (or `pip install chromedriver-autoinstaller`)
- Both frontend (port 8000) and backend (port 8080) servers running

### Run the tests

```bash
# Terminal 3 (with both servers running in terminals 1 and 2)
cd week6
python -m unittest frontend.tests.e2e.test_register_e2e
```

### Run with verbose output

```bash
python -m unittest -v frontend.tests.e2e.test_register_e2e
```

Expected output:

```
test_email_empty (frontend.tests.e2e.test_register_e2e.TestRegister) ... ok
test_name_empty (frontend.tests.e2e.test_register_e2e.TestRegister) ... ok
test_password_empty (frontend.tests.e2e.test_register_e2e.TestRegister) ... ok
test_register_successful (frontend.tests.e2e.test_register_e2e.TestRegister) ... ok
test_tos_not_ticked (frontend.tests.e2e.test_register_e2e.TestRegister) ... ok
----------------------------------------------------------------------
Ran 5 tests in 12.345s

OK
```

### What the E2E tests check

| Test | Action | Expected result |
|------|--------|-----------------|
| `test_name_empty` | Tick TOS, submit with all fields empty | Alert: "Please enter your name." |
| `test_email_empty` | Fill name only, submit | Inline error: "Please enter your email." |
| `test_password_empty` | Fill name + email, submit | Inline error: "Please enter your password." |
| `test_tos_not_ticked` | Fill all fields, untick TOS, submit | Alert: "You must agree to the Terms of Service." |
| `test_register_successful` | Fill all fields, tick TOS, submit | Redirects to `welcome.html` |

### Unit tests vs E2E tests

| | Unit test (week 5) | E2E test (week 6) |
|--|---|---|
| Tests | A single function/class | The whole app as a user sees it |
| Needs server? | No | Yes (both frontend + backend) |
| Speed | Milliseconds | Seconds (opens real browser) |
| Catches | Logic bugs | Integration bugs (HTML + JS + CSS + server) |

---

## File overview

```
week6/
├── backend/
│   ├── __init__.py                  ← Makes backend/ a Python package
│   ├── app.py                       ← Flask server (POST /welcome) — unchanged from week 5
│   └── models/
│       ├── __init__.py              ← Makes models/ a sub-package
│       ├── db_connect.py            ← NEW: SQLite connection factory
│       └── db_init.py               ← NEW: Creates users table + seeds 3 users
├── db/
│   └── app.db                       ← Created by db_init.py (not in git)
└── frontend/
    ├── index.html                   ← Home page
    ├── register.html                ← Registration form (adds required attributes)
    ├── register.js                  ← Form handler (adds validation logic)
    ├── welcome.html                 ← Welcome page
    ├── welcome.js                   ← Reads user from sessionStorage
    ├── logout.html                  ← Logout confirmation
    ├── style.css                    ← Shared styles
    ├── sunflower.jfif               ← Sample image
    └── tests/
        └── e2e/
            ├── __init__.py
            └── test_register_e2e.py ← NEW: Selenium E2E tests (5 tests)
```

---

## Key concepts this week

### SQLite

SQLite is a file-based database built into Python. No installation, no server process — the database is just a `.db` file. Perfect for development and learning.

### The connection pattern

Every database operation follows this pattern:

```python
conn = get_connection()     # 1. Open connection
cursor = conn.cursor()      # 2. Create cursor
cursor.execute("SQL ...")   # 3. Run query
conn.commit()               # 4. Save changes (for INSERT/UPDATE/DELETE)
conn.close()                # 5. Release connection
```

The connection is **stateful** — it tracks the current transaction, cursor position, and uncommitted changes. A transaction starts automatically when the first database-modifying SQL statement (`INSERT`, `UPDATE`, `DELETE`) is executed, and lasts until you either `commit()` (save) or `close()` without committing (rollback).

### Parameterised queries (prevent SQL injection)

```python
# DANGEROUS — never do this
cursor.execute(f"INSERT INTO users VALUES ('{name}', '{email}')")

# SAFE — always use ? placeholders
cursor.execute("INSERT INTO users VALUES (?, ?)", (name, email))
```

### Relational database concepts

A relational database stores data in **tables** that are related to each other. Each row is a **record** (entity), each column is an **attribute**. The **schema** defines the structure: column names, data types, and constraints.

### Primary key and foreign key

A **primary key** uniquely identifies each row. It is always `UNIQUE` and `NOT NULL`. In our `users` table, `id INTEGER PRIMARY KEY AUTOINCREMENT` auto-generates a unique ID for each user.

A **foreign key** links one table to another — it's a column that references a primary key in a different table. We'll use foreign keys in later weeks when we add projects and allocations.

### Data types and constraints

| Constraint | What it enforces |
|-----------|-----------------|
| `PRIMARY KEY` | Unique + required (identifies each row) |
| `NOT NULL` | Cannot be empty |
| `UNIQUE` | No duplicate values allowed |
| `FOREIGN KEY` | Must match an existing primary key in another table |
| `CHECK` | Must satisfy a condition (e.g., `CHECK(age > 0)`) |
| `DEFAULT` | Uses a default value if none is provided |

In our schema: `email TEXT NOT NULL UNIQUE` means every user must have an email, and no two users can share the same email. The database enforces this even if the application code doesn't check.

### No multi-valued fields (First Normal Form)

Each cell in a table should contain only **one value**. This is called First Normal Form (1NF).

Bad — multi-valued cell:

| Student | Subjects |
|---------|----------|
| Alice | Math, Science |

Good — one value per cell:

| Student | Subject |
|---------|---------|
| Alice | Math |
| Alice | Science |

### Many-to-many relationships

When one student can enrol in multiple subjects and one subject can have multiple students, that's a **many-to-many** relationship. Relational databases can't store this directly — you need a **junction table** (e.g., `Enrolments`) that contains foreign keys to both tables.

In later weeks, `Allocations` serves this role — linking students to projects.

### Entity-Relationship Diagram (ERD)

An ERD visually represents tables and their relationships. Each table is a box with its columns listed, and lines between boxes show foreign key relationships with cardinality (one-to-one, one-to-many, many-to-many).

### What's coming next

- **Week 7:** Data Access Layer with full CRUD functions (`add_user`, `get_user_by_email`, `update_user`, `delete_user`) + Flask Blueprints + Routes → building the Model in MVC
- **Week 8:** Controllers separate business logic from routes → full MVC pattern
- **Week 9:** Frontend connects to backend with `fetch()` → registration form finally writes to the database

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

This happens when you run `python -m backend.models.db_init` more than once — the seed users (YH, LG, SG) already exist from the first run, and the `UNIQUE` constraint on `email` blocks the duplicate inserts.

**Option A — Drop the table and re-initialise (quick reset):**

```bash
sqlite3 db/app.db "DROP TABLE IF EXISTS users;"
python -m backend.models.db_init
```

Or interactively in the SQLite shell:

```bash
sqlite3 db/app.db
```

```sql
DROP TABLE IF EXISTS users;
.quit
```

Then run `python -m backend.models.db_init` again.

**Option B — Delete the entire database file and start fresh:**

```powershell
# Windows
Remove-Item db\app.db
python -m backend.models.db_init
```

```bash
# Mac/Linux
rm db/app.db
python -m backend.models.db_init
```

**Option C — Fix `db_init.py` to be re-runnable (recommended):**

Change `INSERT INTO` to `INSERT OR IGNORE INTO` in `db_init.py`. This tells SQLite to silently skip the insert if the email already exists, instead of raising an error:

```python
    cursor.execute("""
            INSERT OR IGNORE INTO users (name, email, password, gender, favcol)
            VALUES (?, ?, ?, ?, ?)
        """, ("YH", "yh@email.com", "pw", "f", "yellow"))
    conn.commit()

    cursor.execute("""
            INSERT OR IGNORE INTO users (name, email, password, gender, favcol)
            VALUES (?, ?, ?, ?, ?)
        """, ("LG", "lg@email.com", "pw", "m", "yellow"))
    conn.commit()

    cursor.execute("""
            INSERT OR IGNORE INTO users (name, email, password, gender, favcol)
            VALUES (?, ?, ?, ?, ?)
        """, ("SG", "sg@email.com", "pw", "m", "yellow"))
    conn.commit()
```

Combined with `CREATE TABLE IF NOT EXISTS`, this makes `db_init.py` fully **idempotent** — safe to run any number of times without errors.

### `ModuleNotFoundError: No module named 'backend'`
Make sure you're running from the `week6/` directory, not from `week6/backend/`.

### `sqlite3.OperationalError: no such table: users`
Run `python -m backend.models.db_init` first to create the table.

### E2E tests fail with `WebDriverException`
ChromeDriver version must match your Chrome browser version. Check your Chrome version at `chrome://version` and download the matching ChromeDriver, or use `pip install chromedriver-autoinstaller`.

### VS Code shows `Import "flask" could not be resolved`
Press `Ctrl+Shift+P` → **Python: Select Interpreter** → pick the interpreter where Flask is installed.
