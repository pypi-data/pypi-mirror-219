from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="niche_cv",
    version="0.0.10",
    url="https://github.com/Niche-Squad/niche_cv",
    author="James Chen",
    author_email="niche@vt.edu",
    description="The Computer Vision Library for Niche Squad",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    entry_points={"console_scripts": ["niche=niche_cv.show:main"]},
)
