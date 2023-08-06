# setup.py

from setuptools import setup, find_packages

setup(
    name='global_tonemapping',
    version='0.1.201',
    url='https://github.com/Elessar11777',
    author='Elessar11777',
    author_email='Elessar11777@gmail.com',
    description='Petri Global Tonemapping Package',
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "opencv-python>=4.5.3"
    ],
)
