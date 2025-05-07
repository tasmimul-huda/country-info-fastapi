# app/core/security.py
from passlib.context import CryptContext
from fastapi import Request, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


from fastapi import Request, HTTPException, status, Depends

def get_current_user_session(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="Not authenticated",
            headers={"Location": "/login"}
        )
    return user