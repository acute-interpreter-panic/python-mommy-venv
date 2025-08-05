import argparse
from enum import Enum

from .utils import MOMMY


def _config_logging(verbose: bool, verbose_all: bool):
    # https://stackoverflow.com/a/59705351/16804841
    import logging

    if verbose_all:
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)


    mommy_logger = logging.getLogger("mommy")
    serious_logger = logging.getLogger("serious")

    def get_mommy_handler():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s~')
        handler.setFormatter(formatter)
        return handler

    mommy_logger.addHandler(get_mommy_handler())


    def get_serious_handler():
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(levelname)s:%(name)s:\t%(message)s")
        handler.setFormatter(formatter)
        return handler

    serious_logger.addHandler(get_serious_handler())
    if verbose:
        serious_logger.setLevel(logging.DEBUG)
        mommy_logger.setLevel(50)
    else:
        serious_logger.setLevel(50)
        mommy_logger.setLevel(logging.INFO)


def _assert_venv(only_warn: bool = False):
    import sys

    if sys.prefix == sys.base_prefix:
        import logging
        mommy_logger = logging.getLogger("mommy")
        serious_logger = logging.getLogger("serious")

        mommy_logger.error("%s doesn't run in a virtual environment~", MOMMY.ROLE)
        serious_logger.error("this should run in a virtual environment")
        if not only_warn:
            exit(1)


def mommify_config():
    parser = argparse.ArgumentParser(description=f"patch the virtual environment which will use {MOMMY.ROLE}")

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="enable verbose and serious output"
    )

    parser.add_argument(
        "--verbose-all",
        action="store_true",
        help="enables serious output and verbose output for every library"
    )

    parser.add_argument(
        '--you', 
        type=str, 
        default='girl', 
        nargs='?',
        help=f'how do you want {MOMMY.ROLE} to call you?'
    )

    args = parser.parse_args()

    _config_logging(args.verbose or args.verbose_all, args.verbose_all)
    MOMMY.YOU = args.you

    
    class Programs(Enum):
        MOMMIFY_GLOBAL_CONFIG = f"prints aliases"
        MOMMIFY_VENV = f"configures aliases for virtual environment"
        MOMMIFY_PATCH_VENV = f"wraps the interpreters in the virtual environment (works for cli tools installed in the venv as well)"
    
    from .utils import select
    print("what do you want to do?")
    p = select(Programs)
    print("")

    from .programs import mommify_global_config, mommify_patch_venv, mommify_venv
    if p == Programs.MOMMIFY_VENV:
        mommify_venv()
    elif p == Programs.MOMMIFY_PATCH_VENV:
        mommify_patch_venv()
    elif p == Programs.MOMMIFY_GLOBAL_CONFIG:
        mommify_global_config()


# run as module
if __name__ == "__main__":
    from . import mommy

    _config_logging(verbose=False, verbose_all=False)
    mommy()
