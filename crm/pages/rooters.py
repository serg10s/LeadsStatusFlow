from fastapi import APIRouter
from leads import leads_router
from admins import admins_router
from access import access_router

root_router = APIRouter()
root_router.include_router(leads_router)
root_router.include_router(admins_router)
root_router.include_router(access_router)
