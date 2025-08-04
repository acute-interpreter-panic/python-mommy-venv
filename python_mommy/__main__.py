from pathlib import Path
import logging
import sys
import argparse

from . import mommy
from .config import load_config
from .static import MOMMY
from .legacy_mommify import legacy_mommify

log_level = logging.INFO

mommy_logger = logging.getLogger("mommy")
mommy_logger.setLevel(logging.INFO)
serious_logger = logging.getLogger("serious")
serious_logger.setLevel(50)


def _config_logging(verbose: bool):
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        mommy_logger.setLevel(50)
        serious_logger.setLevel(logging.DEBUG)

def _assert_venv(only_warn: bool = False):
    if sys.prefix == sys.base_prefix:
        mommy_logger.error("%s doesn't run in a virtual environment~", MOMMY.ROLE)
        serious_logger.error("this should run in a virtual environment")
        if not only_warn:
            exit(1)


def mommify_venv(is_mommy: bool = True):
    MOMMY.set_roles(is_mommy)

    parser = argparse.ArgumentParser(description="patch the virtual environment to use mommy")

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="enable verbose and serious output"
    )

    parser.add_argument(
        '--you', 
        type=str, 
        default='girl', 
        nargs='?',
        help='how do you want mommy to call you?'
    )

    parser.add_argument(
        "-r", "--no-requests",
        action="store_true",
        help="by default if makes one request to GitHub to fetch the newest responses, this disables that"
    )

    args = parser.parse_args()

    MOMMY.YOU = args.you
    _config_logging(args.verbose)
    _assert_venv()

    legacy_mommify()


def daddify_venv():
    return mommify_venv(is_mommy=False)


# run as module
if __name__ == "__main__":
    mommy()
