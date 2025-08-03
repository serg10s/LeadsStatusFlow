from fastapi import FastAPI, Request, Depends, Form, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from db.base import LeadData
from db.database import SessionLocal, engine, Base, get_db
from db.schemas import CreateLead
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
# import requests

from get_status import *

# Base.metadata.create_all(bind=engine)  # create db
app = FastAPI()


app.mount("/assets", StaticFiles(directory='assets'), name='assets')

templates = Jinja2Templates(directory='templates')


def split_string(value, delimiter=" "):
    return str(value).split(delimiter)


def replace_string(value, delimiter="-"):
    return str(value).replace(delimiter, ".")


templates.env.filters["split"] = split_string
templates.env.filters["replace"] = replace_string

API_KEY = "ba67df6a-a17c-476f-8e95-bcdb75ed3958"


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")


@app.get('/', response_class=HTMLResponse)
async def leads_statuses(request: Request, db: Session = Depends(get_db), sort: str = "desc"):
    sort_order = asc(LeadData.create_at) if sort == 'asc' else desc(LeadData.create_at)
    leads = db.query(LeadData).order_by(sort_order).all()

    count_leads = db.query(LeadData).count()
    ftd_count = db.query(LeadData).filter(LeadData.ftd == 1).count()
    return templates.TemplateResponse(request=request, name='statuses.html', context={'leads': leads,
                                                                                      'sort': sort,
                                                                                      'ftd': ftd_count,
                                                                                      'count_leads': count_leads})


@app.get("/update-statuses")
async def update_statuses(db: Session = Depends(get_db)):
    update_lead_statuses(db)
    return {"message": "Статусы обновлены!"}


@app.post('/leads/')
async def create_lead(lead: CreateLead,
                      db: Session = Depends(get_db),
                     _: None = Depends(verify_api_key)):  
    db_lead = LeadData(**lead.dict())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return {'message': 'Успшно добавлено!'}
