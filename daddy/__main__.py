from python_mommy import mommy
from python_mommy.static import MOMMY


if __name__ == "__main__":
    MOMMY.set_roles(False)
    mommy()
