import json
import requests

import copy

from rich.console import Console

from .. crud import state, effects

from .. models import EffectPreset

from . import colour_helpers

from .. config import *

from .. common import output_to_console

if CONSOLE_OUTPUT:
    console = Console()
else:
    console = None

def update_state_from_response(db, response, mode):
    response_dict = response.json()    
    new_effect_preset = EffectPreset()
    new_effect_preset.name = response_dict['effect']['name']
    new_effect_preset.type = response_dict['effect']['type']
    new_effect_preset.config = response_dict["effect"]
    if mode == "sticks":
        state.update_state_ledfx(db, new_effect_preset)
    elif mode == "bands":
        state.update_state_bands(db, new_effect_preset)


def create_api_request_string(db, fx_type, colourscheme, effect_id=None):
    """Looks up a config from the database for the current effect id if provided, and
    substitutes sentinel values for the colourscheme / gradient where appropriate.
    If effect_id is not provided, then hard-coded dictionaries have values replaced in them, and are
    returned instead."""

    gradient = colour_helpers.create_gradient(colourscheme, flash=False)

    if effect_id is not None:
        # output_to_console("print", f"Effect ID: {effect_id}", console)
        # output_to_console("print", f"Colourscheme: {colourscheme}", console)
        effect_config = copy.deepcopy(effects.get_effect_string_by_id(db, effect_id))
        # output_to_console("print", f"{id(effect_config)=}", console)
        # output_to_console("print", f"Effect Config: {effect_config}", console)
        index = list(effect_config['config'].values())
        gradient_indices = [i for i, x in enumerate(index) if x == "#GGGGGG"]
        other_indices = [i for i, x in enumerate(index) if x == "#HHHHHH"]
        # output_to_console("print", f"Gradient Indices: {gradient_indices}", console)
        # output_to_console("print", f"Other Indices:    {other_indices}", console)
        if gradient_indices:
            # output_to_console("print", f"Keys: {[list(effect_config['config'].keys())[g] for g in gradient_indices]}", console)
            for key in [list(effect_config['config'].keys())[g] for g in gradient_indices]:
                # output_to_console("print", f"Replacing {key}", console)
                effect_config['config'][key] = gradient
        if other_indices:
            # output_to_console("print", f"Keys: {[list(effect_config['config'].keys())[o] for o in other_indices]}", console)
            for idx, key in enumerate([list(effect_config['config'].keys())[o] for o in other_indices]):
                # output_to_console("print", f"Replacing {key}", console)
                try:
                    effect_config['config'][key] = colourscheme[idx]
                except IndexError:
                    effect_config['config'][key] = colourscheme[0]

        return effect_config

    data = {
        "active": True,
        "type": str(fx_type),
        "config": {
            "blur": 0.0,
            "gradient": gradient,
            "band_count" : 10,
            "gradient_repeat": 10,
        }
    }
    return data

def perform_api_call(db, data):
    
    endpoint = STICKS_API_ENDPOINT

    if MODE == "test":
        output_to_console("rule", f"[bold red]:test_tube: Test Mode Active :test_tube:[/]\n", console)
        output_to_console("print", f"API Data sent to :{endpoint}", console)
        output_to_console("print", f"{data=}", console)

        # TODO: update state from data
    else:
        output_to_console("rule", f"[bold green]:chequered_flag: API Call :chequered_flag:[/]\n", console)
        data_dump = json.dumps(data)
        # sending post request and saving response as response object
        r = requests.post(url=endpoint, data=data_dump)
        if r.status_code == 200:
            output_to_console("rule", f"[bold green]:thumbs_up: 200 :thumbs_up:[/]\n", console)
            # if mode != "sticks_2":
            update_state_from_response(db, r, "sticks")
        else:
            output_to_console("rule", f"[bold green]:no_entry_sign::thumbs_down: {r.status_code} :thumbs_down::no_entry_sign:[/]\n", console)
    
