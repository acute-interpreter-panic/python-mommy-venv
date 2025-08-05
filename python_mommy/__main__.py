import argparse

from .static import MOMMY



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


def mommify_venv(is_mommy: bool = True):
    MOMMY.set_roles(is_mommy)

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

    parser.add_argument(
        "-r", "--no-requests",
        action="store_true",
        help=f"by default {MOMMY.ROLE} makes one request to GitHub to fetch the newest responses, this disables that"
    )

    parser.add_argument(
        "--legacy",
        action="store_true",
        help="Currently it will add aliases in the selected source file, in legacy mode it will directly wrap the symlinks to the interpreter of the venv in a wrapper script."
    )


    args = parser.parse_args()

    _config_logging(args.verbose or args.verbose_all, args.verbose_all)
    MOMMY.YOU = args.you
    _assert_venv()

    from .mommify import legacy_mommify, mommify
    if args.legacy:
        legacy_mommify()
    else:
        mommify()

def daddify_venv():
    return mommify_venv(is_mommy=False)


# run as module
if __name__ == "__main__":
    from . import mommy

    _config_logging(verbose=False, verbose_all=False)
    mommy()
