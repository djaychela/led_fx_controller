# config.py - global constants are set here, and imported into modules where they are used.

# Sets the base URL for LedFX API calls - should be the IP of the LedFX instance (127.0.0.1 for local)
API_BASE_URL = "http://192.168.1.238:8888"

# Sets the API endpoints based on the above.  Dependent on your LedFX setup
API_ENDPOINT = f"{API_BASE_URL}/api/virtuals/virtual-1/effects"

# Sets the base URL for Controller API - note port difference from base URL!
FX_CTRL_BASE_URL = "http://127.0.0.1:8000"

# API URLs for timed_calls.py:
EFFECT_URL = f"{FX_CTRL_BASE_URL}/state/change_effect"
COLOUR_URL = f"{FX_CTRL_BASE_URL}/state/change_colour"
VIRTUAL_URL = f"{API_BASE_URL}/api/virtuals/virtual-1/effects"

# Sets the mode - running or otherwise.  "run" - Normal or "test" for text output of API call without making it.
MODE = "run"

# Sets whether there will be output to the console:
CONSOLE_OUTPUT = True

# Sets the timeout in seconds for timed_calls.py
TIMED_CALL_TIMEOUT = 120

# Effect type to never choose - caused issues!
NEVER_CHOOSE_EFFECTS_TYPE = ["gradient"]
