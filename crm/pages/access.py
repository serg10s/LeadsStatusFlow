from fastapi import  APIRouter, Request, Response, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from core.templates import templates
from core.authx import security, config


access_router = APIRouter()

@access_router.get('/', response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(request=request, name='auth.html')


@access_router.post('/submit')
async def submit(email: str = Form(...), password: str = Form(...)):
    if email == "test@gmail.com" and password == "test":
        token = security.create_access_token(uid=email)
        redirect = RedirectResponse(url="/statuses", status_code=303)  # replace “post” to “get”
        redirect.set_cookie(
                key=config.JWT_ACCESS_COOKIE_NAME,
                value=token,
                httponly=True,
                max_age=60, # seconds
                secure=False)  # Для разработки без HTTPS
        return redirect
    raise HTTPException(401, detail={"message": "Bad credentials"})


@access_router.get('/sing-up', response_class=HTMLResponse)
async def sing_up(request: Request):
    return templates.TemplateResponse(request=request, name='reg.html')
