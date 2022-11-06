from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in mdpl_addons/__init__.py
from mdpl_addons import __version__ as version

setup(
	name="mdpl_addons",
	version=version,
	description="Addons",
	author="Mohammad Ali",
	author_email="swe.mirz.ali@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
