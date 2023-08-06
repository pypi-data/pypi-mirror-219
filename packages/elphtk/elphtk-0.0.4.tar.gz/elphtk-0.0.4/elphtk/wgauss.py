#!/usr/bin/env python

#====================================================================================
#
# smearing step functions and its derivatives
# e.g. Fermi function
# adapted from the fortran source code of
# Quantum ESPRESSO
# Ref:
# http://www.hector.ac.uk/cse/distributedcse/reports/conquest/conquest/node6.html
#
# Author: Shunhong Zhang
# Email: szhang2@ustc.edu.cn'
# Date: Mar 06, 2020
#
#=====================================================================================


import numpy as np
from scipy.special import erf,erfc

r2=np.sqrt(2.)
sqrtpm1=1./np.sqrt(np.pi)

def gauss_freq(x):
    return 0.5*erfc(-x/r2)

# Broadening of the step function (Fermi-Dirac like)
def wgauss(n,x,maxarg=200.):
    if n==-99:
        # Fermi-Dirac smearing
        if x<-maxarg: wgauss=0.
        elif x>maxarg: wgauss=1.
        else: wgauss= 1./(1.+np.exp(-x))
    elif n==-1:
        # cold smearing  (Marzari-Vanderbilt)
        xp = x - 1./r2
        arg=min(maxarg,xp**2)
        wgauss=0.5*erf(xp)+1./np.sqrt(2.*np.pi)*np.exp(-arg)+0.5
    elif 0<=n<=10:
        # Methfessel-Paxton
        arg=min(200., x**2)
        wgauss = gauss_freq(x*r2)
        if (n==0): return wgauss
        hd=0.
        arg=min(maxarg,x**2)
        hp=np.exp(-arg)
        ni=0
        a=sqrtpm1
        for i in range(1,n+1):
            hd = 2.*x*hp - 2.*float(ni)*hd
            ni +=1
            a = -a/float(i)/4.
            wgauss += a*hd
            hp = 2.*x*hd-2.*float(ni)*hp
            ni +=1
    elif n>10 or n<0:
        exit('''Methfessel-Paxton smearing in order of {0}: 
        higher order smearing is untested and unstable'''.format(n))
    return wgauss


# Broadening of the delta function
def w0gauss(n,x):
    if n==-99:
        # Fermi-Dirac smearing
        if abs(x)<=36.: w0gauss= 1./(2.+np.exp(-x)+np.exp(x))
        else: w0gauss = 0.
    elif n==-1:
        # cold smearing  (Marzari-Vanderbilt)
        arg=min(200.0,(x-1./r2)**2)
        w0gauss=sqrtpm1*np.exp(-arg)*(2.-r2*x)
    elif 0<=n<=10:
        # Methfessel-Paxton
        arg=min(200., x**2)
        w0gauss = np.exp(-arg) * sqrtpm1
        if (n==0): return w0gauss
        hd=0.
        hp=np.exp(-arg)
        ni=0.
        a=sqrtpm1
        for i in range(1,n+1):
            hd = 2.*x*hp - 2.*ni*hd
            ni +=1
            a = -a/float(i)/4.
            hp = 2.*x*hd-2.*ni*hp
            ni += 1.
            w0gauss += a*hp
    elif n>10 or n<0:
        exit('''Methfessel-Paxton smearing in order of {0}: 
        higher order smearing is untested and unstable'''.format(n))
    return w0gauss


def test_wgauss():
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(1,1,figsize=(8,8))
    xx=np.linspace(-10,10,401)
    n=-99
    yy=[wgauss(n,ix) for ix in xx]
    ax.plot(xx,yy,label='$\mathrm{Fermi-Dirac}$')
    n=-1
    yy=[wgauss(n,ix) for ix in xx]
    ax.plot(xx,yy,label='$\mathrm{cold\ (Marzari-Vanderbilt)}$')

    for n in range(5):
        yy=[wgauss(n,ix) for ix in xx]
        ax.plot(xx,yy,label='$\mathrm{Methfessel-Paxton, n=}$'+'{0}'.format(n))

    ax.legend(loc='upper left',fontsize=12)
    ax.set_title('Smearing step function')
    ax.set_ylim(-0.2,1.6)
    plt.show()


def test_w0gauss():
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(1,1,figsize=(8,8))
    xx=np.linspace(-10,10,401)
    n=-99
    yy=[w0gauss(n,ix) for ix in xx]
    ax.plot(xx,yy,label='$\mathrm{Fermi-Dirac}$')
    n=-1
    yy=[w0gauss(n,ix) for ix in xx]
    ax.plot(xx,yy,label='$\mathrm{cold\ (Marzari-Vanderbilt)}$')
    
    for n in range(5):
        yy=[w0gauss(n,ix) for ix in xx]
        ax.plot(xx,yy,label='$\mathrm{Methfessel-Paxton, n=}$'+'{0}'.format(n))

    ax.legend(loc='upper left',fontsize=12)
    ax.set_title('Smearing delta functions')
    ax.set_ylim(-0.2,1.6)
    plt.show()


def main():
    test_wgauss() 
    test_w0gauss()


if __name__=='__main__':
    main()
    
