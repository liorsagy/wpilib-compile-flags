from dataclasses import dataclass
from io import BytesIO
from os.path import join, basename
from typing import Union
from urllib.error import HTTPError
from urllib.request import urlopen
from zipfile import ZipFile

from cmakerio.constants import CMAKERIO_ROOT
from cmakerio.utilities import until


@dataclass
class Dependency:
    url: str
    category: str
    name: str
    version: str
    shared: bool

    def get(self, part: str) -> Union[ZipFile, None]:
        try:
            response = urlopen(
                f"{self.url}/{self.name}/{self.version}/{self.name}-{self.version}-{part}.zip"
            )
            return ZipFile(BytesIO(response.read()))
        except HTTPError:
            return None

    def headers(self) -> bool:
        headers_zip = self.get("headers")
        if headers_zip is None:
            return False

        headers_zip.extractall(
            join(CMAKERIO_ROOT, "headers", self.category, self.name.replace("-cpp", "").lower())
        )
        return True

    def roborio(self) -> bool:
        library_zip = self.get("linuxathena" + ("" if self.shared else "static"))
        if library_zip is None:
            return False

        for library in filter(lambda f: ".so" in f or ".a" in f, library_zip.namelist()):
            libname = basename(library)
            libname = until(libname, ".so")
            libname = until(libname, ".a")
            libname = libname.lower().replace("_", "").replace("-", "").replace("cpp", "")

            open(join(CMAKERIO_ROOT, "roborio", "lib", libname), "wb").write(library_zip.read(library))

        return True

    def install(self):
        print(f"Installing {self.category}.{self.name}")
        self.headers()
        self.roborio()
