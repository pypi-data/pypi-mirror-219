
from setuptools import setup, find_packages

setup(
    name='vimoweb_Summarizer',
    version='1.0.0',
    author='vimoweb',
    author_email='vimocodes@gmail.com',
    description='Summary Generator Library',
    packages=find_packages(),
    install_requires=[
        'spacy',
    ],
)
