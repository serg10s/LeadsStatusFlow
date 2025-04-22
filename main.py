import requests
from fastapi import FastAPI, Request, Depends, Form, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from fastapi.responses import ORJSONResponse
# from db.models import LeadsForm
from db.base import LeadData
from db.database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

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

API_KEY = "ba67df6a-a17c-476f-8e95-bcdb75ed3958"  # Exemple


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/', response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')


@app.get('/statuses', response_class=HTMLResponse)
async def leads_statuses(request: Request, db: Session = Depends(get_db), sort: str = "desc"):
    sort_order = asc(LeadData.create_at) if sort == 'asc' else desc(LeadData.create_at)
    leads = db.query(LeadData).order_by(sort_order).all()

    count_leads = db.query(LeadData).count()
    ftd_count = db.query(LeadData).filter(LeadData.ftd == 1).count()
    print(ftd_count)
    # print('LEADS: ', leads)
    return templates.TemplateResponse(request=request, name='statuses.html', context={'leads': leads,
                                                                                      'sort': sort,
                                                                                      'ftd': ftd_count,
                                                                                      'count_leads': count_leads})


def get_statuses_from_api():
    url = "https://brokercrm.com/api/getstatuses"  # Exemple url
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # {"email": "asdf@gmail.com", "status": "callback"}
    else:
        raise Exception('Error statuses')


def save_statuses_to_db(db: Session, email: str, statuses: list[str]):
    for status in statuses:
        exist = db.query(LeadData).filter_by(email=email, statuses=status).first()
        if not exist:
            db.add(LeadData(email=email, statuses=status))
        db.commit()


def update_lead_statuses(db: Session):
    # json.loads(get_statuses_from_api())
    get_statuses_api = {"email": "asdf@gmail.com", "status": ["callback"]}
    email = get_statuses_api["email"]
    statuses = get_statuses_api["status"]
    save_statuses_to_db(db, email, statuses)


@app.get("/update-statuses")
async def update_statuses(db: Session = Depends(get_db)):
    update_lead_statuses(db)
    return {"message": "Статусы обновлены!"}


@app.post('/send', response_class=HTMLResponse)
async def send_leads_info(request: Request,
                          first_name: str = Form(...),
                          last_name: str = Form(...),
                          email: str = Form(...),
                          phone: str = Form(...),
                          db: Session = Depends(get_db),
                          ):

    client_ip = request.client.host  # get ip
    landing_url = str(request.url)
    token = request.cookies["api_key"]
    if token != API_KEY:
        raise HTTPException(status_code=403, detail="Неверный API ключ")
    # print(landing_url)
    # print(dir(request))
    # print(request)
    leads = LeadData(first_name=first_name, last_name=last_name, email=email,
                     phone=phone, ip=client_ip, landing_url=landing_url)
    db.add(leads)
    db.commit()
    db.refresh(leads)
    return templates.TemplateResponse(request=request, name='success.html', context={'name': first_name})
