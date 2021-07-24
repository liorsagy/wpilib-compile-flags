from json import loads
from os import listdir
from os.path import exists, join
from sys import argv
from typing import List, Union

from cmakerio.constants import NI_LIBRARIES, NI_VERSION, WPILIB_VERSION, WPILIB_LIBRARIES
from cmakerio.dependency import Dependency
from cmakerio.utilities import until


def install(project: Union[str, None] = None) -> None:
    dependencies: List[Dependency] = []

    for library in NI_LIBRARIES:
        dependencies.append(
            Dependency(
                url="https://frcmaven.wpi.edu/ui/api/v1/download?repoKey=release&path=edu/wpi/first/ni-libraries",
                category="ni",
                name=library,
                version=NI_VERSION,
                shared=True,
            )
        )

    for library in WPILIB_LIBRARIES:
        dependencies.append(
            Dependency(
                url=f"https://frcmaven.wpi.edu/ui/api/v1/download?repoKey=release&path=edu/wpi/first/{library}",
                category="wpilib",
                name=f"{library}-cpp",
                version=WPILIB_VERSION,
                shared=False,
            )
        )

    if project is not None and exists(join(project, "vendordeps")):
        project = join(project, "vendordeps")
        for dep in listdir(project):
            try:
                vendordeps = loads(open(join(project, dep), "r").read())

                for d in vendordeps["cppDependencies"]:
                    dependencies.append(
                        Dependency(
                            url=(
                                f"{vendordeps['mavenUrls'][0].removesuffix('/')}/{d['groupId'].replace('.', '/')}" if d[
                                                                                                                          "version"] != "wpilib" else "https://frcmaven.wpi.edu/ui/api/v1/download?repoKey=release&path=edu/wpi/first/wpilibNewCommands"),
                            category=until(vendordeps["name"].lower(), "-", remove=True),
                            name=d["artifactId"],
                            version=(d["version"] if d["version"] != "wpilib" else WPILIB_VERSION),
                            shared=d["sharedLibrary"],
                        )
                    )
            except:
                pass

    i = 0
    for dependency in dependencies:
        print(f"Progress: {int(i / len(dependencies) * 100)}%")
        dependency.install()
        i += 1
