import json
import requests

from copy import deepcopy

from rich.console import Console

from ..crud import state, effects

from ..models import EffectPreset

from . import colour_helpers

from ..config import *

from ..common import output_to_console

if CONSOLE_OUTPUT:
    console = Console()
else:
    console = None


def update_state_from_response(db, response):
    response_dict = response.json()
    new_effect_preset = EffectPreset()
    new_effect_preset.name = response_dict["effect"]["name"]
    new_effect_preset.type = response_dict["effect"]["type"]
    new_effect_preset.config = response_dict["effect"]
    state.update_state_ledfx(db, new_effect_preset)


def create_api_request_string(db, fx_type, gradient, effect_id=None):
    """Uses hard-coded dictionaries that have values replaced in them, to create
    the API string for the request."""

    data = {
        "active": True,
        "type": str(fx_type),
        "config": {
            "blur": 0.0,
            "gradient": gradient,
            "band_count": 10,
            "gradient_repeat": 10,
        },
    }
    return data


def create_api_effect_request_string(db, effect_id, colourscheme):
    """Creates the API string needed when creating an effect, from the effect string in
    the database and the current colourscheme."""
    gradient = colour_helpers.create_gradient(colourscheme, mode="single")
    effect_config = deepcopy(effects.get_effect_string_by_id(db, effect_id))
    index = list(effect_config["config"].values())
    gradient_indices = [i for i, x in enumerate(index) if x == "#GGGGGG"]
    other_indices = [i for i, x in enumerate(index) if x == "#HHHHHH"]
    if gradient_indices:
        for key in [list(effect_config["config"].keys())[g] for g in gradient_indices]:
            effect_config["config"][key] = gradient
    if other_indices:
        for idx, key in enumerate(
            [list(effect_config["config"].keys())[o] for o in other_indices]
        ):
            try:
                effect_config["config"][key] = colourscheme[idx]
            except IndexError:
                effect_config["config"][key] = colourscheme[0]

    return effect_config


def perform_api_call(db, data):

    endpoint = API_ENDPOINT

    if MODE == "test":
        output_to_console(
            "rule", f"[bold red]:test_tube: Test Mode Active :test_tube:[/]\n", console
        )
        output_to_console("print", f"API Data sent to :{endpoint}", console)
        output_to_console("print", f"{data=}", console)

    else:
        output_to_console(
            "rule",
            f"[bold green]:chequered_flag: API Call :chequered_flag:[/]\n",
            console,
        )
        data_dump = json.dumps(data)
        r = requests.post(url=endpoint, data=data_dump)
        if r.status_code == 200:
            output_to_console(
                "rule", f"[bold green]:thumbs_up: 200 :thumbs_up:[/]\n", console
            )
            update_state_from_response(db, r)
        else:
            output_to_console(
                "rule",
                f"[bold green]:no_entry_sign::thumbs_down: {r.status_code} :thumbs_down::no_entry_sign:[/]\n",
                console,
            )


def get_api_response(endpoint):
    r = requests.get(url=endpoint)
    if r.status_code == 200:
        output_to_console(
            "rule", f"[bold green]:thumbs_up: 200 :thumbs_up:[/]\n", console
        )
        return r.json()
    else:
        output_to_console(
            "rule",
            f"[bold green]:no_entry_sign::thumbs_down: {r.status_code} :thumbs_down::no_entry_sign:[/]\n",
            console,
        )
        return None
