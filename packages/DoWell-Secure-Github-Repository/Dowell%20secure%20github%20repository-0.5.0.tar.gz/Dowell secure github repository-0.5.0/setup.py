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
    version="0.5.0",
    description="Dowell secure github repository from DoWell",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='uxlivinglab',
    license="Apache License 2.0",
    packages=["doWellSecureGithubRepository"],
    include_package_data=True,
    install_requires=["requests"]
)