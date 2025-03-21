from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from .. import models, schemas

from . import state

from ..config import *


def create_effect(db: Session, effect: schemas.EffectPresetCreate):
    db_effect = models.EffectPreset(**effect.dict())
    db.add(db_effect)
    db.commit()
    db.refresh(db_effect)
    return db_effect


def check_effect_duplicate(db: Session, effect: schemas.EffectPreset):
    """Takes an effect and checks if config already in database.  Returns True if match found."""
    matching = (
        db.query(models.EffectPreset)
        .filter(models.EffectPreset.config == effect.config)
        .all()
    )
    if matching:
        return True
    return False


def store_effect_preset(db: Session, ledfx_current_config: schemas.EffectPresetCreate):
    db_effect = models.EffectPreset()
    db_effect.config = ledfx_current_config
    db_effect.name = ledfx_current_config["effect"]["name"]
    db_effect.type = ledfx_current_config["effect"]["type"]
    db_effect.max_colours = 6
    db_effect.colour_mode = "gradient"
    duplicated = check_effect_duplicate(db, db_effect)
    if duplicated:
        db_effect.config = "Already Stored"
    else:
        db.add(db_effect)
        db.commit()
        db.refresh(db_effect)
    return db_effect


def get_effect_presets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.EffectPreset).offset(skip).limit(limit).all()


def get_effect_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Effect).offset(skip).limit(limit).all()


def get_effect_preset_by_id(db: Session, effect_id: int):
    return (
        db.query(models.EffectPreset)
        .filter(models.EffectPreset.id == effect_id)
        .first()
    )

def delete_effect_preset_by_id(db: Session, effect_id: int):
    to_delete = db.query(models.EffectPreset).filter(models.EffectPreset.id == effect_id).delete()
    if to_delete:
        db.commit()
        return True
    return False


def get_random_effect(db: Session, max_colours):
    current_state = state.get_state(db)
    current_effect_id = current_state.effect_id
    random_effect = (
        db.query(models.Effect)
        .filter(models.Effect.max_colours >= max_colours)
        .filter(models.Effect.id != current_effect_id)
        .order_by(func.random())
        .first()
    )
    while random_effect.type in NEVER_CHOOSE_EFFECTS_TYPE:
        random_effect = (
            db.query(models.Effect)
            .filter(models.Effect.max_colours >= max_colours)
            .filter(models.Effect.id != current_effect_id)
            .order_by(func.random())
            .first()
        )
    return random_effect


def get_random_effect_preset(db: Session):
    return db.query(models.EffectPreset).order_by(func.random()).first()


def get_effect_preset_by_song_id(db: Session, song_id: str):
    return (
        db.query(models.EffectPreset)
        .filter(models.EffectPreset.song_id == song_id)
        .first()
    )


def get_effect_string_by_id(db: Session, effect_id: str):
    effect = db.query(models.Effect).filter(models.Effect.id == effect_id).first()
    return effect.config


def find_effect_match(db: Session, type: str, colour_mode: str, max_colours: int):
    effect = (
        db.query(models.Effect)
        .filter(models.Effect.type == type)
        .filter(models.Effect.colour_mode == colour_mode)
        .filter(models.Effect.max_colours == max_colours)
        .first()
    )
    if not effect:
        effect = (
            db.query(models.Effect)
            .filter(models.Effect.type == type)
            .filter(models.Effect.colour_mode == colour_mode)
            .first()
        )
    if not effect:
        effect = db.query(models.Effect).filter(models.Effect.type == type).first()
    if effect:
        return effect
    else:
        return None
