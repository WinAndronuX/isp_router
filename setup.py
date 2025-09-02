from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in isp_router/__init__.py
from isp_router import __version__ as version

setup(
    name="isp_router",
    version=version,
    description="Mikrotik Router Administration",
    author="Fastnet",
    author_email="admiin@fastnet.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
