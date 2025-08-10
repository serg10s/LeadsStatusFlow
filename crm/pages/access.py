from fastapi import  APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError, jwt
import json

from core.templates import templates
from core.authx import security, config
from db.base import AdminsModel
from db.database import get_session
from db.schemas import CreateAdmin
from services.utils import get_password_hash, create_verification_token, get_redis
from services.verify_email import send_verification_email
from services.tg_message import push_telegram_admin
from config import settings, VERIFICATION_TOKEN_EXPIRE_HOURS, ALGORITHM

access_router = APIRouter()

@access_router.get('/', response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(request=request, name='auth.html')


@access_router.post('/auth')
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

    
@access_router.post('/register')
async def register(
    first_name: str = Form(...), last_name: str = Form(...),
    email: str = Form(...), password: str = Form(...),
    session: AsyncSession = Depends(get_session)):

    admins_select = await session.execute(select(AdminsModel).where(AdminsModel.email == email)) 
    desired_admin = admins_select.scalar_one_or_none()
    if desired_admin:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем или email уже существует.")

    user_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": get_password_hash(password)
    }
    
    verification_token = create_verification_token({"sub": email})
    
    redis_backend = get_redis()  # save data to redis
    user_data_json = json.dumps(user_data)
    await redis_backend.set(f"pending_user:{email}", user_data_json, expire=VERIFICATION_TOKEN_EXPIRE_HOURS*3600)
    
    verification_url = f"{settings.BASE_URL}/verify-email?token={verification_token}"  # send email
    print("CHECK URL", verification_url)
    await send_verification_email(email, f"http://{verification_url}") # on prod https
    
    return {"message": "Письмо с подтверждением отправлено на ваш email"}

@access_router.get("/verify-email")
async def verify_email(token: str, session: AsyncSession = Depends(get_session)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=400, detail="Неверный токен")
    except JWTError:
        raise HTTPException(status_code=400, detail="Неверный или просроченный токен")
    
    redis_backend = get_redis()  # get data 
    user_data = await redis_backend.get(f"pending_user:{email}")

    if not user_data:
        raise HTTPException(status_code=404, detail="Данные пользователя не найдены или срок действия ссылки истёк")
    
    admins_schema = CreateAdmin(**json.loads(user_data.decode())) # to schema

    if not admins_schema:
        raise HTTPException(status_code=400, detail="Поля превысили лимит по длине")

    await push_telegram_admin(json.loads(user_data.decode()))  # sending to telegram

    db_admins = AdminsModel(**admins_schema.dict()) # save admin to db
    session.add(db_admins)
    await session.commit()
    await session.refresh(db_admins)

    await redis_backend.clear(f"pending_user:{email}") # clear data from redis 
    
    return {"message": "Email успешно подтверждён, аккаунт создан"}
    