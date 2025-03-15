from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from json import dumps
from pathlib import Path

from ..crud import state, effects, sonos
from ..dependencies import get_db
from .. import api_calls
from ..state import get_state


from ..config import SONOS_SPEAKER_ADDRESS

router = APIRouter(prefix="")

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    current_state = state.get_state(db)
    led_fx_config = current_state.ledfx_config
    led_fx_json = dumps(led_fx_config)
    return templates.TemplateResponse(
        "random.html", {"request": request, "current_state": led_fx_json}
    )


@router.get("/multi_gradient", response_class=HTMLResponse)
async def change_colour(
    request: Request, db: Session = Depends(get_db), colours: int = 6
):
    api_response = api_calls.new_random_colour_gradient(db, colours)
    colour = api_response["config"]["gradient"]
    return templates.TemplateResponse(
        "updated_colour.html",
        {"request": request, "type": "Multi Gradient", "data": colour},
    )


@router.get("/single_colour", response_class=HTMLResponse)
async def change_colour(request: Request, db: Session = Depends(get_db)):
    api_response = api_calls.new_random_single_colour(db)
    colour = api_response["config"]["gradient"]
    return templates.TemplateResponse(
        "updated_colour.html",
        {"request": request, "type": "Single Colour", "data": colour},
    )


@router.get("/single_gradient", response_class=HTMLResponse)
async def change_colour(request: Request, db: Session = Depends(get_db)):
    api_response = api_calls.new_random_single_colour(db, mode="gradient")
    colour = api_response["config"]["gradient"]
    return templates.TemplateResponse(
        "updated_colour.html",
        {"request": request, "type": "Single Colour Gradient", "data": colour},
    )


@router.get("/change_effect", response_class=HTMLResponse)
async def change_effect(request: Request, db: Session = Depends(get_db)):
    api_response = api_calls.new_random_effect(db)
    data = api_response["name"]
    data_2 = api_response["config"]["gradient"]
    return templates.TemplateResponse(
        "updated.html",
        {"request": request, "type": "Effect & Colour", "data": data, "data_2": data_2},
    )


@router.get("/random_preset", response_class=HTMLResponse)
async def random_preset(request: Request, db: Session = Depends(get_db)):
    api_response = api_calls.select_random_effect_preset(db)
    data = api_response["name"]
    data_2 = api_response["config"]["gradient"]
    return templates.TemplateResponse(
        "updated.html",
        {"request": request, "type": "Random Preset", "data": data, "data_2": data_2},
    )


@router.get("/presets_list", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    presets_list = effects.get_effect_presets(db)
    presets_list = [
        (
            preset.name,
            preset.config["effect"]["config"],
            preset.config["effect"]["config"]["gradient"],
        )
        for preset in presets_list
    ]
    return templates.TemplateResponse(
        "presets_list.html", {"request": request, "presets_list": presets_list}
    )


@router.post("/load_delete_preset", response_class=HTMLResponse)
async def load_delete_preset(
    request: Request, db: Session = Depends(get_db), action: str = Form(...)
):
    (action, effect_id) = action.split("_")
    effect_id = int(effect_id)
    if action == "load":
        effect_preset = api_calls.select_effect_preset(db, effect_id=effect_id)
        completed_action = "Loaded Preset"
    elif action == "delete":
        deleted = effects.delete_effect_preset_by_id(db, effect_id=effect_id)
        completed_action = "Deleted Preset"

    return templates.TemplateResponse(
        "load_delete_preset.html",
        {
            "request": request,
            "completed_action": completed_action,
            "effect_id": effect_id,
        },
    )


@router.get("/settings", response_class=HTMLResponse)
async def settings(request: Request, db: Session = Depends(get_db)):
    current_state = get_state(db)
    return templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "sonos_active": current_state.sonos_active,
            "sonos_ip": SONOS_SPEAKER_ADDRESS,
            "sonos_mode": current_state.sonos_mode,
        },
    )


@router.post("/settings", response_class=HTMLResponse)
async def store_settings(
    request: Request, db: Session = Depends(get_db), sonos_active: str = Form(""), sonos_mode: str = Form(...)
):
    # print(f"{sonos_mode=}")
    if sonos_active == "true":
        sonos.store_sonos_state(db, True)
    else:
        sonos.store_sonos_state(db, False)
    sonos.store_sonos_mode(db, sonos_new_mode=sonos_mode)
    current_state = get_state(db)
    return templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "sonos_active": current_state.sonos_active,
            "sonos_ip": SONOS_SPEAKER_ADDRESS,
            "sonos_mode": sonos_mode,
        },
    )


@router.get("/sonos", response_class=HTMLResponse)
async def settings(request: Request, db: Session = Depends(get_db)):
    current_state = get_state(db)
    return templates.TemplateResponse(
        "sonos.html",
        {
            "request": request,
            "sonos_title": current_state.current_song_title,
            "sonos_artist": current_state.current_song_artist,
            "sonos_album": current_state.current_song_album,
            "sonos_album_art": current_state.current_song_album_art,
            "sonos_active": current_state.sonos_active,
        },
    )
