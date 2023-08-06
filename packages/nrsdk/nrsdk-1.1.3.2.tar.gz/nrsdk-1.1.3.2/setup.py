from setuptools import setup
from setuptools import find_packages

VERSION = '1.1.3.2'
AUTHOR='eegion'
EMAIL='hehuajun@eegion.com'
REQUIRED = [
    'beautifulsoup',
    "lxml"
]

setup(
    name='nrsdk',  # package name
    version=VERSION,  # package version
    author=AUTHOR,
    author_email=EMAIL,
    requires=REQUIRED,
    description='Api for use quanlan device, since v1.1.3.2',  # package description
    packages=find_packages(),
    package_data={
        "nrsdk": ["lib/*.dll"],
        "":["*.txt", "*.md"]
    },
    zip_safe=False,
)