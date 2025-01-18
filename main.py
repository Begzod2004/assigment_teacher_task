from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from app.routers import (
    users_router, 
    products_router, 
    categories_router, 
    auth_router, 
    admin_router, 
    customer_router
)
from app.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(products_router)
app.include_router(categories_router)
app.include_router(admin_router)
app.include_router(customer_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Application"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My Assigment task",
        version="1.0.0",
        description="This is a custom OpenAPI schema with authentication.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi