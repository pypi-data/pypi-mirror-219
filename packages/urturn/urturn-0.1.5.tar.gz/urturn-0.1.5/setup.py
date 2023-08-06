"""Setup urturn
"""

import subprocess
import os
import re
import json
import setuptools

_VERSION_FILE_PATH = os.path.join('urturn', 'VERSION')
_REQUIREMENTS_FILE_PATH = os.path.join('urturn', 'REQUIREMENTS')

if not os.path.isfile(_VERSION_FILE_PATH):
    urturn_version = (
        subprocess.run(
            ["git", "describe", "--tags"],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout
        .decode('utf-8')
        .strip()
    )

    print(urturn_version)

    assert re.fullmatch(r"\d+\.\d+\.\d+", urturn_version), \
        f"No valid version found: {urturn_version}!"

    with open(_VERSION_FILE_PATH, 'w', encoding="utf-8") as f:
        f.write(urturn_version)
else:
    with open(_VERSION_FILE_PATH, 'r', encoding="utf-8") as f:
        urturn_version = f.read().strip()

if not os.path.isfile(_REQUIREMENTS_FILE_PATH):
    with open("requirements.txt", "r", encoding="utf-8") as f:
        requires = f.read().split()

    with open(_REQUIREMENTS_FILE_PATH, 'w', encoding="utf-8") as f:
        json.dump(requires, f)
else:
    with open(_REQUIREMENTS_FILE_PATH, 'r', encoding="utf-8") as f:
        requires = json.load(f)

setuptools.setup(
    name="urturn",
    version=urturn_version,  # determined by release in github
    author="Matthias Rieck",
    author_email="Matthias.Rieck@tum.de",
    description="Analyse git repositories",
    long_description="Analyse git repositories",
    url="https://github.com/MatthiasRieck/urturn",
    packages=setuptools.find_packages(exclude=["tests*"]),
    package_data={"urturn": [
        "VERSION",
        "REQUIREMENTS",
        "templates/*",
    ]},
    include_package_data=True,
    install_requires=requires,  # determined by requirements.txt
)
