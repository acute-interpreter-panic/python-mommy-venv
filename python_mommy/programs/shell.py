from typing import Optional, Dict, Tuple, List
from collections.abc import Iterable
import logging
import sys
from pathlib import Path
from enum import Enum
import re

from ..utils import MOMMY, find_venv_dir, select


mommy_logger = logging.getLogger("mommy")
serious_logger = logging.getLogger("serious")


class Shells(Enum):
    BASH = "bash"
    ZSH = "zsh"
    CSH = "csh"
    FISH = "fish"
    POWER_SHELL = "power shell"


SHELL_TO_COMMENT: Dict[Shells, str] = {
    Shells.BASH: "# {msg}",
    Shells.ZSH: "# {msg}",
    Shells.CSH: "# {msg}",
    Shells.FISH: "# {msg}",
    Shells.POWER_SHELL: "# {msg}",
}


SHELL_TO_ALIAS: Dict[Shells, str] = {
    Shells.BASH: "alias {name}='{interpreter} -m {module}'",
    Shells.ZSH: "alias {name}='{interpreter} -m {module}'",
    Shells.CSH: "alias {name} '{interpreter} -m {module}'",
    Shells.FISH: 'alias {name}="{interpreter} -m {module}"',
    Shells.POWER_SHELL: 'Set-Alias -Name {name}  -Value {interpreter} -m {module}',
}

SHELL_TO_LIKELY_CONFIG_FILE: Dict[Shells, str] = {
    Shells.BASH: "~/.bashrc",
    Shells.ZSH: "~/.zshrc",
    Shells.CSH: "~/.cshrc",
    Shells.FISH: "~/.config/fish/config.fish",
    Shells.POWER_SHELL: "",
}


START_COMMENT = "mommify-start"
END_COMMENT = "mommify-end"


def get_comment(shell: Shells, msg: str) -> str:
    return SHELL_TO_COMMENT[shell].format(msg=msg)

def find_python_interpreter(bin: Path) -> Iterable[Path]:
    for p in bin.iterdir():
        if not p.is_file():
            continue

        if p.name.startswith("python") and "-" not in p.name:
            mommy_logger.info("%s found %s", MOMMY.ROLE, p.name)
            serious_logger.info("found python interpreter %s", p)
            yield p

def generate_aliases(shell: Shells, interpreters: List[Path]) -> str:
    result: List[str] = [get_comment(shell=shell, msg=START_COMMENT)]

    template = SHELL_TO_ALIAS[shell]
    module = "daddy" if MOMMY.ROLE == "daddy" else "mommy"
    for path in interpreters:
        result.append(template.format(
            name=path.name,
            interpreter=path.name,
            module=module
        ))

    result.append(get_comment(shell, END_COMMENT))
    return "\n".join(result)


def get_regex(shell: Shells):
    return re.compile(get_comment(shell, START_COMMENT) + r".*?" + get_comment(shell, END_COMMENT), flags=re.DOTALL)


def find_activate(venv_dir: Path) -> Iterable[Tuple[Shells, Path]]:
    activate_to_shell: Dict[str, Shells] = {
        "activate": Shells.BASH,
        "activate.csh": Shells.CSH,
        "activate.fish": Shells.FISH,
        "Activate.ps1": Shells.POWER_SHELL,
    }

    for p in Path(venv_dir, "bin").iterdir():
        if not p.is_file():
            continue

        if p.name in activate_to_shell:
            yield activate_to_shell[p.name], p


def mommify_venv(venv_dir: Optional[Path] = None):
    venv_dir = find_venv_dir()
    if venv_dir is None:
        mommy_logger.error("%s couldn't find a venv directory to mess up", MOMMY.ROLE)
        serious_logger.error("couldn't find a venv directory")
        exit(1)
    serious_logger.info("using venv dir %s", venv_dir)

    # get activate scripts
    interpreters = list(find_python_interpreter(venv_dir / "bin"))
    for shell, path in find_activate(venv_dir=venv_dir):
        serious_logger.info("%s found at %s", shell.value, path)
        mommy_logger.info("%s takes a look at %s. %s knows its %s", MOMMY.ROLE, path, MOMMY.PRONOUN, shell.value)

        regex = get_regex(shell)
        with path.open("r") as f:
            text = f.read()

        aliases = generate_aliases(shell, interpreters)
        if regex.search(text) is not None:
            serious_logger.info("already found aliases in file => replacing")
            text = re.sub(regex, aliases, text)
        else:
            serious_logger.info("didn't find aliases in file => appending")
            text += "\n" + aliases
        
        with path.open("w") as f:
            serious_logger.info("writing to file %s", path)
            f.write(text)


def mommify_global_config():
    print("what shell do you use?")
    shell = select(options=Shells)
    print()
    content = generate_aliases(shell, list(find_python_interpreter(Path("/", "usr", "bin"))))
    print()
    if shell == Shells.POWER_SHELL:
        print("here is info, how to configure power shell:\nhttps://learn.microsoft.com/en-us/powershell/scripting/learn/shell/creating-profiles?view=powershell-7.5")
    else:
        print("you can probably configure your shell here:")
        print(f"> {SHELL_TO_LIKELY_CONFIG_FILE[shell]}")
    print()
    print(content)
