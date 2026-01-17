from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    """
    Lightweight health check endpoint.
    Must be fast, dependency-free, and always available.
    """
    return {
        "status": "ok",
        "service": "kundli-service"
    }
