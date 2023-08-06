from setuptools import setup

setup(
    name="toypandas",
    version="0.1",
    author="Daniele Traversaro",
    author_email="daniele.traversaro@dibris.unige.it",
    description="An educational library based on Pandas for introductory data science.",
    packages=["toypandas"],
    install_requires=["pandas", "numpy", "matplotlib", "re", "itertools"],
)
