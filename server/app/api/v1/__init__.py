from fastapi import APIRouter
from app.api.v1 import health
from app.api.v1 import kundli
from app.api.v1 import location
from app.api.v1 import planetary

router = APIRouter(prefix="/api/v1")
router.include_router(health.router)
router.include_router(kundli.router)
router.include_router(location.router)
router.include_router(planetary.router)
