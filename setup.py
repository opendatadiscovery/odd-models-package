from setuptools import setup, find_packages
import os

version = os.environ['ODD_MODELS_VERSION']

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requires = [
    'connexion==2.7.0',
    'pydantic==1.8.2',
    'flask-compress==1.10.1'
]

classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
]

setup(
    name="odd-models",
    version=version,
    author="Open Data Discovery",
    author_email="pypi@opendatadiscovery.org",
    description="Open Data Discovery Models",
    license="Apache License 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/opendatadiscovery/odd-contract-package",
    packages=find_packages(exclude=['test*']),
    include_package_data=True,
    install_requires=requires,
    package_data={'': ['openapi/openapi.yaml']},
    classifiers=classifiers,
    python_requires='>=3.6',
)
