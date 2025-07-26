import random
import subprocess
import sys
from typing import Optional
import termcolor
import os
import re
import signal

from .config import CONFIG
from .static import RESPONSES, Situation

def _expand_template(template: str) -> str:
    for key, value in CONFIG.items():
        template = template.replace(key, random.choice(value))

    return template + " " + random.choice(CONFIG["MOMMYS_EMOTES"])

def get_response(situation: Situation, colorize: Optional[bool] = None):
    if colorize is None:
        colorize = sys.stdout.isatty()

    # get message
    possible_templates = RESPONSES[random.choice(CONFIG["MOMMYS_MOODS"])][situation]
    message = _expand_template(random.choice(possible_templates))

    # return message
    if not colorize:
        return message
    return termcolor.colored(message, attrs=["bold"])
