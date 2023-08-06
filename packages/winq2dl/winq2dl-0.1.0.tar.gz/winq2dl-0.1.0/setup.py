import re
from setuptools import setup, find_packages

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('winq2dl.py').read(),
    re.M
    ).group(1)

setup(
    name='winq2dl',
    version=version,
    description='A Python wrapper for the Windows API designed for drawing.',
    long_description=long_description,
    url="https://github.com/AquaQuokka/winq2dl",
    author="AquaQuokka",
    license='BSD-3-Clause',
    py_modules=['winq2dl'],
    scripts=['winq2dl.py'],
    install_requires=["pywin32==306"],
)