from fastapi import APIRouter
from app.api.v1 import blog, surveys, users, comparisons

api_router = APIRouter()

# Incluir routers
api_router.include_router(blog.router)
api_router.include_router(surveys.router, prefix="/surveys", tags=["Surveys"])
api_router.include_router(users.router)
api_router.include_router(comparisons.router)
