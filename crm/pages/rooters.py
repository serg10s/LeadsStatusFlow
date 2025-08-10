from fastapi import APIRouter
from pages.leads import leads_router
from pages.admins import admins_router
from pages.access import access_router

root_router = APIRouter()
root_router.include_router(leads_router)
root_router.include_router(admins_router)
root_router.include_router(access_router)
