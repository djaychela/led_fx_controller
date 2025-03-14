from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Gradient(Base):
    __tablename__ = "gradient_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    gradient = Column(String, index=True)


class Effect(Base):
    __tablename__ = "effect_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String, index=True)
    colour_mode = Column(String, index=True)
    max_colours = Column(Integer)
    config = Column(JSON)


class EffectPreset(Base):
    __tablename__ = "effect_preset_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String, index=True)
    config = Column(JSON)
    colour_mode = Column(String, index=True)
    max_colours = Column(Integer)


class State(Base):
    __tablename__ = "state_table"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    colours = Column(String)
    ledfx_name = Column(String, index=True)
    ledfx_type = Column(String, index=True)
    ledfx_config = Column(JSON)
    ledfx_colour_mode = Column(String, index=True)
    ledfx_max_colours = Column(Integer)
    effect_id = Column(Integer)
    current_song_title = Column(String)
    current_song_artist = Column(String)
