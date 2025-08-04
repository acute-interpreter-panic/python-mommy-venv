from __future__ import annotations

from pathlib import Path
import os
import logging
from typing import Optional
import sys


logger = logging.Logger(__name__)


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
