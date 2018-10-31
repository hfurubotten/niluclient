import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="niluclient",
    version="0.1.0",
    author="Heine Furubotten",
    description="An API client for getting pollution data "
                "from NILU sensor stations in Norway.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hfurubotten/niluclient",
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)