# elphtk
A Python library for phonon and electron-phonon related properties analysis

## Code introduction

This is a python package for pre- and post-processing of phonon and electron-phonon-coupling calculations

Copyright Shunhong Zhang 2023

zhangshunhong.pku@gmail.com


## Code citation

If you usage of this code lead to some publications, we request that you kindly cite it like

Shunhong Zhang, elphtk: a python library for electron-phonon-related properties analysis (2023)


## Code distributions

* arguments: some arguments for command line
* elphtk: the core lib
* sciprts: some executables


## Installation
* Fast installation via pypi
pip install elphtk


* Install manually from tarball 
1. Download the zip or tarball (tar.gz) of the package
2. unzip the package
3. Run one of the two following command
   python setup.py install --home=.
   python setup.py install --user

* To check whether you have successfully install the package, go to the python interactive shell
 
import elphtk

  If everything runs smoothly, the installation should be done. 
  Contact the author if you come across any problem.

## Clean installation
./clean

This operation removes "build" and "dists" directories generated upon compilation
and results in the examples directory, including dat and ovf files, and figures in png


## Usage

* Use pysuerpcell as an API

    The major functions are collected in elphtk library, to use it in your python script, use

    import elphtk


* Use elphtk as an executable (python script)

    check the "scripts" directory to see available scripts


## Additional Notes

Note: This is a .md file in Markdown, to have a better view on the contants

we suggest you to install mdview, a free software for viewing .md files

In Ubuntu, run the following commands to install it

sudo atp update

sudo apt install snapd

sudo snap install mdview

