import sys
from pathlib import Path
import stat

from . import get_response
from .static import Situation


def development():
    s = "positive"
    if len(sys.argv) > 1:
        s = sys.argv[1]


    print(get_response(Situation(s)))


TEMPLATE = """#!{inner_bin}
# -*- coding: utf-8 -*-

import sys, subprocess
from python_mommy_venv import get_response, Situation


INTERPRETER = "{inner_bin}"
result = subprocess.run([INTERPRETER] + sys.argv[1:])
code = result.returncode

print()
print(get_response(Situation.POSITIVE if code == 0 else Situation.NEGATIVE))
exit(code=code)
"""


def mommify_venv():
    v = ".venv"
    if len(sys.argv) > 1:
        v = sys.argv[1]

    bin_path = Path(v, "bin")
    bin_path = bin_path.resolve()
    print(bin_path)

    for path in bin_path.iterdir():
        if not path.is_symlink():
            continue
        
        name = path.name
        if name.startswith("inner_"):
            continue
        target = path.resolve()

        print("")
        print(f"modifying {name} ({target})")

        # creating inner symlink
        inner_bin = Path(bin_path, "inner_" + name)
        if inner_bin.exists():
            print(f"inner symlink does already exist {inner_bin}")
            print("skipping")
            continue

        print(f"creating symlink: {inner_bin} -> {target}")
        Path(bin_path, "inner_" + name).symlink_to(target)

        # remove original symlink
        print(f"removing original symlink: {path}")
        path.unlink()

        # creating the wrapper string
        print("writing wrapper script")
        with path.open("w") as f:
            f.write(TEMPLATE.format(inner_bin=str(inner_bin)))
        print("making wrapper script executable")
        path.chmod(path.stat().st_mode | stat.S_IEXEC)
