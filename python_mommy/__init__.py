
try:
    import sys 
    import random
    from typing import Optional
    import time
    from dataclasses import dataclass

    from .config import load_config
    from .utils import colors

except (ModuleNotFoundError, ImportError):
    import sys, subprocess

    proc = subprocess.run([
        sys.executable,
        *sys.argv[1:],
    ])
    sys.exit(proc.returncode)


@dataclass
class Context:
    mommy_start_time: float = 0
    execution_time: int = 0


def get_response_from_situation(situation: str, colorize: Optional[bool] = None, context: Optional[Context] = None):
    context = context if context is not None else Context()

    if colorize is None:
        colorize = sys.stdout.isatty()

    # get message
    config = load_config(disable_requests=False)
    existing_moods = list(config["moods"].keys())
    template_options = config["moods"][random.choice(existing_moods)][situation]
    template: str = random.choice(template_options)

    template_values = {}
    for key, values in config["vars"].items():
        template_values[key] = random.choice(values)

    message = template.format(**template_values)

    if colorize:
        message = colors.BOLD + message + colors.ENDC

    prefix = ""
    if config["advanced"]["print_time"]:
        prefix += f"[{context.execution_time}ms] "
    
    if config["advanced"]["print_mommy_time"]:
        t_difference = round((time.time() - context.mommy_start_time) * 1000)
        prefix += f"[{t_difference}ms] "

    return prefix + message.replace("\n", "\n" + " " * len(prefix))

def get_response(code: int, colorize: Optional[bool] = None, context: Optional[Context] = None) -> str:
    return get_response_from_situation("positive" if code == 0 else "negative", colorize=colorize, context=context)


def mommy():
    # credits to the original project
    # https://github.com/Def-Try/python-mommy/blob/main/python_mommy/__init__.py
    import sys, subprocess
    import time
    from . import get_response

    context = Context()

    prev_time = time.time()
    proc = subprocess.run([
        sys.executable,
        *sys.argv[1:],
    ])
    context.mommy_start_time = time.time()
    context.execution_time = round((time.time() - prev_time) * 1000)

    print("")
    print(get_response(proc.returncode, context=context))
