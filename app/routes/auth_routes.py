from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud import users
from app.core.security import verify_password

auth_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# signup
@auth_router.get("/signup")
def register_get(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@auth_router.post("/signup")
def register_post(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = users.get_user_by_username(db, username)
    if user:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "User already exists"})
    users.create_user(db, username, email, password)
    return RedirectResponse(url="/login", status_code=303)

# Login
@auth_router.get("/login")
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@auth_router.post("/login")
def login_post(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = users.get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    request.session["user"] = user.username
    return RedirectResponse(url="/", status_code=303)

# Logout
@auth_router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")
