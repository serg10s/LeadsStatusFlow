from fastapi import  APIRouter, Request, Depends, HTTPException, Header
from fastapi.responses import HTMLResponse
from db.base import LeadModel
from db.database import get_session
from db.schemas import CreateLead
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from config import API_KEY 
from services.get_status import *
from core.templates import templates
from core.authx import security

leads_router = APIRouter(dependencies=[Depends(security.access_token_required)])

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")


@leads_router.get('/statuses', response_class=HTMLResponse)
async def leads_statuses(request: Request, session: AsyncSession = Depends(get_session)):
    leads_select = await session.execute(select(LeadModel))
    leads = leads_select.scalars().all()
    return templates.TemplateResponse(request=request, name='statuses.html', context={'leads': leads}
                                                                                    #   'ftd': ftd_count,
                                                                                    #   'count_leads': count_leads}
                                      )


@leads_router.get("/update-statuses")
async def update_statuses(session: AsyncSession = Depends(get_session)):
    await update_lead_statuses(session)
    return {"message": "Статусы обновлены!"}


@leads_router.post('/leads')
async def create_lead(lead: CreateLead,
                      session: AsyncSession = Depends(get_session),
                      _: None = Depends(verify_api_key)):  
    db_lead = LeadModel(**lead.dict())
    session.add(db_lead)
    await session.commit()
    await session.refresh(db_lead)
    return {'message': 'Успшно добавлено!'}
