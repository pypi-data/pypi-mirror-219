#import setuptools
from setuptools import setup, find_packages, Distribution
from os import path

HERE = path.abspath(path.dirname(__file__))

class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""
    def has_ext_modules(foo):
        return True
    
setup(
    name = 'openHySim', 
    version = '0.0.1',
    description = 'OpenSees and OpenFresco combined together',
    author = 'Ning Li',
    author_email = 'neallee@tju.edu.cn',
    url = 'http://github.com/nealleehit/osfeo',
    #packages_dir = {'openhytestpip':'openHySim'},
    packages = find_packages(exclude=['contrib','docs','tests']),
    classifiers = ["Programming Language :: Python :: 3",
                    "License :: OSI Approved :: MIT License",
                    "Operating System :: Microsoft :: Windows",],
    include_package_data=True,
    package_data={'openHySim':['libcrypto-3-x64.dll', 
                               'libssl-3-x64.dll',
                               'ntpciscr64.dll',
                               'opensees.pyd',
                               'Pnpscr64.dll',
                               'xpcapi.dll',]},
    install_requires = ['numpy'], #get_requirements(),
    distclass=BinaryDistribution,
)