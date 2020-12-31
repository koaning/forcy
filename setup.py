from setuptools import setup, find_packages

base_packages = ["numpy>=1.15.4", "scipy>=1.2.0", "scikit-learn>=0.20.2",
                 "pandas>=0.23.4"]

dev_packages = ["flake8>=3.6.0", "pytest==4.0.2", "jupyterlab>=0.35.4"]


setup(
    name="forcy",
    version="0.0.1",
    packages=find_packages(exclude=['notebooks']),
    install_requires=base_packages,
    extras_require={
        "dev": dev_packages
    }
)
