from setuptools import setup, find_packages

setup(
    name="spectral-mesh-analysis",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24",
        "scipy>=1.10",
        "matplotlib>=3.7",
        "trimesh>=4.0",
        "pyvista>=0.43",
    ],
)