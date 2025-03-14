import colorsys
import math
import re

from copy import deepcopy

from rich.console import Console

from random import choice, shuffle, uniform

from . import colour_helpers

from ..crud import state, effects

from ..config import *

from ..common import output_to_console

if CONSOLE_OUTPUT:
    console = Console()
else:
    console = None


def generate_random_hex_colour() -> str:
    # returns a 6-digit hex colour in the format #AABBCC
    candidates = [
        "#ff0000",
        "#00ff00",
        "#0000ff",
        "#fa9d00",
        "#ffff00",
        "#9370db",
        "#808080",
        "#00ffff",
        "#ff00ff",
    ]
    colour = choice(candidates)
    output_to_console("print", f"Random Colour: {colour}", console)
    return colour


def convert_int_to_hex(colour_tuple) -> str:
    return "#{:02x}{:02x}{:02x}".format(
        colour_tuple[0], colour_tuple[1], colour_tuple[2]
    )


def convert_to_rgb(colour_string):
    colours = colour_string.lstrip("#")
    return f"rgb{tuple(int(colours[i:i+2], 16) for i in (0, 2, 4))}"


def convert_to_rgb_int(colour_string):
    colours = colour_string.lstrip("#")
    return tuple(int(colours[i : i + 2], 16) for i in (0, 2, 4))


def adjacent_colours(rgb_colour, d=30 / 360):  # Assumption: r, g, b in [0, 255]
    r, g, b = [c / 255 for c in convert_to_rgb_int(rgb_colour)]  # Convert to [0, 1]
    h, l, s = colorsys.rgb_to_hls(r, g, b)  # RGB -> HLS
    h = [(h + d) % 1 for d in (-d, d)]  # Rotation by d
    adjacent = [
        list(map(lambda x: int(round(x * 255)), colorsys.hls_to_rgb(hi, l, s)))
        for hi in h
    ]  # H'LS -> new RGB
    hex_list = [convert_int_to_hex(colour) for colour in adjacent]
    hex_list.insert(1, rgb_colour)
    return hex_list


def sort_colour_list(colour_list):
    def lum(r, g, b):
        return math.sqrt(0.241 * r + 0.691 * g + 0.068 * b)

    if colour_list is None:
        return []
    if len(colour_list) == 0:
        return []
    if len(colour_list) == 1:
        return colour_list
    """Takes a list of hex-format colours and sorts them in brightness order"""

    colour_list_nums = [convert_to_rgb_int(colour) for colour in colour_list]
    colour_list_nums.sort(key=lambda rgb: lum(*rgb), reverse=False)
    colour_list_hex = [convert_int_to_hex(colour) for colour in colour_list_nums]

    return colour_list_hex


def create_gradient(colour_list, mode, limit=6):
    """takes a list of hex-format colours, and outputs
    a linear gradient for ledfx based on the colour list.
    if there are more than limit entries, only a random selection
    of length limit will be added to the gradient."""
    colour_list = sort_colour_list(colour_list)
    if len(colour_list) > limit:
        shuffle(colour_list)
        colour_list = colour_list[:limit]
    if len(colour_list) == 0:
        colour_list = [generate_random_hex_colour()]
    if len(colour_list) == 1 and mode == "single":
        # return a single colour (otherwise 1-colour gradient)
            return colour_list[0]
    increment = int(98 / len(colour_list))
    location = 0
    stem = "linear-gradient(90deg, rgb(0, 0, 0) 0%"
    for colour in colour_list:
        colour_rgb = convert_to_rgb(colour)
        location += increment
        current_colour = f", {colour_rgb} {location}%"
        stem += current_colour
    stem += ")"
    return stem


def refine_colourscheme(db, colour_list: list, colour_mode: str) -> list:
    # Takes a list of colours and a mode from an effect
    # returns an appropriately-altered gradient
    output_to_console(
        "print", "[bright_cyan]colour_helpers[/].[bold]refine_colourscheme[/]", console
    )
    output_to_console("print", f"{colour_list=}, {colour_mode=}", console)
    colour_list = list(set(colour_list))
    if colour_mode == "gradient":
        current_state = state.get_state(db)
        ledfx_max_colours = current_state.ledfx_max_colours
        unsorted_colourscheme = colour_list[:ledfx_max_colours]
        colourscheme = sort_colour_list(unsorted_colourscheme)
    elif colour_mode == "adjacent":
        colour = colour_list[0]
        colourscheme = adjacent_colours(colour)
    elif colour_mode == "single":
        colourscheme = [colour_list[0]]

    output_to_console("print", f"Returning {colourscheme=}", console)
    return colourscheme


def extract_gradient(gradient_string):
    """Takes a gradient string in rgb or hex value.
    Returns a list of hex values of colours."""
    rgb_matches = re.findall(r"(\d+),\s*(\d+),\s*(\d+)", gradient_string)
    hex_matches = [convert_int_to_hex([int(x) for x in rgb]) for rgb in rgb_matches]
    hex_finds = re.findall(r"#[A-Fa-f0-9]+", gradient_string)
    if hex_finds:
        hex_matches += hex_finds
    return hex_matches

