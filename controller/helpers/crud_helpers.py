from sqlalchemy.orm import Session

from .. import schemas

def return_effect_preset_json(effect: schemas.EffectPreset):
    """ Takes an EffectPreset and returns the json call for it"""
    return effect.config["effect"]
