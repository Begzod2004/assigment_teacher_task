from .users import router as users_router
from .products import router as products_router
from .categories import router as categories_router
from .auth_router import router as auth_router
from .admin_routes import router as admin_router
from .customer_routes import router as customer_router

__all__ = [
    "users_router",
    "products_router",
    "categories_router",
    "auth_router",
    "admin_router",
    "customer_router"
] 