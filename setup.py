import os

from setuptools import setup, find_packages

import twdown

this_directory = os.path.abspath(os.path.dirname(__file__))

# python setup.py sdist bdist_wheel && python -m twine upload dist/*
setup(
    name="twdown",
    version=twdown.__version__,
    keywords=["twdown", "twitter-video-downloader"],
    author="QIN2DIM",
    author_email="yaoqinse@gmail.com",
    url="https://github.com/QIN2DIM/twdown-api",
    license="MIT",
    description="Twitter video downloader",
    long_description=open(os.path.join(this_directory, "README.md")).read(),
    long_description_content_type="text/markdown",
    packages=find_packages(include=["twdown", "twdown.*", "LICENSE"]),
    install_requires=["requests~=2.28.1", "bs4~=0.0.1", "beautifulsoup4~=4.11.1"],
    python_requires=">=3.8",
    classifiers=[
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
)
