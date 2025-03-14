from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from json import dumps
from pathlib import Path

from ..crud import state
from ..dependencies import get_db
from .. import api_calls

router = APIRouter(prefix="")

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    current_state = state.get_state(db)
    led_fx_config = current_state.ledfx_config
    led_fx_json = dumps(led_fx_config)
    return templates.TemplateResponse("home.html", {"request": request, "current_state": led_fx_json})


@router.get("/multi_gradient", response_class=HTMLResponse)
async def change_colour(request: Request, db: Session = Depends(get_db), colours:int=6):
    api_response = api_calls.new_random_colour_gradient(db, colours)
    colour = api_response["config"]["gradient"]
    return templates.TemplateResponse(
        "updated.html", {"request": request, "type": "Colour", "data": colour}
    )

@router.get("/single_colour", response_class=HTMLResponse)
async def change_colour(request: Request, db: Session = Depends(get_db)):
    api_response = api_calls.new_random_single_colour(db)
    colour = api_response["config"]["gradient"]
    return templates.TemplateResponse(
        "updated.html", {"request": request, "type": "1 Colour", "data": colour}
    )

@router.get("/single_gradient", response_class=HTMLResponse)
async def change_colour(request: Request, db: Session = Depends(get_db)):
    api_response = api_calls.new_random_single_colour(db, mode="gradient")
    colour = api_response["config"]["gradient"]
    return templates.TemplateResponse(
        "updated.html", {"request": request, "type": "1 Gradient", "data": colour}
    )

@router.get("/change_effect", response_class=HTMLResponse)
async def change_effect(request: Request, db: Session = Depends(get_db)):
    api_response = api_calls.new_random_effect(db)
    data = api_response["name"]
    return templates.TemplateResponse(
        "updated.html", {"request": request, "type": "Effect", "data": data}
    )

@router.get("/random_preset", response_class=HTMLResponse)
async def random_preset(request: Request, db: Session = Depends(get_db)):
    api_response = api_calls.select_random_effect_preset(db)
    data = api_response["name"]
    return templates.TemplateResponse(
        "updated.html", {"request": request, "type": "Random Preset", "data": data}
    )

