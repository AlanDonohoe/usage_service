from fastapi import APIRouter

router = APIRouter(prefix="/v1")


@router.get("/usage")
def read_usage() -> None:
    """Get usage information."""
