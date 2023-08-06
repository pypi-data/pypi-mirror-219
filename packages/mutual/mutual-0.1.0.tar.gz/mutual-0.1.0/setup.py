from setuptools import setup, find_packages

setup(
    name='mutual',
    version='0.1.0',  # beta
    description='A Python client for the Mutual API.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Alex Betita', # placeholder for now
    author_email='alexbetita25@gmail.com', # placeholder for now
    url='https://github.com/Mutu-AI',  # if you have a github repo for the package
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
