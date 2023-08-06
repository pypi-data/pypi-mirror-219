# setup.py
from setuptools import setup

try:
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
except:
    requirements = ''

setup(
    install_requires=requirements,
    name="idftools",
    author_email="eniodefarias@gmail.com",
    author="eniodefarias",
    version="0.1.3",
    url="",
    description="Um pacote com alguns utilitarios uteis",
    py_modules=["utilities", "driversfactory", "certificate"],
    package_dir={"": "idftools"}
)