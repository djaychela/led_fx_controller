from soco import SoCo
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from ..config import SONOS_SPEAKER_ADDRESS

from .state import get_state, update_track_info

from ..dependencies import get_db

from ..api_calls import select_random_effect_preset


def connect_to_sonos():
    sonos = SoCo(SONOS_SPEAKER_ADDRESS)
    return sonos


def get_sonos_db_state():
    generator = get_db()
    db = next(generator)
    current_state = get_state(db)
    return current_state.sonos_active


def get_sonos_state():
    if get_sonos_db_state():
        generator = get_db()
        db = next(generator)
        sonos = connect_to_sonos()
        track_info = sonos.get_current_track_info()
        current_state = get_state(db)
        if current_state.current_song_title != track_info["title"]:
            update_track_info(
                db,
                track_artist=track_info["artist"],
                track_title=track_info["title"],
                track_album=track_info["album"],
                track_album_art=track_info["album_art"]
            )
            select_random_effect_preset(db)
            return track_info
        return None
    return None


def store_sonos_state(db: Session, sonos_new_state: bool):
    current_state = get_state(db)
    current_state.sonos_active = sonos_new_state
    db.commit()
