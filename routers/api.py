from fastapi import APIRouter
from routers.v1 import tts_router
from routers.v1 import user_router
from routers.v1 import auth_router
router = APIRouter()
router.include_router(tts_router.router)
router.include_router(user_router.router)
router.include_router(auth_router.router)