from setuptools import setup

with open("README.md", "r") as fd:
    long_description = fd.read()

setup(
    name="revealjs",
    version="0.0.1",
    description="Reveal.js Presentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="guna",
    author_email="gunag5127@gmail.com",
    url="https://github.com/gunaNeelamegam/revealjs-presentation.git",
    packages=["revealjs"],
    py_modules=["revealjs.reveal_js"],
    entry_points={
        "console_scripts": ["reveal_js = revealjs.reveal_js:main"],
    },
    install_requires=[i.strip() for i in open("requirements.txt").readlines()],
)
