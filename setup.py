# Build-in imports
from setuptools import setup, find_packages

setup(
    name="feature_hero_ml",
    version="0.0.1",
    description="""
        This is a project that builds and implements a simple Feature Store using
        Feast, the main purpose of this project is to help in the training and
        deploying of Machine Learning models into production environments using the
        best MLOps practices.
    """,
    packages=find_packages(),
)
