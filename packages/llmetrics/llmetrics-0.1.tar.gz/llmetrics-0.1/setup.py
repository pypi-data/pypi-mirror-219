from setuptools import setup, find_packages

setup(
    name="llmetrics",
    version="0.1",
    description="A metrics and evaluation library for LLMs",
    author="Openlayer",
    author_email="engineers@openlayer.com",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'pandas',
        'rouge-score',
        'spacy',
        'nltk'
    ],
)