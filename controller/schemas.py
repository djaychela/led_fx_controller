from pydantic import BaseModel, Json
from typing import Optional


class GradientBase(BaseModel):
    gradient: str

    class Config:
        from_attributes = True


class Gradient(GradientBase):
    gradient: str


class GradientCreate(GradientBase):
    gradient: str


class EffectBase(BaseModel):
    name: str
    type: str
    colour_mode: str
    max_colours: int

    class Config:
        from_attributes = True


class EffectPresetBase(BaseModel):
    name: str
    type: str
    config: Optional[dict]

    class Config:
        from_attributes = True


class EffectPresetCreate(EffectPresetBase):
    name: str
    type: str
    config: Json

    class Config:
        from_attributes = True


class EffectPreset(EffectPresetBase):
    class Config:
        from_attributes = True


class EffectPresetSelect(BaseModel):
    name: str
    type: str

    class Config:
        from_attributes = True


class StateBase(BaseModel):
    ledfx_name: str
    ledfx_type: str
    ledfx_config: Optional[dict]
    ledfx_colour_mode: str
    ledfx_max_colours: int
    effect_id: int
    colours: Optional[str]
    sonos_active: bool

    class Config:
        from_attributes = True


class StateLedFxUpdate(BaseModel):

    ledfx_name: str
    ledfx_type: str
    ledfx_config: Optional[dict]

    class Config:
        from_attributes = True


class StateLedFxUpdateColours(BaseModel):

    ledfx_colour_mode: str
    ledfx_max_colours: str

    class Config:
        from_attributes = True


class StateSetSong(BaseModel):
    current_song_id: str
    current_song_title: str
    current_song_artist: str
