# ISD 2026 - Weekly Workshop Guide

This repository contains progressive weekly exercises for building a **Project Management System** with Flask (backend) and HTML/React (frontend).

---

## 📋 Weekly Overview

| Week | Topics Covered | Key Concepts |
|------|----------------|--------------|
| **4** | Frontend Basics | HTML forms, CSS Styling, JavaScript DOM, Navigation Parameters, Frontend `sessionStorage` |
| **5** | Flask Backend & Unit Testing | Flask, API Endpoints, `unittest` |
| **6** | Database & E2E Testing | Relational Database, SQLite, `sqlite3`, E2E Testing with Selenium |
| **7** | Model of MVC | Model-View-Controller (MVC), Data Access Layer (DAL), Flask Blueprint, Admin Functionality (API Key) |
| **8** | Controller of MVC | Controller, Data Access Object (DAO), API Testing |
| **9** | Frontend-Backend Integration | `fetch()`, CORS, Backend `session`, UML Sequence Diagram |
| **10** | Extending the Data Model & Software Features | Projects, Allocations, Entity-Relationship-Diagram (ERD) |
| **11** | React Frontend | React Components, React Router, State Management |

---

## 🚀 Getting Started

### Prerequisites

1. **Python 3.x** - [Download](https://www.python.org/downloads/)
2. **Node.js** (for Week 11) - [Download](https://nodejs.org/)
3. **Git** - [Download](https://git-scm.com/downloads)

### Activate Python Virtual Environment

```bash
pip install venv # install python venv module
python -n venv <virtual-environment-name> # create a virtual environment
source /<virtual-environment-name>/Scripts/activate # activate the virtual environment
deactivate # deactivate the virtual environment
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## 📂 Project Structure

Each week folder follows this structure:

```
weekX/
├── backend/
│   ├── app.py              # Flask application entry point
│   ├── controllers/        # Business logic (Week 8+)
│   ├── models/             # Database models & CRUD operations
│   ├── routes/             # API endpoints (Blueprints)
│   └── tests/              # Unit tests
└── frontend/               # HTML/CSS/JS files (or frontend-react/ for Week 11)
```

---

## ▶️ How to Run Each Week

**Always run commands from the `weekX/` folder!**

### Start the Backend Server

```bash
cd week9  # or any week folder
python -m backend.app
```

The server runs at: `http://127.0.0.1:8080`

### Start the Frontend Server

```bash
cd week9  # or any week folder
python -m http.server 8000 --directory ./frontend/
```

Open your browser at: `http://127.0.0.1:8000`

### Run Unit Tests

```bash
# Backend tests (no server needed)
python -m unittest backend/tests/test_app.py
```

### Run E2E Tests
``` bash
python -m unittest frontend/tests/e2e/test_login_e2e.py
```

### Week 11 - React Frontend

```bash
cd week11/frontend-react
npm install
npm run dev
```

Alternatively, to run it in the `weekX/` folder,

```
npm --prefix ./frontend-react run dev
```

---

## 📖 Week-by-Week Details

### Week 4: Frontend Basics

**Focus:** Building the registration form UI

**Key Files:**
- `frontend/register.html` - Registration form with validation
- `frontend/register.js` - Form handling with `sessionStorage`
- `frontend/welcome.html` - User welcome page
- `frontend/style.css` - Basic styling

**Learning Goals:**
- HTML form structure
- CSS styling and layout
- JavaScript event handling
- Client-side data storage with `sessionStorage`

---

### Week 5: Flask Backend & Unit Testing

**Focus:** Backend domain logic with classes

**Key Files:**
- `backend/project_bidding.py` - User, Project, Allocation classes
- `backend/test_project_bidding.py` - Unit tests
- `backend/app.py` - Simple Flask endpoint

**Learning Goals:**
- Python classes and objects
- Writing unit tests with `unittest`
- Test-driven development concepts

---

### Week 6: Database & E2E Testing

**Focus:** SQLite database connection

**Key Files:**
- `backend/models/db_connect.py` - Database connection helper
- `backend/models/db_init.py` - Table creation script
- `backend/tests/test_db.py` - Database connection tests

**Learning Goals:**
- SQLite database basics
- Python `sqlite3` module
- Database schema design

---

### Week 7: Model of MVC

**Focus:** Building RESTful endpoints with Flask Blueprints

**Key Files:**
- `backend/routes/auth.py` - Login/Register endpoints
- `backend/routes/users.py` - User CRUD endpoints
- `backend/routes/api_key_decorator.py` - API key authentication
- `backend/models/db_crud.py` - Database CRUD operations

**API Endpoints:**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | User login |
| POST | `/auth/register` | User registration |
| GET | `/users/list` | List all users (requires API key) |
| POST | `/users/add` | Add new user |
| DELETE | `/users/delete` | Delete user |

**Learning Goals:**
- Flask Blueprints for route organization
- RESTful API design
- API key authentication

---

### Week 8: Controller of MVC

**Focus:** Separating concerns with controllers

**Key Files:**
- `backend/controllers/auth_controller.py` - Auth business logic
- `backend/controllers/user_controller.py` - User business logic
- `backend/models/user.py` - User model class

**Learning Goals:**
- Model-View-Controller pattern
- Input validation (email, password)
- Separating routes from business logic

---

### Week 9: Frontend-Backend Integration

**Focus:** Connecting frontend to Flask API

**Key Files:**
- `frontend/login.js` - Login with `fetch()` API
- `frontend/register.js` - Registration with `fetch()` API
- `backend/app.py` - CORS configuration

**Learning Goals:**
- JavaScript `fetch()` API
- Handling API responses
- CORS (Cross-Origin Resource Sharing)
- Form validation (frontend + backend)

---

### Week 10: Extending the Data Model & Software Features

**Focus:** Complete project management system

**New Features:**
- Project management (CRUD)
- Student-to-project allocations
- Admin-only operations

**Key Files:**
- `backend/routes/projects.py` - Project endpoints
- `backend/routes/allocations.py` - Allocation endpoints
- `frontend/project-dashboard.js` - Project listing
- `frontend/project-form.js` - Create/Edit projects

**Learning Goals:**
- Multi-table relationships
- Role-based access (admin vs student)
- Complex CRUD operations

---

### Week 11: React Frontend

**Focus:** Modern React SPA (Single Page Application)

**Key Files:**
- `frontend-react/src/App.jsx` - React Router setup
- `frontend-react/src/components/Login.jsx` - Login component
- `frontend-react/src/components/Register.jsx` - Registration component
- `frontend-react/src/components/ProjectDashboard.jsx` - Project list

**Learning Goals:**
- React functional components
- React hooks (`useState`, `useEffect`)
- React Router for navigation
- Converting vanilla JS to React

---

## 🔑 Test Credentials

For testing login functionality:

| Role | Email | Password |
|------|-------|----------|
| User | Register a new account | Must contain: uppercase, lowercase, number, special char (@$#%) |
| Admin | (Check `db_init.py` for seeded data) | - |

**Password Requirements:** 6-20 characters with at least one uppercase, one lowercase, one number, and one special character (`@`, `$`, `#`, `%`)

---

## 🐛 Common Issues

### CORS Error
Make sure `flask-cors` is installed and the backend has:
```python
from flask_cors import CORS
CORS(app, origins=["http://127.0.0.1:8000"], supports_credentials=True) # specifies the URL of the frontend; note that localhost and 127.0.0.1 are considered different origins
```

### Database Not Found
Run the `db_init.py` script first:
```bash
python -c "from backend.models.db_init import init_db; init_db()"
```

### Port Already in Use
Kill the existing process or use a different port:
```bash
# Check what's using port 8080
lsof -i :8080
# Kill it
kill -9 <PID>
```

---

## 📚 Recommended Study Order

1. **Read the code** before running it
2. **Trace the data flow** from frontend → routes → controllers → models → database
3. **Modify and experiment** - break things, then fix them!
4. **Write additional tests** to verify your understanding

---

## 💡 Tips for Success

- Always run code from the `weekX/` directory
- Check browser console (F12) for JavaScript errors
- Use `Ctrl+R` to refresh/reload pages to clear cached content if needed
- Check terminal for Flask errors
- Use Postman or curl to test API endpoints directly
- Read error messages carefully - they usually tell you what's wrong!

---

Good luck with your workshops! 🎉