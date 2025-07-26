import sys

from . import get_response
from .static import Situation


def development():
    s = "positive"
    if len(sys.argv) > 1:
        s = sys.argv[1]


    print(get_response(Situation(s)))
