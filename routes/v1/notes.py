from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix='/v1/notes', tags=["Notes"])
templates = Jinja2Templates(directory="static/templates/v1/")  # remove leading slash for relative path


@router.get("/update", response_class=HTMLResponse)
def render_template(request: Request):
    return templates.TemplateResponse("notes.html", {"request": request})