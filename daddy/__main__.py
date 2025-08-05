from python_mommy import mommy
from python_mommy.utils import MOMMY


if __name__ == "__main__":
    MOMMY.set_roles(False)
    mommy()
