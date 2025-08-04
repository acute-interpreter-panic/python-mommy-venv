import random
import sys
from typing import Optional
import json

from .static import colors, get_compiled_config_file


def get_response_from_situation(situation: str, colorize: Optional[bool] = None):
    if colorize is None:
        colorize = sys.stdout.isatty()

    # get message
    config = json.loads(get_compiled_config_file().read_text())
    existing_moods = list(config["moods"].keys())
    template_options = config["moods"][random.choice(existing_moods)][situation]
    template: str = random.choice(template_options)

    template_values = {}
    for key, values in config["vars"].items():
        template_values[key] = random.choice(values)

    message = template.format(**template_values)

    # return message
    if not colorize:
        return message
    return colors.BOLD + message + colors.ENDC


def get_response(code: int, colorize: Optional[bool] = None) -> str:
    return get_response_from_situation("positive" if code == 0 else "negative")


def main():
    print("hi")
