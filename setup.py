import os
from setuptools import setup

# Read the README file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "microImage",
    version = "1.0",
    author = "Vivien WALTER",
    author_email = "walter.vivien@gmail.com",
    description = ("Python3 module to open all common type of image used in microscopy."),
    license = "BSD",
    keywords = "microscopy image open",
    url = "https://github.com/vivien-walter/microImage",
    packages=['microImage'],
    long_description=read('README.md'),
    classifiers=[
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    python_requires='>=3.7',
    install_requires=[
        'numpy',
        'Pillow',
        'pims',
    ]
)
