from setuptools import setup
from yaml import safe_load

with open("config.yaml") as fp:
    data = safe_load(fp)

with open("README.md", "r") as fd:
    long_description = fd.read()

setup(
    **data,
    long_description=long_description,
    packages=["revealjs"],
    py_modules=["revealjs.reveal_js", "revealjs.interface"],
    data_files=[("revealjs", ["revealjs/slide.adoc"])],
    entry_points={
        "console_scripts": ["reveal_js = revealjs.reveal_js:main"],
    },
    install_requires=[i.strip() for i in open("requirements.txt").readlines()],
)
