import os
from setuptools import setup, find_packages

cur_dir = os.path.realpath(os.path.dirname(__file__))

setup(
    name='IMaSynData',
    packages=find_packages(),
    version='0.2.0',
    author='Synthesis Project Team',
    author_email='olgakononova@lbl.gov',
    description='Web app for data mining of synthesis recipes',
    zip_safe=False,
    install_requires=open(os.path.join(cur_dir, './requirements.txt')).readlines(),
    include_package_data=True
)
