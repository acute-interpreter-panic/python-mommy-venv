import random
import subprocess
import sys
from typing import Optional
import os
import re
import signal

from .config import get_mood, get_template_values
from .static import RESPONSES, Situation, colors


def get_response(situation: Situation, colorize: Optional[bool] = None):
    if colorize is None:
        colorize = sys.stdout.isatty()

    # get message
    mood = get_mood()
    template = random.choice(RESPONSES[mood][situation])
    message = template.format(**get_template_values(mood))

    # return message
    if not colorize:
        return message
    return colors.BOLD + message + colors.ENDC
