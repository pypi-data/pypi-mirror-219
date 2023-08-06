"""Setup script for realpython-reader"""

import os.path
from setuptools import setup, find_packages

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()


def load_req(path):
    with open(path) as f:
        requirements = f.read().splitlines()
        # this is a workaround for the fact that pip set doesn't support intuitive whl install
        for i in range(len(requirements)):
            if "{CWD}" in requirements[i]:
                requirements[i] = requirements[i].replace("{CWD}", os.getcwd())
    return [r for r in requirements if r and r[0] != '#']


# This call to setup() does all the work
setup(
    name="oasis-api-client",
    version="1.0.0",
    description="OASIS is a Python wrapper of ONNC",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://www.skymizer.com",
    author="The Skymizer Team",
    author_email="hello@skymizer.com",
    license="Apache License 2.0",
    packages=find_packages(),
    package_data={"oasis": ["*"]},
    data_files=[],
    install_requires=["requests", "onnx", "loguru", "sentry-sdk", "packaging"] +
    load_req("requirements.txt"))
