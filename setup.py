from setuptools import find_packages, setup

with open("VERSION") as fh:
    __version__ = fh.read().strip()

build_version = __version__


requires = ["aiohttp", "aiohttp-devtools"]

setup(
    name="neuromancer",
    version=__version__,
    install_requires=requires,
    include_package_data=True,
    packages=find_packages(),
    extras_require={},
    zip_safe=False,
)
