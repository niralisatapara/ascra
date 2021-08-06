from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in ascra/__init__.py
from ascra import __version__ as version

setup(
	name="ascra",
	version=version,
	description="Testing App",
	author="TEST",
	author_email="niralisatapara@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
