# 🌍 Country Info System  

A full-featured web application that allows users to browse, search, filter, and manage country data. The project is built using **FastAPI** for backend development and supports both **RESTful APIs** and **HTML template rendering** for frontend delivery. The app uses data from the REST Countries API and integrates authentication, session handling, and database management.

---


## 📦 Project Overview

This project was developed in **four phases**:

### 🔹 Phase 1: Data Fetching and Storage
- Fetches country data from the [REST Countries API]( https://restcountries.com/v3.1/all).
- Stores data into a local SQLite database using SQLAlchemy models.

### 🔹 Phase 2: RESTful API Development
- Exposes RESTful endpoints to:
  - Get all countries
  - Filter by region or language
  - CRUD operations on country data (add/update/delete)
- Returns JSON responses for API clients.

### 🔹 Phase 3: Web Interface (HTML Template Rendering)
- Provides a user-friendly interface with:
  - Search and filter by name, region, or language
  - Detail view showing related countries and spoken languages
- Uses **Bootstrap** for UI design
- Pages rendered via Jinja2 templates using FastAPI’s `TemplateResponse`

### 🔹 Phase 4: Authentication and Security
- Implements user registration and login using form-based authentication.
- Protected routes: only authenticated users can access the country list, add, update, or delete data.
- Session-based authentication using Starlette’s `SessionMiddleware`.

---

## 🧠 Why FastAPI?

- FastAPI is a modern, high-performance web framework for building APIs with Python 3.7+ based on standard Python type hints.
- Excellent support for both RESTful API endpoints and template rendering.
- Async I/O for performance.
- Built-in support for dependency injection, which helps manage database and authentication logic cleanly.

---

## 💡 Why HTML Template Rendering?

Although the initial requirements emphasized RESTful APIs, HTML rendering was used to:
- Deliver a simple web-based interface for non-technical users.
- Enhance usability with server-side rendered forms and views.
- Reduce frontend complexity by not relying on a separate SPA frontend framework.

This hybrid approach ensures:
- API clients can consume JSON endpoints.
- Web users have a functional UI through HTML pages.

---

🔐 Authentication
Routes are protected using session-based authentication.

Logged-in users can:

View the full country list

Add, edit, delete, and filter countries

Unauthenticated users are redirected to the login page.

## 📦 Tech Stack

- **FastAPI**
- **SQLAlchemy**
- **SQLite** (default, can switch to PostgreSQL/MySQL)
- **Jinja2** for templates
- **Bootstrap 5** for UI
- **Uvicorn** (ASGI server)
- **Pydantic** for data validation

---

## Prerequisites

- Python 3.10 or higher
- pip
- virtualenv (recommended)

## ⚙️ Setup Instructions


### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/country-info-fastapi.git
cd country-info-fastapi
```

### 2. Create and activate a virtual environment

```bash
# Install specific Python version (if needed)
# For Ubuntu/Debian:

# Create virtual environment with Python 3.10
python3.10 -m venv env

# Activate the virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
virtualenv -p python3.10 env
env\Scripts\activate

```
### 3. Install Dependencies
```
pip install -r requirements.txt
```
### 4. Set Environment Variables
Create a .env file in the root folder:
```bash
# Database
DATABASE_URL=sqlite:///./codefusion.db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
### 5. Fetch Country Data (One-Time Script)
Initially, if database is not there, it will automatically create a database and ask for ```username```, ```email``` and ```password``` to ceate a demo user.   
```python scripts/fetch_and_store.py```

### 5. Run the App
```
uvicorn app.main:app --reload
```

🌐 Accessing the App
🔸 Web Interface (HTML Rendering)
After starting the server, visit:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)  

You'll be redirected to the login page. After signing in, you'll be able to view, search, filter, and manage countries via the UI.

🔸 API Documentation (Swagger UI)
FastAPI automatically provides documentation:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

You can test all REST API endpoints (including country data and auth) via this interface.


✅ Assignment Phases Covered
✔️ Phase 1: Data fetching and storage from external API.

✔️ Phase 2: RESTful API development.

✔️ Phase 3: Web interface with template rendering and Bootstrap.

✔️ Phase 4: Authentication and access control (login, signup, logout).


✅ RESTful API vs HTML Rendering Justification
While pure REST APIs return only JSON and are suitable for headless clients (mobile/web apps), many practical applications require a web interface for admin panels or user dashboards. Our project supports:

API consumption: for integration or automation

HTML rendering: for immediate human usability

This balanced architecture provides flexibility, clarity, and real-world utility.

## 📁 Project Structure
```bash
codefusion_ai/
├── app/
│   ├── api/                        # API routes (REST)
│   │   ├── countries.py
│   │   └── __init__.py 
│   ├── core/                        # Config and security
│   │   ├── config.py
│   │   ├── security.py  
│   ├── crud/                        # DB access functions
│   │   ├── countries.py
│   │   └── users.py
│   ├── db/
│   │   ├── models/                  # SQLAlchemy models
│   │   │   ├── country.py
│   │   │   ├── user.py
│   │   │   └── __init__.py
│   │   ├── database.py
│   │   └── __init__.py
│   ├── routes/                      # HTML Rendering routes
│   │   ├── __init__.py
│   │   ├── auth_routes.py  
│   │   └── country_routes.py
│   ├── schemas/                      # Pydantic schemas
│   │   ├── country.py
│   │   ├── user.py
│   │   └── __init__.py
│   ├── static/
│   ├── templates/                    # HTML templates
│   │   ├── base.html
│   │   ├── countries.html
│   │   ├── country_detail.html
│   │   ├── country_edit.html
│   │   ├── country_new.html
│   │   ├── login.html
│   │   ├── signup.py
│   └── main.py                      # App entry point
├── scripts/                         # One-time scripts (e.g. fetch_and_store)
│   ├── fetch_and_store.py
│   └── __init__.py
├── LICENSE               # requirements
├── .gitignore
├── requirements.txt                 # requirements
├── .env                           # Secrets
└── README.md
```



🙋 Author
[S.M Tasmimul HUda]
