from soco import SoCo

from ..config import SONOS_SPEAKER

from .state import get_state, update_track_info

from ..dependencies import get_db

from ..api_calls import select_random_effect_preset


def connect_to_sonos():
    sonos = SoCo(SONOS_SPEAKER)
    return sonos


def get_sonos_state():
    generator = get_db()
    db = next(generator)
    sonos = connect_to_sonos()
    track_info = sonos.get_current_track_info()
    current_state = get_state(db)
    if current_state.current_song_title != track_info["title"]:
        update_track_info(
            db, track_artist=track_info["artist"], track_title=track_info["title"]
        )
        select_random_effect_preset(db)
        return track_info
    return None
