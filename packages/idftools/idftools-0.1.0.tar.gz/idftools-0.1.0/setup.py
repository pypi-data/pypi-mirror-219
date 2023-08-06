# setup.py
from setuptools import setup

setup(
    name="idftools",
    author_email="eniodefarias@gmail.com",
    author="eniodefarias",
    version="0.1.0",
    url="",
    description="Um pacote com alguns utilitarios uteis",
    py_modules=["utilities", "driversfactory", "certificate"],
    package_dir={"": "idftools"}
)