from fastapi import APIRouter

from .ignored_messages import ignored_messages_router


v1_router = APIRouter()

v1_router.include_router(ignored_messages_router, prefix="/ignored_messages")