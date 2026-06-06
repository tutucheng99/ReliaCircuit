from __future__ import annotations

from setuptools import find_packages, setup


setup(
    name="reliacircuit",
    version="0.1.0",
    description="Research artifacts for FDR-controlled sparse circuit mining.",
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.26",
        "pandas>=2.0",
        "pyarrow>=15",
        "scipy>=1.11",
        "matplotlib>=3.7",
    ],
)
