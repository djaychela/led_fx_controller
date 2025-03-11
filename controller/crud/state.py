from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

import json

from .. import models, schemas


def get_state(db: Session):
    return db.query(models.State).filter(models.State.id == 1).first()

def update_state_ledfx(db: Session, effect: schemas.EffectPreset):
    """ Takes a db session and an Effect and updates the current ledfx state to reflect the present Effect"""
    current_state = get_state(db)
    current_state.ledfx_name = effect.name
    current_state.ledfx_type = effect.type
    current_state.ledfx_config = effect.config
    db.commit()

def update_state_colours(db: Session, colours):
    """ Takes a list of colours, and stores it in the database as json"""
    current_state = get_state(db)
    current_state.colours = json.dumps(colours)
    db.commit()   

def update_effect_id(db: Session, effect_id: int):
    """ Takes an effect id and updates the current state.  Returns the state"""
    current_state = get_state(db)
    current_state.effect_id = effect_id
    db.commit()
    return current_state

