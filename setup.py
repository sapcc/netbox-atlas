from setuptools import find_packages, setup

from os import path
top_level_directory = path.abspath(path.dirname(__file__))
with open(path.join(top_level_directory, "README.md"), encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="netbox_atlas_plugin",
    version="1.0.2",
    description="A Prometheus SD API plugin for Netbox.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Stefan Hipfel",
    author_email="stefan.hipfel@sap.com",
    install_requires=[],
    packages=find_packages(),
    license="Apache-2.0",
    include_package_data=True,
    keywords=["netbox", "netbox-plugin", "plugin"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.10",
    ],
)
