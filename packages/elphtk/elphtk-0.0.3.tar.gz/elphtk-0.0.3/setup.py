#!/usr/bin/env python


#===========================================================================#
#                                                                           #
#  File:       setup.py                                                     #
#  Usage:      install the files as a lib and generate excutables           #      
#  Author:     Shunhong Zhang <szhang2@ustc.edu.cn>                         #
#  Date:       Jun 04, 2023                                                 #
#                                                                           #
#===========================================================================#


import glob
import os
import sys
import platform
from distutils.core import setup
#from setuptools import setup


def test_modules(module_list,desc,pkg='asd'):
    import importlib
    import glob
    import shutil
    print ( '\n{0}\nTEST: {1}\n{0}'.format('='*50,desc))
    print ( '{0:40s} {1:10s}\n{2}'.format('MODULE','STATUS','-'*50))
    for mod in module_list:
        if '__init__' in mod: continue
        try:
            mod = mod.replace('/','.')
            importlib.import_module(mod)
            print('{0:40s} success'.format(mod))
        except:
            print('{0:40s} failed!'.format(mod))
    print('{0}\n'.format('='*50))
    for item in glob.glob('*pyc'): os.remove(item)
    if os.path.isdir('__pycache__'): shutil.rmtree('__pycache__')



def write_code_info(kwargs_setup):
    with open('elphtk/__init__.py','w') as fw:
        for key in ['__name__','__version__','__author__','__author_email__','__url__','__license__','__platforms__']:
            print ('{:<20s}  =  "{}"'.format(key,kwargs_setup[key.strip('__')]),file=fw)



core_modules=[
'arguments',
'epw_binary',
'epw_tool',
'wgauss',
'qe_phonon',
'phonopy_phonon',
'phonon_plot',
'pkg_info',
'__init__',
]

core_modules = ['elphtk/{}'.format(item) for item in core_modules]
scripts_pysupercell = glob.glob('scripts/*')

long_desc="An open-source Python library for phonon-related data processing"


kwargs_setup=dict(
name='elphtk',
version='0.0.3',
author='Shunhong Zhang',
author_email='zhangshunhong.pku@gmail.com',
url='https://pypi.org/project/elphtk',
download_url='https://pypi.org/project/elphtk',
keywords=['Python','Phonon','Electron-phonon'],
py_modules=core_modules,
license="MIT License",
description='Python library for (electron)-phonon-related analysis',
long_description=long_desc,
platforms=[platform.system()],
)


if __name__=='__main__':
    #setup(**kwargs_setup)
    setup()
    write_code_info(kwargs_setup)
    test_modules(core_modules,'core modules')
