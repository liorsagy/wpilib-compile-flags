from os import listdir, walk
from os.path import exists, isdir, join, relpath

from cmakerio.constants import CMAKERIO_ROOT


def generate_header_with_all_includes(path: str):
    print(path)
    if not isdir(path):
        return

    includes = []
    for root, directories, files in walk(join(CMAKERIO_ROOT, "headers")):
        if "ni" in root or "Eigen" in root or "ntcore" in root or "cscore" in root:
            continue

        root = relpath(root, join(CMAKERIO_ROOT, "headers"))
        if "/" in root:
            root = root[root.index("/") + 1:]
            if "/" in root:
                root = root[root.index("/") + 1:]

        includes += map(lambda f: join(root, f), filter(lambda f: f.endswith(".h"), files))

    open(join(path, "AllExternal.h"), "w").write(
        "/* THIS IS AN AUTOMATICALLY GENERATED FILE. YOU SHOULDN'T EDIT IT. */\n" + "\n".join(
            map(lambda include: f"#include <{include}>", includes)))
