from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, api_calls
from ..dependencies import get_db
from ..crud import state


router = APIRouter(
    prefix="/state",
)


@router.get("/", response_model=schemas.StateBase)
def read_state(db: Session = Depends(get_db)):
    current_state = state.get_state(db)
    return current_state


@router.get("/change_effect")
def change_effect(db: Session = Depends(get_db)):
    current_state = state.get_state(db)
    api_calls.new_random_effect(db)
    current_state = state.get_state(db)
    return current_state

@router.get("/random_preset")
def random_preset(db: Session = Depends(get_db)):
    current_state = state.get_state(db)
    random_preset = api_calls.select_random_effect_preset(db)
    current_state = state.get_state(db)
    return random_preset


@router.get("/change_colour")
def change_colour(db: Session = Depends(get_db)):
    current_state = state.get_state(db)
    api_calls.new_random_colour(db)
    current_state = state.get_state(db)
    return current_state


@router.get("/get_ledfx_state")
def get_ledfx_state(db: Session = Depends(get_db)):
    led_fx_state = api_calls.get_current_ledfx_state()
    led_fx_state_preset = state.create_ledfx_state_preset(led_fx_state)
    state.update_state_ledfx(db, led_fx_state_preset)
    return led_fx_state
