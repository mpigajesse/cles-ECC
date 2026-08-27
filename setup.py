"""Setup configuration for ECC Key Generator project."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ecc-key-generator",
    version="0.1.0",
    author="Jesse",
    author_email="mpigajesse@gmail.com",
    description="Educational ECC key pair generator with mathematical transparency",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mpigajesse/cles-ECC",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Education :: Computer Science",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pytest>=7.4.0",
        "pytest-cov>=4.1.0",
        "sympy>=1.12",
        "ecdsa>=0.18.0",
        "colorama>=0.4.6",
    ],
)
