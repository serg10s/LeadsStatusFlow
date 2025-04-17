from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()


app.mount("/assets", StaticFiles(directory='assets'), name='assets')

templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')
