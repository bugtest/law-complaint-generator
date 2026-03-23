from .auth import router as auth_router
from .cases import router as cases_router
from .documents import router as documents_router
from .templates import router as templates_router
from .generate import router as generate_router

__all__ = [
    "auth_router", "cases_router", "documents_router",
    "templates_router", "generate_router"
]
