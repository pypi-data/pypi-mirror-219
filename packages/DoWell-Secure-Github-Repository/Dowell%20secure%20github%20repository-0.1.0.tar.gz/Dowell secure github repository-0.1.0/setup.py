# To use a consistent encoding
from codecs import open
from os import path

from setuptools import setup

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name="Dowell secure github repository",
    version="0.1.0",
    description="Dowell secure github repository from DoWell",
    author='uxlivinglab',
    license="Apache License 2.0",
    packages=["doWell_secure_github_repository"],
    include_package_data=True,
    install_requires=["requests"]
)