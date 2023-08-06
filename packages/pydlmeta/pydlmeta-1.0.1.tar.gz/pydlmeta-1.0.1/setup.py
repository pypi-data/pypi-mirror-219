"""Setup script for realpython-reader"""
from distutils.core import setup
import os.path
from setuptools import setup, find_packages

def load_req(path):
    with open(path) as f:
        requirements = f.read().splitlines()
        # this is a workaround for the fact that pip set doesn't support intuitive whl install
        for i in range(len(requirements)):
            if "{CWD}" in requirements[i]:
                requirements[i] = requirements[i].replace("{CWD}", os.getcwd())
    return [r for r in requirements if r and r[0] != '#']

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="pydlmeta",
    version="1.0.1",
    license="Apache License 2.0",
    long_description=README, # without this pypi upload will raise warning
    long_description_content_type="text/markdown",  # without this pypi upload will raise warning
    packages=find_packages(),
    package_data={"pydlmeta": ["*"]},
    dependency_links=[
        "https://download.pytorch.org/whl/torch_stable.html",
    ],
    install_requires=(load_req('requirements.txt')),
    data_files=[],
    package_dir={'': '.'},
    entry_points={}
    )
