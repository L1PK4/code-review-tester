from fastapi import APIRouter

from app.endpoints import login, users, tel_verification_code, email_verification_code

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(email_verification_code.router)
api_router.include_router(tel_verification_code.router)
