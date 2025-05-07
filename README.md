# Country Data API Project

This project fetches country data from the REST Countries API and stores it in a database, along with user management capabilities.

## Prerequisites

- Python 3.9 or higher
- pip
- virtualenv (recommended)

## Setup Instructions

### 1. Create and activate a virtual environment

```bash
# Install specific Python version (if needed)
# For Ubuntu/Debian:
sudo apt update
sudo apt install python3.9 python3.9-venv

# Create virtual environment with Python 3.9
python3.9 -m venv venv

# Activate the virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
.\venv\Scripts\activate

```

## Project Structure
codefusion_ai/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── countries.py
│   │   │   │   └── auth.py
│   │   │   └── __init__.py  # for API versioning
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py  # auth dependencies
│   │   └── __init__.py
│   ├── crud/
│   │   ├── countries.py
│   │   └── users.py
│   ├── db/
│   │   ├── models/
│   │   │   ├── country.py
│   │   │   ├── user.py
│   │   │   └── __init__.py
│   │   ├── database.py
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── country.py
│   │   ├── user.py
│   │   └── __init__.py
│   ├── services/
│   │   └── country_service.py
│   ├── static/
│   ├── templates/
│   ├── tests/
│   │   ├── api/
│   │   ├── crud/
│   │   └── __init__.py
│   └── main.py
├── scripts/
│   ├── fetch_and_store.py
│   └── __init__.py
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── .env
└── README.md