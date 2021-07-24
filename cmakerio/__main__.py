from .generate_header_with_all_includes import generate_header_with_all_includes
from .install import install
from sys import argv


if argv[1] == "install":
    if len(argv) > 2:
        install(argv[2])
    else:
        install()
elif argv[1] == "huge-index":
    generate_header_with_all_includes(argv[2])
