from setuptools import setup
from setuptools import find_packages


VERSION = '0.1.0-alpha.1'

setup(
    name='universeparticle',  # package name
    version=VERSION,  # package version
    description='common util',  # package description
    packages=find_packages(),
    zip_safe=False,
)