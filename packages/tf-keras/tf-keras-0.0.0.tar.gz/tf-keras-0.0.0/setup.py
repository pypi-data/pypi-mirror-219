"""Setup script."""

from setuptools import find_packages
from setuptools import setup


setup(
    name="tf-keras",
    description="TensorFlow Keras.",
    version="0.0.0",
    url="https://github.com/keras-team/tf-keras",
    author="Keras team",
    author_email="keras-users@googlegroups.com",
    license="Apache License 2.0",
    install_requires=[
    ],
    # Supported Python versions
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
    ],
    packages=find_packages(exclude=("*_test.py",)),
)