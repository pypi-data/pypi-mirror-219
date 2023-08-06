from setuptools import setup, find_packages

setup(
    name="niche_cv",
    version="0.0.2",
    url="https://github.com/Niche-Squad/niche_cv",
    author="James Chen",
    author_email="niche@vt.edu",
    description="The Computer Vision Library for Niche Squad",
    packages=find_packages(),
    install_requires=[],
    entry_points={"console_scripts": ["niche=niche_cv.show:main"]},
)
