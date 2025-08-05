from typing import Optional, Dict, Tuple, List
from collections.abc import Iterable
import logging
import sys
from pathlib import Path
from enum import Enum
import re

from .utils import find_venv_dir, select
from ..static import MOMMY


mommy_logger = logging.getLogger("mommy")
serious_logger = logging.getLogger("serious")


class SupportedShells(Enum):
    BASH = "bash"
    ZSH = "zsh"
    CSH = "csh"
    FISH = "fish"
    POWER_SHELL = "power shell"


SHELL_TO_COMMENT: Dict[SupportedShells, str] = {
    SupportedShells.BASH: "# {msg}",
    SupportedShells.ZSH: "# {msg}",
    SupportedShells.CSH: "# {msg}",
    SupportedShells.FISH: "# {msg}",
    SupportedShells.POWER_SHELL: "# {msg}",
}


SHELL_TO_ALIAS: Dict[SupportedShells, str] = {
    SupportedShells.BASH: "alias {name}='{interpreter} -m {module}'",
    SupportedShells.ZSH: "alias {name}='{interpreter} -m {module}'",
    SupportedShells.CSH: "alias {name} '{interpreter} -m {module}'",
    SupportedShells.FISH: 'alias {name}="{interpreter} -m {module}"',
    SupportedShells.POWER_SHELL: 'Set-Alias -Name {name}  -Value {interpreter} -m {module}',
}


START_COMMENT = "mommify-start"
END_COMMENT = "mommify-end"


def get_comment(shell: SupportedShells, msg: str) -> str:
    return SHELL_TO_COMMENT[shell].format(msg=msg)

def find_python_interpreter(bin: Path) -> Iterable[Path]:
    for p in bin.iterdir():
        if not p.is_file():
            continue

        if p.name.startswith("python") and "-" not in p.name:
            serious_logger.info("found python interpreter %s", p)
            yield p

def generate_aliases(shell: SupportedShells, bin: Path) -> str:
    result: List[str] = [get_comment(shell=shell, msg=START_COMMENT)]

    template = SHELL_TO_ALIAS[shell]
    module = "daddy" if MOMMY.ROLE == "daddy" else "mommy"
    for path in find_python_interpreter(bin=bin):
        result.append(template.format(
            name=path.name,
            interpreter=path.name,
            module=module
        ))

    result.append(get_comment(shell, END_COMMENT))
    return "\n".join(result)


def get_regex(shell: SupportedShells):
    return re.compile(get_comment(shell, START_COMMENT) + r".*?" + get_comment(shell, END_COMMENT), flags=re.DOTALL)


def find_activate(venv_dir: Path) -> Iterable[Tuple[SupportedShells, Path]]:
    activate_to_shell: Dict[str, SupportedShells] = {
        "activate": SupportedShells.BASH,
        "activate.csh": SupportedShells.CSH,
        "activate.fish": SupportedShells.FISH,
        "Activate.ps1": SupportedShells.POWER_SHELL,
    }

    for p in Path(venv_dir, "bin").iterdir():
        if not p.is_file():
            continue

        if p.name in activate_to_shell:
            yield activate_to_shell[p.name], p


def mommify_local(venv_dir: Optional[Path] = None):
    venv_dir = find_venv_dir()
    if venv_dir is None:
        mommy_logger.error("%s couldn't find a venv directory to mess up~", MOMMY.ROLE)
        serious_logger.error("couldn't find a venv directory")
        exit(1)
    serious_logger.info("using venv dir %s", venv_dir)

    # get activate scripts
    for shell, path in find_activate(venv_dir=venv_dir):
        serious_logger.info("%s found at %s", shell.value, path)
        mommy_logger.info("%s takes a look at %s. %s knows its %s", MOMMY.ROLE, path, MOMMY.PRONOUN, shell.value)

        regex = get_regex(shell)
        with path.open("r") as f:
            text = f.read()

        aliases = generate_aliases(shell, venv_dir / "bin")
        if regex.search(text) is not None:
            serious_logger.info("already found aliases in file => replacing")
            text = re.sub(regex, aliases, text)
        else:
            serious_logger.info("didn't find aliases in file => appending")
            text += "\n" + aliases
        
        with path.open("w") as f:
            serious_logger.info("writing to file %s", path)
            f.write(text)



def mommify_global():
    shell = select(options=SupportedShells)
    print()
    print(generate_aliases(shell, Path("/", "usr", "bin")))

class Mode(Enum):
    LOCAL = "automatically edit the source file in your virtual environment"
    GLOBAL = "tells you how to edit you'r .bashrc/.zshrc to mommify your whole system"


def mommify(venv_dir: Optional[Path] = None):
    print("normal mommify")

    mode = select(options=Mode)
    print()
    
    if mode == Mode.LOCAL:
        mommify_local(venv_dir=venv_dir)
    elif mode == Mode.GLOBAL:
        mommify_global()
    else:
        raise NotImplementedError
