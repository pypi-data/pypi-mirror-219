#!/usr/bin/env python


def verbose_pkg_info(version):
    try:
        from pyfiglet import Figlet
        pysc_text = Figlet().renderText('elphtk')
        print ('\n{}'.format(pysc_text))
    except:
        print ('\nRunning the script: {0}\n'.format(__file__.lstrip('./')))
    print ('{:>31s}'.format('version {}'.format(version)))
    print ('{:>31s}\n'.format('Copyright @ Shunhong Zhang 2023'))
