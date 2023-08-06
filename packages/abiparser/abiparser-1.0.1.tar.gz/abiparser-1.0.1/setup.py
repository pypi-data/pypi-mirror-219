from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='abiparser',
    version='1.0.1',
    description='A Python package to parse Ethereum contract ABI files',
    author='August Radjoe',
    author_email='atg271@gmail.com',
    packages=['abiparser'],
    install_requires=[],  # Add any dependencies here
    long_description=long_description,
    long_description_content_type="text/markdown",
)
