#!/usr/bin/env python
#===========================================================================#
#                                                                           #
#  File:       epw_tool.py                                                  #
#  Usage:      processing data from EPW for plot and analysis               #      
#  Author:     Shunhong Zhang <szhang2@ustc.edu.cn>                         #
#  Date:       Sep 28, 2019                                                 #
#                                                                           #
#===========================================================================#


import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import itertools
import collections
import phonopy.units as units
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}' #for \text command


def get_qf_from_out(filout='epw.out'):
    get_qf=os.popen('grep "iq =" {0}'.format(filout)).readlines()
    qf=np.array([item.split()[7:10] for item in get_qf],float)
    wq=np.array([item.split()[-1] for item in get_qf],float)
    return qf, wq


def get_kf_from_out(filout='epw.out'):
    get_kf=os.popen('grep "ik =" {0}'.format(filout)).readlines()
    kf=np.array([item.split()[4:] for item in get_kf],float)
    return kf


def plot_kgmap(args):
    print ('plot kgmap')
    get_qpts=os.popen('grep "q = " {0}.dyn*'.format(args.prefix)).readlines()
    get_qpts=[line.split('(')[1].split(')')[0].split() for line in get_qpts]
    qpts=[[float(item) for item in line] for line in get_qpts]
    qpts=np.array(qpts)
    print (qpts)
    fil='{0}.kgmap'.format(args.prefix)
    kmap=[]
    with open(fil) as f:
        while True:
            line=f.readline().split()
            if len(line)==2:  
                kmap.append([int(item) for item in line[0:2]])
            else: 
                nq=int(line[0])
                break
        kgmap=np.fromfile(f,count=nq*3,sep=' ',dtype=float).reshape(nq,3)
    fig=plt.figure(figsize=args.figsize)
    ax=fig.add_subplot(111)
    ax.scatter(qpts[:,0],qpts[:,1],s=20,facecolor='r',edgecolor='none')
    ax.scatter(kgmap[:,0],kgmap[:,1],s=10,facecolor='b',edgecolor='none')
    ax.set_aspect('equal')
    fig.tight_layout()
    fig.savefig('kgmap',dpi=args.dpi)
    if args.show_plot: plt.show()
    return fig


def plot_specfun(args):
    print ('plot spectral function')
    fil='specfun.elself'
    nlne=500
    data=[]
    int_spec=[]
    with open(fil) as f:
        for i in range(6): f.readline()
        nkpt=int(os.popen('grep -c Integrated {0}'.format(fil)).read().split()[0])
        for ikpt in range(nkpt):
            data.append(np.fromfile(f,count=nlne*3,sep=' ',dtype=float).reshape(nlne,3))
            int_spec.append(float(f.readline().split()[-1]))
    data=np.array(data)
    data=np.transpose(data,(1,0,2))
    print ('data shape',data.shape)
    fig=plt.figure(figsize=args.figsize)
    ax=fig.add_subplot(212)
    my_extent=[1,nkpt,np.min(data[:,:,1]),np.max(data[:,:,1])]
    im=ax.imshow(data[:,:,2],extent=my_extent,cmap='viridis',aspect='auto',origin='lower')
    ax.set_ylim(-1,1)
    #cbaxes = fig.add_axes([1.1, 0.1, 0.03, 0.8]) 
    fig.colorbar(im,ticks=[0,0.02,0.04],orientation='horizontal')
    ax.axhline(0,c='w',ls='--',alpha=0.8)
    ax.set_xlim(1,nkpt)
    ax.set_ylabel('$\omega$ (eV)')
    ax=fig.add_subplot(211)
    ax.plot(np.arange(201),int_spec,'r-')
    ax.set_yticks(np.arange(5))
    ax.set_ylabel('electron linewidth (meV)')
    fig.tight_layout()
    fig.savefig('specfun',dpi=args.dpi)
    if args.show_plot: plt.show()
    return fig


def plot_specfun_sup(args):
    print ('plot spectral function')
    fil='specfun_sup.elself'
    nlne=500
    f=open(fil)
    for i in range(6): f.readline()
    data=np.loadtxt(f)
    nlne=data.shape[0]
    nkpt=len(set(data[:,0]))
    nband=len(set(data[:,1]))
    ne=500
    data=data.reshape(nband,nkpt,500,6)
    data=np.transpose(data,(0,2,1,3))
    fig=plt.figure(figsize=args.figsize)
    for iband in range(nband):
        ax=fig.add_subplot(1,nband,iband+1)
        my_extent=[1,nkpt,np.min(data[iband,:,:,3]),np.max(data[iband,:,:,3])]
        im=ax.imshow(data[iband,:,:,4],extent=my_extent,cmap='viridis',aspect='auto',origin='lower')
        ax.axhline(0,c='w',ls='--',alpha=0.8)
        ax.set_xlim(1,nkpt)
        if iband==0: ax.set_ylabel('$\omega$ (eV)')
    fig.colorbar(im)
    fig.tight_layout()
    fig.savefig('specfun_sup',dpi=args.dpi)
    if args.show_plot: plt.show()
    return fig


def plot_phself(args):
    print ('plot phonon self-energy')
    fil='linewidth.phself'
    with open(fil) as f:
        f.readline()
        data=np.loadtxt(f)
    subsets=set(data[:,1])
    print ('subsets:',subsets)
    print ('no. of branches: {0:2d}'.format(len(subsets)))
    print ('max linewidth: {0}'.format(np.max(data[:,-1])))
    print ('min linewidth: {0}'.format(np.min(data[:,-1])))
    if np.where(data[:,3]<0):
        print ('\nWarning: the linewidth for the following data points are negative!')
        for idx in np.where(data[:,3]<0)[0]:
            print ('{0:4.0f} {1:4.0f} {2:12.6f} {3:12.6f}'.format(data[idx,0],data[idx,1],data[idx,2],data[idx,3]))
        print ('\nThey are adjusted to zero during plotting\n')
        data[np.where(data[:,3]<0)[0],3]=0

    qf,wq=get_qf_from_out()

    fig,ax=plt.subplots(1,1,figsize=args.figsize)
    if args.kmode=='band':
        for isub in subsets:
            idx=np.where(data[:,1]==isub)[0]
            ax.plot(data[idx,0],data[idx,2],'g-',alpha=0.5)
        size=500
        ax.scatter(data[:,0],data[:,2],s=size*data[:,3],facecolor='r',edgecolor='none')
        ax.set_xlim(np.min(data[:,0]),np.max(data[:,0]))
        ax.axhline(0,c='gray',ls='--',alpha=0.5)
        ax.set_ylabel('$\omega$ (meV)')
        ax.set_ylim(0,30)
    elif args.kmode=='mesh':
        nmode=len(subsets)
        nkpt=data.shape[0]/nmode
        data=data.reshape(nkpt,nmode,data.shape[-1])
        if args.sum_modes: fc=np.sum(data[:,:,-1],axis=1)
        else: fc=data[:,args.imode,-1]
        cax=ax.scatter(qf[:,0],qf[:,1],s=args.markersize,facecolor=fc,edgecolor='none')
        cbar=fig.colorbar(cax)
        ax.set_aspect('equal')
    fig.tight_layout()
    figname = '{}_linewidth'.format(args.task)
    fig.savefig(figname,dpi=args.dpi)
    if args.show_plot: plt.show()
    return fig


def plot_elself(args):
    print ('plot electron self-energy')
    fil='linewidth.elself'
    with open(fil) as f:
        f.readline()
        data=np.loadtxt(f)
    bands=set(data[:,1])
    modes=set(data[:,-2])
    nbnd=len(bands)
    nmode=len(modes)
    print ('no. of bands: {0:3d}'.format(nbnd))
    print ('no. of branches: {0:2d}'.format(nmode))
    print ('max linewidth: {0}'.format(np.max(data[:,-1])))
    print ('min linewidth: {0}'.format(np.min(data[:,-1])))
    if np.where(data[:,3]<0):
        print ('\nWarning: the linewidth for the following data points are negative!')
        for idx in np.where(data[:,3]<0)[0]:
            print ('{0:4.0f} {1:4.0f} {2:12.6f} {3:12.6f}'.format(data[idx,0],data[idx,1],data[idx,2],data[idx,3]))
        print ('\nThey are adjusted to zero during plotting\n')
        data[np.where(data[:,3]<0)[0],3]=0

    kf=get_kf_from_out()

    fig,ax=plt.subplots(1,1,figsize=args.figsize)
    if args.kmode=='band':
        for isub in subsets:
            idx=np.where(data[:,1]==isub)[0]
            ax.plot(data[idx,0],data[idx,2],'g-',alpha=0.5)
        size=500
        ax.scatter(data[:,0],data[:,2],s=size*data[:,3],facecolor='r',edgecolor='none')
        ax.set_xlim(np.min(data[:,0]),np.max(data[:,0]))
        ax.axhline(0,c='gray',ls='--',alpha=0.5)
        ax.set_ylabel('$\omega$ (meV)')
        ax.set_ylim(0,30)
    elif args.kmode=='mesh':
        nkpt=data.shape[0]/nmode/nbnd
        data=data.reshape(nkpt,nbnd,nmode,data.shape[-1])
        if args.sum_modes: fc=np.sum(data[:,:,:,-1],axis=(1,2))
        else: fc=data[:,args.iband,args.imode,-1]
        cax=ax.scatter(kf[:,0],kf[:,1],s=args.markersize,facecolor=fc,edgecolor='none')
        cbar=fig.colorbar(cax)
        ax.set_aspect('equal')
    fig.tight_layout()
    figname = '{0}_linewidth'.format(args.task)
    fig.savefig(figname,dpi=args.dpi)
    if args.show_plot: plt.show()
    return fig


def plot_lambda_phself():
    print ('plot lambda phonon self-energy')
    print ('under development')


def plot_fermi_surface(args):
    print ('plot fermi surface')
    efermi=float(os.popen('grep Ef epw.out|grep "fine k-mesh"').read().split()[-2])
    fil='linewidth.elself'
    with open(fil) as f:
        f.readline()
        data=np.loadtxt(f)
    bands=set(data[:,1])
    modes=set(data[:,-2])
    nbnd=len(bands)
    nmode=len(modes)
    kf=get_kf_from_out()
    nkpt=len(kf)
    print ('Fermi energy read from fine k-mesh: {:10.5f} eV'.format(efermi))
    print ('No. of bands: {0:3d}'.format(nbnd))
    print ('No. of branches: {0:2d}'.format(nmode))
    print ('No. of kpts: {0:6d}'.format(nkpt))
    data=data.reshape(nkpt,nbnd,nmode,data.shape[-1])
    evals=data[:,:,0,-1]-efermi
    #abs_evals=np.abs(evals)
    #ibnd = [(np.where(abs_evals[ik]==np.min(abs_evals[ik]))[0]) for ik in range(nkpt)]
    #print (ibnd[:40])
    for ibnd in range(nbnd):
        fc=evals[:,ibnd]
        fig,ax=plt.subplots(1,1,figsize=args.figsize)
        cax=ax.scatter(kf[:,0],kf[:,1],s=args.markersize,facecolor=fc,edgecolor='none',vmin=-1,vmax=1,cmap='bwr')
        cbar=fig.colorbar(cax)
        ax.set_aspect('equal')
        fig.tight_layout()
        figname = 'fermi_surface_bnd_{}'.format(ibnd)
        fig.savefig(figname,dpi=args.dpi)
    if args.show_plot: plt.show()
    return fig


def get_smearing(prefix):
    get_lines=os.popen("grep -A 1 smearing {0}.a2f".format(prefix)).readlines()
    ph_smearing=np.array([float(item) for item in get_lines[1].split()[1:]])
    el_smearing=float(get_lines[2].split()[-1])
    return ph_smearing,el_smearing


def plot_phmesh(args,ikz=0):
    import spcd
    qpts,freqs=spcd.read_freq(seedname=args.prefix)
    freq=freqs[:,args.imode]
    freq_THz=freq*units.Rydberg/units.THzToEv
    print ('\nfrequencies range for mode {0}'.format(args.imode))
    print ('[{:12.7f}, {:12.7f}] eV'.format(np.min(freq),np.max(freq)))
    print ('[{:12.7f}, {:12.7f}] THz'.format(np.min(freq_THz),np.max(freq_THz)))
    print ('')
    cx=collections.Counter(qpts[:,0])
    cy=collections.Counter(qpts[:,1])
    cz=collections.Counter(qpts[:,2])
    print ('Plotting phmesh in kz={:8.3f} plane'.format(qpts[ikz,2]))
    #plot_data=data[:,iband].reshape(nqx,nqy,nqz)[:,:,ikz].T
    fig=plt.figure(figsize=args.figsize)
    ax=fig.add_subplot(111)
    #my_extent=[0,1,0,1] # need refinement
    #im = ax.imshow(plot_data,extent=my_extent,cmap='viridis',origin='lower')
    im=ax.scatter(qpts[:,0],qpts[:,1],s=30,facecolor=freq_THz,edgecolor='none',cmap='viridis')
    ax.set_xticks([])
    ax.set_xlabel('$k_x$')
    ax.set_ylabel('$k_y$')
    ax.set_aspect('equal')
    cbar = fig.colorbar(im)
    cbar.ax.set_title('$\omega\ \mathrm{(THz)}$')
    fig.tight_layout()
    figna,e = 'phmesh_{}'.format(args.imode)
    fig.savefig(figname,dpi=args.dpi)
    if args.show_plot: plt.show()
    return fig 


def plot_phband(args):
    print ('plot phonon band')
    fil='{}.freq'.format(args.prefix)
    with open(fil) as f:
        line=f.readline().split()
        nband=int(line[2].rstrip(','))
        nkpt=int(line[4])
        data=[]
        for ikpt in range(nkpt):
            line=f.readline()
            data.append(np.fromfile(f,count=nband,sep=' ',dtype=float))
    data=np.array(data)
    fig=plt.figure(figsize=args.figsize)
    ax=fig.add_subplot(111)
    for iband in range(nband): ax.plot(np.arange(nkpt),data[:,iband],'g-')
    ax.set_xlim(0,nkpt)
    ax.set_xticks([])
    ax.set_ylabel('$\omega$ ($meV$)')
    fig.tight_layout()
    fig.savefig('phband',dpi=args.dpi)
    if args.show_plot: plt.show()
    return fig


def plot_phdos(args):
    print ('plot phonon density of states')
    try: 
        ph_smearing,el_smearing=get_smearing(args.prefix)
        print ('ph smearing: {0} meV'.format(ph_smearing[args.ismear]))
    except: pass
    fil='{0}.phdos'.format(args.prefix)
    data=np.loadtxt(open(fil))
    freq=data[:,0]
    phdos=data[:,1:]
    fig=plt.figure(figsize=args.figsize)
    ax=fig.add_subplot(111)
    ax.set_xlabel('$\omega$ ($meV$)')
    ax.set_ylabel('$phdos$ ($\omega^{-1}$)')
    ax.plot(freq,phdos[:,args.ismear],'g-')
    ax.set_xlim(freq[0],freq[-1])
    fig.tight_layout()
    figname = '{}_phdos'.format(args.prefix)
    fig.savefig(figname,dpi=args.dpi)
    if args.show_plot: plt.show()
    return fig
    

def plot_lambda_FS(args):
    with open('{}.lambda_FS'.format(args.seedname)) as f:
        f.readline()
        data=np.loadtxt(f)
    kpt=data[:,:3]
    band_idx=data[:,3]
    band_en=data[:,4]
    count_band = collections.Counter(band_idx)
    nkpt = count_band[1.]
    nband = int(np.max([key for (key,value) in count_band.items()]))
    print ('no. of  k-points in Fermi shell = {:5d}'.format(nkpt))
    print ('max no. of bands in Fermi shell = {:5d}'.format(nband))
    band_lambda=np.zeros((nband,nkpt),float)
    kpt_fs=np.zeros((nkpt,3),float)
    ikpt=-1
    iband=0
    for ii in range(data.shape[0]):
        if band_idx[ii]==1: 
            ikpt+=1
            iband=0
            kpt_fs[ikpt]=kpt[ii]
        band_lambda[iband,ikpt]=data[ii,5]
        iband+=1
        ii+=1
    lambda_all=np.sum(band_lambda,axis=0)
    if args.sum_modes:
        fig=plt.figure(figsize=(6,4))
        ax=fig.add_subplot(111)
        fig.subplots_adjust(right=0.8)
        cb=ax.scatter(kpt_fs[:,0],kpt_fs[:,1],s=args.markersize,c=lambda_all,cmap='rainbow')
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.1, 0.03, 0.7])
        fig.colorbar(cb,cax=cbar_ax)
        ax.set_aspect('equal')
        fig.savefig('lambda_all',dpi=args.dpi)
        if args.show_plot: plt.show()
        return fig

    for ib in range(nband):
        fig=plt.figure(figsize=(6,4))
        ax=fig.add_subplot(111)
        #subset=np.where(band_idx==idx+1)[0]
        if args.mesh_style=='interp':
            #colors=np.zeros((len(ky),len(kx)),float)
            for (ix,iy) in itertools.product(range(len(kx)),range(len(ky))):
                for ik in subset:
                    if kpt[ik,0]==kx_grid[iy,ix] and kpt[ik,1]==ky_grid[iy,ix]: colors[iy,ix]=band_lambda[ik]
            my_extent=[min(kx),max(kx),min(ky),max(ky)]
            cb=ax.imshow(colors,extent=my_extent,cmap='rainbow',vmin=0,vmax=np.max(band_lambda),origin='lower')
        elif args.mesh_style=='dot':
            cb=ax.scatter(kpt_fs[:,0],kpt_fs[:,1],facecolor=band_lambda[ib],edgecolor='none',cmap='rainbow',vmin=0,vmax=np.max(band_lambda),s=15)
        else: exit('Allowed mesh_style are: interp, dot')

        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        margin_x=(np.max(kpt[:,0])-np.min(kpt[:,0]))*0.0
        margin_y=(np.max(kpt[:,1])-np.min(kpt[:,1]))*0.0
        ax.set_xlim(np.min(kpt[:,0])-margin_x,np.max(kpt[:,0])+margin_y)
        ax.set_ylim(np.min(kpt[:,1])-margin_y,np.max(kpt[:,1])+margin_y)
        ax.set_xlabel('$k_x$')
        ax.set_title('band {0}'.format(ib+1))
        ax.set_ylabel('$k_y$')
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.1, 0.03, 0.7])
        fig.colorbar(cb,cax=cbar_ax)
        figname = 'lambda_band_{}_{}'.format(args.mesh_style,ib)
        fig.savefig(figname,dpi=args.dpi)
    if args.show_plot: plt.show()
    return fig
     

def read_a2f(args,iso=False):
    ncol=11
    nrow=500
    fil='{}.a2f.01'.format(args.prefix)
    if iso: fil='{}_iso'.format(fil)
    print ('Reading data from {}'.format(fil))
    f=open(fil,'r')
    data=np.fromfile(f,count=ncol*nrow,dtype=float,sep=' ')
    data = data.reshape(nrow,ncol)
    freq=data[:,0]
    a2f=data[:,1:]
    print ('a2f shape:',a2f.shape)
    # times 2 to include the spin degeneracy, for spin case please double check it
    cum_epc=np.array([np.trapz(a2f[:iw,args.ismear]/freq[:iw],x=freq[:iw]) for iw in range(nrow)])*2
    print ('integrated el-ph strength:{0:10.7f}'.format(cum_epc[-1]))

    if iso==True:
        line=f.readline().split()
        int_epc=float(line[2])
        sum_epc=float(line[-1])
    else:
        f.readline() 
        int_epc=np.array([float(item) for item in f.readline().split()[1:]])
        [f.readline() for i in range(3)]
        fermi_win=float(f.readline().split()[-1])
        sum_epc=float(f.readline().split()[-1])
    return freq,a2f,cum_epc,int_epc,sum_epc


def plot_a2f(args):
    print ('Plotting Eliashberg spectral function')
    data=read_a2f(args,args.iso)
    freq=data[0]
    a2f=data[1]
    cum_epc=data[2]
    fig=plt.figure(figsize=args.figsize)
    ax=fig.add_subplot(111)
    ax.set_xlabel('$\omega$ ($meV$)')
    if args.freq_unit=='cm-1':
        print ('transfer unit of frequency to cm-1')
        freq=freq*1e-3/units.THzToEv*units.THzToCm
        ax.set_xlabel('$\omega$ ($cm^{-1}$)')
    ax.set_ylabel('$\\alpha^2F$ ($\omega$), $\lambda$ ($\omega$)')
    ax.plot(freq,a2f[:,args.ismear],'g-',label='$\\alpha^2F$ ($\omega$)')
    ax.set_xlim(freq[0],freq[-1])
    ax.plot(freq,cum_epc,'r--',label='$\lambda$ ($\omega$)')
    ax.legend(fontsize=12)
    if args.max_freq>0: ax.set_xlim(0,args.max_freq)
    fig.tight_layout()
    if args.iso: 
       iso='iso'
    else: 
       iso='aniso'
       ph_smearing,el_smearing=get_smearing(args.prefix)
       print ('Phononic smearing:{:8.5f}'.format(ph_smearing[args.ismear]))
    figname = '{}_a2f_{}_{}'.format(args.prefix,iso,args.ismear)
    fig.savefig(figname,dpi=args.dpi)
    if args.show_plot: plt.show()
    return fig


def plot_gap(args):
    print ('plot superconducting gap')
    fil_head='{0}.{1}_aniso_gap0_'.format(args.prefix,args.gtype)
    fils=[fil.rstrip('\n') for fil in os.popen('ls {0}*'.format(fil_head)).readlines()]
    fig=plt.figure(figsize=args.figsize)
    ax=fig.add_subplot(111)
    for fil in fils:
        temp=float(fil.split('_')[-1])
        print ('temp ={0:6.3f} K, file = {1}'.format(temp,fil))
        nskip={'imag':1,'pade':0}
        data=np.loadtxt(open(fil),skiprows=nskip[args.gtype])
        ax.plot(data[:,0],data[:,1]*1e3,'b-')
        ax.axvline(temp,c='b',alpha=0.8)
    ax.set_xlabel('$T\ \mathrm{(K)}$')
    ax.set_ylabel('$\Delta_{n\\bf{k}}(\omega=0) \mathrm{(meV)}$')
    fig.tight_layout()
    figname = '{}_gap_{}'.format(args.prefix,args.gtype)
    fig.savefig(figname,dpi=args.dpi)
    if args.show_plot: plt.show()
    return fig


def plot_qpr(args):
    print ('plot quasiparticle renormalization')
    fil_head='{0}.*_aniso_'.format(args.prefix)
    fils=[fil.rstrip('\n') for fil in os.popen('ls {0}*'.format(fil_head)).readlines()]
    rm=[item for item in fils if 'gap' in item]
    for item in rm: fils.remove(item)
    colors=['r','g','b','violet']
    fig=plt.figure(figsize=args.figsize)
    ax1=fig.add_subplot(211)
    ax2=fig.add_subplot(212)
    for i,fil in enumerate(fils):
        temp=float(fil.split('_')[-1])
        with open(fil) as f:
            f.readline()
            data=np.loadtxt(f)
        if 'imag' in fil:
            ax1.scatter(data[:,0]*1e3,data[:,-2]*1e3,facecolor=colors[i],edgecolor='None',s=2,label='{0}K'.format(temp))
        else:
            ax2.scatter(data[:,0]*1e3,data[:,-2]*1e3,facecolor=colors[i-len(fils)/2],edgecolor='None',s=2)
    ax1.legend(loc='upper right',scatterpoints=1,markerscale=3,prop={'size':args.legend_fontsize})
    ax1.set_xlim(0,200)
    ax2.set_xlim(0,200)
    ax1.set_ylim(-2,13)
    ax2.set_ylim(-20,33)
    ax2.set_xlabel('$\omega$ (meV)')
    ax1.set_ylabel('$\Delta_{n\\bf{k}}(i\omega)$ ($meV$)')
    ax2.set_ylabel('$\Delta_{n\\bf{k}}(\omega)$ ($meV$)')
    fig.tight_layout()
    fignmae = '{}_qp_renormalization'.format(args.prefix)
    fig.savefig(figname,dpi=args.dpi)
    if args.show_plot: plt.show()
    return fig


def plot_qdos(args):
    print ('plot quasiparticle dos')
    fil_head='{0}.qdos_'.format(args.prefix,args.gtype)
    fils=[fil.rstrip('\n') for fil in os.popen('ls {0}*'.format(fil_head)).readlines()]
    fig=plt.figure(figsize=args.figsize)
    ax=fig.add_subplot(111)
    colors=['r','g','b','violet']
    for i,fil in enumerate(fils):
        temp=float(fil.split('_')[-1])
        f=open(fil)
        f.readline()
        data=np.loadtxt(f)
        ax.plot(data[:,0]*1e3,data[:,1],c=colors[i],ls='-',label='T={0}'.format(temp))
    ax.set_xlabel('$\omega$ (meV)')
    ax.set_ylabel('$N_s (\omega) / N(\epsilon_F)$')
    ax.set_xlim(0,10)
    ax.legend(loc='upper left',ncol=2)
    ax.set_title('quasiparticle density of statres')
    fig.tight_layout()
    figname = '{0}_qdos'.format(args.prefix)
    fig.savefig(figname,dpi=args.dpi)
    if args.show_plot: plt.show()
    return fig


def plot_nest_fn(args):
    lines = os.popen('grep "Adimensional" epw.out').readlines()
    nest=np.array([float(line.split()[3]) for line in lines])
    print ('max value of nesting fn: {0}'.format(np.max(nest)))
    ndim=int(np.sqrt(nest.shape[0]))
    nest=nest.reshape(ndim,ndim)
    nest=np.vstack((nest,nest[:,0]))
    nest=np.vstack((nest.T,nest[:,0].T)).T
    fig=plt.figure()
    ax=fig.add_subplot(111)
    #cax=ax.scatter(qpts[:,0],qpts[:,1],s=20,facecolor=nest,edgecolor='none')
    #my_extent=[0,np.max(qpts[:,0]),0,np.max(qpts[:,1])]
    #print 'extent for plot: ', my_extent
    my_extent=[0,1,0,1]
    cax=ax.imshow(nest,extent=my_extent,origin='lower',cmap=args.cmap)
    ax.set_xlabel('$k_x (2\pi/a)$',fontsize=20)
    ax.set_ylabel('$k_y (2\pi/b)$',fontsize=20)
    fig.colorbar(cax)
    fig.savefig('nest')
    if args.show_plot: plt.show()
    return fig


def plot_wan_band(args):
    labels=None
    xsym=None
    #if os.path.isfile('{0}.win'.format(args.seedname)):
    #    get_labels=os.popen('grep -n kpoint_path {0}.win 2>/dev/null'.format(args.seedname)).readlines()
    #    if len(get_labels)>0:
    #        nseg=int(get_labels[1].split(':')[0])-int(get_labels[0].split(':')[0])
    #        get_labels=os.popen('grep -A {0} kpoint_path {1}.win 2>/dev/null'.format(nseg,args.seedname)).readlines()[1:nseg]
    #        labels=np.array([item.split()[0] for item in get_labels]+[get_labels[-1].split()[4]])
    if os.path.isfile('{0}_band.labelinfo.dat'.format(args.seedname)):
        lines=open('{0}_band.labelinfo.dat'.format(args.seedname)).readlines()
        #labels1=np.array([line.split()[0] for line in lines],dtype='S10')
        #labels2=np.array([line.split()[1] for line in lines],dtype='S10')
        #labels=labels1
        labels=np.array([line.split()[0] for line in lines])
        xsym=[int(line.split()[1])-1 for line in lines]
    data=np.loadtxt(open('{0}_band.dat'.format(args.seedname)))
    fig,ax=plt.subplots(1,1,figsize=args.figsize)
    ax.scatter(data[:,0],data[:,1],s=0.5,facecolor='r',edgecolor='r')
    ax.set_ylabel('$E (eV)$',fontsize=16)
    if xsym: 
        ax.set_xticks(data[xsym,0])
        for tick in ax.get_xticklines(): tick.set_visible(False)
        for xx in xsym: ax.axvline(data[xx,0],alpha=0.5,c='gray')
        if len(labels)>1:
            #idx=np.where(labels=='G')[0]
            #labels[idx]='\Gamma'
            ax.set_xticklabels(['${0}$'.format(item) for item in labels],fontsize=16)
        else: 
            ax.set_xticklabels([])
    else: ax.set_xticks([])
    ax.set_xlim(np.min(data[:,0]),np.max(data[:,0]))
    ax.axhline(args.wan_efermi,c='g',ls='--',lw=1,alpha=0.8,zorder=-1)
    ewin=np.max(data[:,1])-np.min(data[:,1])
    ax.set_ylim(np.min(data[:,1])-ewin*0.1,np.max(data[:,1])+ewin*0.1)
    if args.elim[1]>args.elim[0]: ax.set_ylim(args.elim)
    fig.tight_layout()
    fig.savefig('epw_wan_band',dpi=args.dpi)
    if args.show_plot: plt.show()
    return fig


def plot_gap_FS(args):
    fils=os.popen('ls *.imag_aniso_gap_FS*').readlines()
    nrow=int(round(sqrt(len(fils))))
    fig,ax=plt.subplots(nrow,len(fils)/nrow,figsize=args.figsize,sharex=True,sharey=True)
    for ifil,fil in enumerate(fils):
        j=ifil/nrow
        i=np.mod(ifil,nrow)
        data=np.loadtxt(open(fil.rstrip('\n')),skiprows=1)
        print ('gap range: {0:6.3f} to {1:6.3f} meV'.format(np.min(data[:,-1]*1e3),np.max(data[:,-1]*1e3)))
        sc=ax[i,j].scatter(data[:,0],data[:,1],s=10,facecolor=data[:,-1]*1e3,edgecolor='none',cmap=args.cmap)
        ax[i,j].set_aspect('equal')
        ax[i,j].set_xlim(0,1)
        ax[i,j].set_ylim(0,1)
        ax[i,j].set_xticks([0,1])
        ax[i,j].set_yticks([0,1])
        ax[i,j].set_title('$T =\ \mathrm{'+'{0:5.2f}'.format(float(fil.rstrip('\n').split('_')[-1]))+'}$',fontsize=10)
    fig.subplots_adjust(left=0.1,right=0.85)
    cbar_ax = fig.add_axes([0.9, 0.09, 0.02, 0.8])
    cbar=fig.colorbar(sc, cax=cbar_ax)
    cbar.ax.set_title('$\Delta\ \mathrm{(meV)}$')
    fig.savefig('gap_FS',dpi=args.dpi)
    if args.show_plot: plt.show()
    return fig


def plot_gap_freq(args):
    fils=os.popen('ls *.imag_aniso_0*').readlines()
    nrow=int(round(np.sqrt(len(fils))))
    fig,ax=plt.subplots(nrow,int(len(fils)/nrow),figsize=args.figsize,sharex=True,sharey=True)
    for ifil,fil in enumerate(fils):
        j=int(ifil/nrow)
        i=int(np.mod(ifil,nrow))
        data=np.loadtxt(open(fil.rstrip('\n')),skiprows=1)
        print ('gap range: {0:6.3f} to {1:6.3f} meV'.format(np.min(data[:,3]*1e3),np.max(data[:,3]*1e3)))
        ax[i,j].scatter(data[:,0]*1e3,data[:,3]*1e3,facecolor='g',edgecolor='none',s=2)
        ax[i,j].set_title('$T =\ \mathrm{'+'{0:5.2f}'.format(float(fil.rstrip('\n').split('_')[-1]))+'}$',fontsize=10)
        if i==ax.shape[0]-1:    ax[i,j].set_xlabel('$\omega\ \mathrm{(meV)}$')
        if j==0:    ax[i,j].set_ylabel('$\Delta\ \mathrm{(meV)}$')
    fig.tight_layout()
    fig.savefig('gap_freq',dpi=args.dpi)
    if args.show_plot: plt.show()
    return fig


def gen_xkff(nkf1,nkf2,nkf3):
    xx=np.linspace(0,1,nkf1,endpoint=False)
    yy=np.linspace(0,1,nkf2,endpoint=False)
    zz=np.linspace(0,1,nkf3,endpoint=False)
    y,z,x = np.meshgrid(yy,zz,xx)
    nkftot=np.prod([nkf1,nkf2,nkf3])
    xkff=np.array([x.T,y.T,z.T]).reshape(3,nkftot).T
    return xkff


def plot_nkfs(nkf1,nkf2,nkf3,ixkf,ekfs,show=False):
    # only works for 2D systems
    idx=np.where(ixkf!=0)[0]
    nkfs=len(idx)
    xkff=gen_xkff(nkf1,nkf2,nkf3)

    colors=['r','g','b','c','m','orange']
    nbnd=ekfs.shape[1]
    fig,ax=plt.subplots(1,nbnd,figsize=(4*nbnd,4))
    for i in range(ekfs.shape[1]):
        ax[i].scatter(xkff[idx][:,0],xkff[idx][:,1],s=30,facecolor=colors[i],edgecolor='none')
    fig.tight_layout()
    fig.savefig('nkfs',dpi=500)
    if show: plt.show()
    return fig
