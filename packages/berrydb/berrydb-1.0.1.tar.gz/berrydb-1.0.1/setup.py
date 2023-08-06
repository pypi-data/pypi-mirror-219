from setuptools import setup

VERSION = "1.0.1"

DESCRIPTION = "Connect to your BerryDB database"
AUTHOR = "BerryDB"
URL = "https://app.berrydb.io"

setup(
    name="berrydb",
    version=VERSION,
    description=DESCRIPTION,
    url=URL,
    author=AUTHOR,
    license="Proprietary",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "requests",
    ],
    classifiers=[
        "License :: Other/Proprietary License",
    ],
)
