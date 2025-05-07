from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.country import Country
from app.schemas.country import CountryCreate, CountryUpdate
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi import Request, Form, status
from app.core.security import get_current_user_session

from fastapi import FastAPI, Request
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.routes import auth_router, country_router
from app.api.countries import router
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import Response
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


app = FastAPI()
app.include_router(router, prefix="/countries_api", tags=["countries"])

