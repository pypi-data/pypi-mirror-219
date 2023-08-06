from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
directory = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="numerical_methods",
    version="0.1.0",
    description="Library for solving mathematical problems in numerical form",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://d1mka.fun",
    author="Dimka-Lab",
    author_email="alexeew.di@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["numerical_methods"],
    include_package_data=True,
    install_requires=["numpy"]
)
