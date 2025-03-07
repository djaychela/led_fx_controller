
from random import randint

from rich.console import Console

from .crud import state, effects

from .helpers import colour_helpers, api_helpers

from .config import *

from .common import output_to_console

if CONSOLE_OUTPUT:
    console = Console()
else:
    console = None

def new_random_effect(db):
    output_to_console("rule", f"[bold green]:light_bulb: New Random Effect :light_bulb:[/]\n", console)
    num_votes = 6
    random_effect = effects.get_random_effect(db, num_votes)
    state.update_effect_id(db, random_effect.id)
    output_to_console("print", f"Effect Chosen: {random_effect.type}", console)

    colourscheme = new_random_colourscheme(db)
    
    api_request_1 = api_helpers.create_api_request_string(db, random_effect.type, colourscheme, random_effect.id)
    api_helpers.perform_api_call(db, api_request_1)

    return api_request_1


def new_random_colour(db):
    output_to_console("rule", f"[bold green]:light_bulb: New Random Colour :light_bulb:[/]\n", console)
    current_state = state.get_state(db)
    colour_mode = current_state.ledfx_colour_mode
    max_colours = current_state.ledfx_max_colours
    colours = [colour_helpers.generate_random_hex_colour() for _ in range(max_colours)]    
    colourscheme = colour_helpers.refine_colourscheme(db, colours, colour_mode, "song")
    state.update_state_colours(db, colourscheme)
    
    api_request_1 = api_helpers.create_api_request_string(db, current_state.ledfx_type, colourscheme)
    api_helpers.perform_api_call(db, api_request_1)
    return api_request_1

def new_random_colourscheme(db):
    output_to_console("rule", f"[bold green]:light_bulb: New Random Colour :light_bulb:[/]\n", console)
    current_state = state.get_state(db)
    colour_mode = current_state.ledfx_colour_mode
    max_colours = current_state.ledfx_max_colours
    max_colours = randint(1, max_colours) # Provide variety!
    colours = [colour_helpers.generate_random_hex_colour() for _ in range(max_colours)]    
    colourscheme = colour_helpers.refine_colourscheme(db, colours, colour_mode, "song")
    state.update_state_colours(db, colourscheme)

    return colourscheme
