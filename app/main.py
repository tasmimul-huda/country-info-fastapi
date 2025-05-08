
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.routes import auth_router, country_router
from app.api.countries import router
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import Response


app = FastAPI()

class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response: Response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    
app.add_middleware(NoCacheMiddleware)
app.add_middleware(SessionMiddleware, secret_key="supersecret")
app.include_router(router, prefix="/countries_api", tags=["countries"])
app.include_router(auth_router, tags=["Web Interface"])
app.include_router(country_router, tags=["Web Interface"])

