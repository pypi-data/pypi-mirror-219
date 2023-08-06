from setuptools import find_packages, setup

setup(
    name="my_awesome_lib",
    packages=find_packages(include=["my_awesome_lib"]),
    version="0.1.0",
    description="My first Python library",
    author="Me",
    license="MIT",
    install_requires=[],
    test_requires=["pytest"],
    setup_requires=["pytest-runner"],
    test_suite="tests",
)
