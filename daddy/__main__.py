from python_mommy_venv import mommy
from python_mommy_venv.static import MOMMY


if __name__ == "__main__":
    MOMMY.set_roles(False)
    mommy()
