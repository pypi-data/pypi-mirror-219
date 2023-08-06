from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A simple examle pypi package'
LONG_DESCRIPTION = 'A simple examle pypi package'

setup(
    name="example-pkg-darksidevt",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Darksidevt",
    author_email="artyisnummberone@gmail.com",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'example', 'package'],
)