import random
import sys
from typing import Optional
import time

from .config import load_config
from .static import colors


def get_response_from_situation(situation: str, colorize: Optional[bool] = None):
    start_time = time.time()

    if colorize is None:
        colorize = sys.stdout.isatty()

    # get message
    config = load_config(disable_requests=True)
    existing_moods = list(config["moods"].keys())
    template_options = config["moods"][random.choice(existing_moods)][situation]
    template: str = random.choice(template_options)

    template_values = {}
    for key, values in config["vars"].items():
        template_values[key] = random.choice(values)

    message = template.format(**template_values)

    if config["advanced"]["print_mommy_time"]:
        t_difference = int((time.time() - start_time) * 1000)
        message = f"[{t_difference}ms] " + message

    # return message
    if not colorize:
        return message
    return colors.BOLD + message + colors.ENDC


def get_response(code: int, colorize: Optional[bool] = None) -> str:
    return get_response_from_situation("positive" if code == 0 else "negative", colorize=colorize)


def main():
    # credits to the original project
    # https://github.com/Def-Try/python-mommy/blob/main/python_mommy/__init__.py
    import sys, subprocess
    import time
    from . import get_response

    proc = subprocess.run([
        sys.executable,
        *sys.argv[1:],
    ])

    prev_time = time.time()
    print("")
    print(get_response(proc.returncode))
