from random import randint

from rich.console import Console

from .crud import state, effects

from .helpers import colour_helpers, api_helpers, crud_helpers

from .config import *

from .common import output_to_console

if CONSOLE_OUTPUT:
    console = Console()
else:
    console = None


def get_current_ledfx_state():
    current_ledfx_state = api_helpers.get_api_response(API_ENDPOINT)
    return current_ledfx_state


def select_random_effect_preset(db):
    output_to_console(
        "rule", f"[bold green]:light_bulb: New Random Preset :light_bulb:[/]\n", console
    )
    random_effect_preset = effects.get_random_effect_preset(db)
    state.update_effect_id(db, random_effect_preset.id)
    state.update_state_ledfx(db, random_effect_preset)

    output_to_console(
        "print", f"Effect Preset Chosen: {random_effect_preset.type}", console
    )

    effect_preset_json = crud_helpers.return_effect_preset_json(random_effect_preset)
    api_helpers.perform_api_call(db, effect_preset_json)

    return effect_preset_json


def new_random_effect(db):
    output_to_console(
        "rule", f"[bold green]:light_bulb: New Random Effect :light_bulb:[/]\n", console
    )
    num_votes = 6
    random_effect = effects.get_random_effect(db, num_votes)
    state.update_effect_id(db, random_effect.id)
    output_to_console("print", f"Effect Chosen: {random_effect.type}", console)

    colourscheme = new_random_colourscheme(db)

    output_to_console("rule", f"[bright_red]:light_bulb: {colourscheme=}[/]\n", console)

    api_request_1 = api_helpers.create_api_effect_request_string(
        db, random_effect.id, colourscheme
    )

    api_helpers.perform_api_call(db, api_request_1)

    return api_request_1


def new_random_colour_gradient(db, max_colours=6):
    output_to_console(
        "rule", f"[bold green]:light_bulb: New Random Colour :light_bulb:[/]\n", console
    )
    current_state = state.get_state(db)
    led_fx_state = get_current_ledfx_state()
    if led_fx_state == {}:
        return led_fx_state
    led_fx_state_preset = state.create_ledfx_state_preset(led_fx_state)
    state.update_state_ledfx(db, led_fx_state_preset)
    colour_mode = current_state.ledfx_colour_mode
    # max_colours = current_state.ledfx_max_colours
    colours = [colour_helpers.generate_random_hex_colour() for _ in range(max_colours)]
    colourscheme = colour_helpers.refine_colourscheme(db, colours, colour_mode)
    state.update_state_colours(db, colourscheme)
    gradient = colour_helpers.create_gradient(colourscheme, mode="single")

    api_request_1 = api_helpers.create_api_request_string(
        db, current_state.ledfx_type, gradient
    )
    api_helpers.perform_api_call(db, api_request_1)
    return api_request_1


def new_random_single_colour(db, mode="single"):
    output_to_console(
        "rule",
        f"[bold green]:light_bulb: New Random Single Colour :light_bulb:[/]\n",
        console,
    )
    current_state = state.get_state(db)
    led_fx_state = get_current_ledfx_state()
    if led_fx_state == {}:
        return led_fx_state
    led_fx_state_preset = state.create_ledfx_state_preset(led_fx_state)
    state.update_state_ledfx(db, led_fx_state_preset)
    colour_mode = current_state.ledfx_colour_mode
    colours = [colour_helpers.generate_random_hex_colour()]
    print(f"{colours=}")
    colourscheme = colour_helpers.refine_colourscheme(db, colours, colour_mode)
    state.update_state_colours(db, colourscheme)
    gradient = colour_helpers.create_gradient(colourscheme, mode=mode)

    api_request_1 = api_helpers.create_api_request_string(
        db, current_state.ledfx_type, gradient
    )
    api_helpers.perform_api_call(db, api_request_1)
    return api_request_1


def new_random_colourscheme(db):
    output_to_console(
        "rule",
        f"[bold green]:light_bulb: New Random Colourscheme :light_bulb:[/]\n",
        console,
    )
    current_state = state.get_state(db)
    colour_mode = current_state.ledfx_colour_mode
    max_colours = randint(1, current_state.ledfx_max_colours)
    colours = [colour_helpers.generate_random_hex_colour() for _ in range(max_colours)]
    colourscheme = colour_helpers.refine_colourscheme(db, colours, colour_mode)

    return colourscheme
