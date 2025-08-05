from python_mommy.utils import MOMMY


if __name__ == "__main__":
    MOMMY.set_roles(True)
    from python_mommy import __main__
    __main__.mommify_config()
