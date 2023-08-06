from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.3'
DESCRIPTION = 'A simple Notion db interface for Python'
requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Setting up
setup(
    name="NotionInterface",
    version=VERSION,
    author="LukaPedra (Lucca Rocha)",
    author_email="<lucca.v.rocha@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=requirements,
    keywords=['python', 'Notion', 'Database', 'page', 'Block', 'pandas'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)