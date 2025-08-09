from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from core.templates import templates
from core.authx import security

admins_router = APIRouter(dependencies=[Depends(security.access_token_required)])


@admins_router.get("/admins", response_class=HTMLResponse)
async def admins(request: Request):
    return templates.TemplateResponse(request=request, name='admins.html')
