from typing import Optional
import logging
import sys
from pathlib import Path

from .utils import find_venv_dir


mommy_logger = logging.getLogger("mommy")
serious_logger = logging.getLogger("serious")





def mommify(venv_dir: Optional[Path] = None):
    print("normal mommify")

    venv_dir = find_venv_dir(venv_dir=venv_dir)
    serious_logger.info("using venv dir %s", venv_dir)
    