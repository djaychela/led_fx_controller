from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from pathlib import Path

from ..crud import effects

from .. import schemas
from ..database import SessionLocal, engine
from ..dependencies import get_db

from ..helpers import api_helpers

from ..config import API_ENDPOINT
from ..models import EffectPreset

router = APIRouter(prefix="/effects")

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))


@router.post("/", response_model=schemas.EffectPreset)
def create_effect(effect: schemas.EffectPreset, db: Session = Depends(get_db)):
    effect_created = effects.create_effect(db=db, effect=effect)
    return effect_created


@router.get("/store_preset", response_class=HTMLResponse)
def store_effect_preset(request: Request, db: Session = Depends(get_db)):
    ledfx_current_config = api_helpers.get_api_response(API_ENDPOINT)
    effect_created = effects.store_effect_preset(
        db=db, ledfx_current_config=ledfx_current_config
    )
    return templates.TemplateResponse(
        "updated.html", {"request": request, "type": "Preset Stored", "data": effect_created.config}
    )


@router.get("/", response_model=list[schemas.EffectPreset])
def read_effects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    effects_list = effects.get_effect_presets(db, skip=skip, limit=limit)
    return effects_list


@router.get("/view/{effect_id}", response_model=schemas.EffectPreset)
def read_effect(effect_id: int, db: Session = Depends(get_db)):
    db_effect = effects.get_effect_preset_by_id(db, effect_id=effect_id)
    if db_effect is None:
        raise HTTPException(status_code=404, detail="Effect Not Found!")
    return db_effect


@router.get("/types/")
def read_effect_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    effect_types = effects.get_effect_types(db, skip=skip, limit=limit)
    return effect_types
