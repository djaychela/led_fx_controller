from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, api_calls
from .. dependencies import get_db
from .. crud import state


router = APIRouter(prefix="/state",)

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

@router.get("/change_colour")
def change_colour(db: Session = Depends(get_db)):
    current_state = state.get_state(db)
    api_calls.new_random_colour(db)
    current_state = state.get_state(db)
    return current_state
