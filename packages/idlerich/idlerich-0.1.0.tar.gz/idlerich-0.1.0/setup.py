from setuptools import setup

mdata = {}
with open("idlerich/metadata.py", "r") as f:
    for line in f.read().split("\n")[:~0]:
        linedata = [i.strip(" \"") for i in line.split("=")]
        mdata[linedata[0]] = linedata[1]

with open("README.rst", "r") as f:
    readme = f.read()

# set-oop
setup(
    name="idlerich",
    version=mdata["__version__"],
    description="A bootloader that caches and auto-richifies IDLE because I felt lazy.",
    url=mdata["__url__"],
    author=mdata["__author__"],
    author_email=mdata["__authoremail__"],
    license="MIT License",
    packages=["idlerich"],
    install_requires=[
        "rich>=13.0.0a1"
    ],
    python_requires=">=3.6",
    long_description=readme,
    long_description_content_type="text/x-rst",
    entry_points = {
        "console_scripts": ["idlerich=idlerich:main"]
    }
)
