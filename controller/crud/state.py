from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

import json

from .. import models, schemas


def get_state(db: Session):
    return db.query(models.State).filter(models.State.id == 1).first()

def create_ledfx_state_preset(ledfx_state):
    """ Takes a dictionary of ledfx state, and returns an EffectsPreset of that data"""
    led_fx_state_preset = models.EffectPreset()
    led_fx_state_preset.name = ledfx_state['effect']['name']
    led_fx_state_preset.type = ledfx_state['effect']['type']
    led_fx_state_preset.config = ledfx_state["effect"]
    return led_fx_state_preset

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

# def return_effect_preset_json(db: Session, effect: schemas.EffectPreset):
#     """ Takes an EffectPreset and returns the json call for it"""
#     return effect.config["effect"]
