from typing import Optional, List, TypeVar, Tuple, Callable
from collections.abc import Iterable
from pathlib import Path
import logging
import sys
from enum import Enum



class MOMMY:
    ROLE = "mommy"
    PRONOUN = "her"
    YOU = "girl"

    @classmethod
    def set_roles(cls, is_mommy: bool):
        if is_mommy:
            cls.ROLE = "mommy"
            cls.PRONOUN = "her"
        else:
            cls.ROLE = "daddy"
            cls.PRONOUN = "his"

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


T = TypeVar('T')


def get_integer(bounds: Optional[Tuple[int, int]]) -> int:
    while True:
        s = input("[int]> ")
        try:
            i = int(s)
        except ValueError:
            print(f"{colors.FAIL}{s} is not an integer{colors.ENDC}")
            continue

        if bounds is None:
            return i
        
        if i < bounds[0]:
            print(f"{colors.FAIL}{i} isn't >= {bounds[0]}{colors.ENDC}")
            continue

        if i > bounds[1]:
            print(f"{colors.FAIL}{i} isn't <= {bounds[1]}{colors.ENDC}")

        return i


def select(options: Iterable[T], to_string: Optional[Callable[[T], str]] = None) -> T:
    options = list(options)

    if to_string is None:
        if isinstance(options[0], Enum):
            to_string = lambda x: x.value
        else:
            to_string = lambda x: str(x)
    
    s_rows: List[str] = []
    for i, o in enumerate(options):
        s_rows.append(f"{colors.OKCYAN}{i}{colors.ENDC}: {to_string(o)}")

    print("\n".join(s_rows))

    return options[get_integer(bounds=(0, len(options) - 1))]


def find_venv_dir(venv_dir: Optional[Path] = None) -> Optional[Path]:
    mommy_logger = logging.getLogger("mommy")
    serious_logger = logging.getLogger("serious")


    if venv_dir is not None:
        if venv_dir.exists():
            serious_logger.debug("venv dir was specified")
            return venv_dir
        else:
            serious_logger.warning("specified venv dir %s wasn't found", venv_dir)
            mommy_logger.warning("%s could not find the venv dir %s %s specified~ %s", MOMMY.ROLE, MOMMY.PRONOUN, MOMMY.YOU, venv_dir)
    
    if sys.prefix != sys.base_prefix:
        serious_logger.debug("detected running in venv %s", sys.prefix)
        return Path(sys.prefix)
    
    possible_venv_dirs: List[Path] = []
    for sub_dir in Path.cwd().iterdir():
        if not sub_dir.is_dir():
            continue

        if Path(sub_dir, "pyvenv.cfg").exists():
            serious_logger.debug("found venv at %s", sub_dir)
            possible_venv_dirs.append(sub_dir)

    if len(possible_venv_dirs) == 1:
        serious_logger.debug("only one possible venv dir")
        return possible_venv_dirs[0]
    
    if len(possible_venv_dirs) > 1:
        serious_logger.debug("found multiple possible venv dirs. initializing user input")
        return select(possible_venv_dirs, to_string=lambda x: x.name)
    
