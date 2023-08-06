import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

# with open(here / "requirements.txt", "r") as f:
#     requireds = f.read().splitlines()

# with open(here / "README.md", "r") as f:
#     long_description = f.read()

setup(
    name="souJpg-comm",
    version="1.1.3",
    author="zhaoyufei",
    author_email="",
    description="souJpg-comm",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    # install_requires=requireds,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8.10",
)
