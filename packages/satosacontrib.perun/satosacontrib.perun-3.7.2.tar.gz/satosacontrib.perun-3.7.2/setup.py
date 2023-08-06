from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="satosacontrib.perun",
    python_requires=">=3.9",
    url="https://github.com/CESNET/satosacontrib.perun.git",
    description="Microservices for SATOSA authentication proxy, made by the Perun team",
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "setuptools",
        "SATOSA~=8.1",
        "pysaml2~=7.1",
        "requests~=2.28",
        "perun.connector~=3.7",
        "PyYAML~=6.0",
        "SQLAlchemy~=1.4",
        "jwcrypto~=1.3",
        "natsort~=8.3.1",
        "python-dateutil~=2.8",
        "geoip2~=4.6",
        "user_agents~=2.2",
        "pymongo~=4.3",
    ],
)
