#!/usr/bin/env python


#==============================================
# Read binary files output by EPW
# Shunhong Zhang (USTC)
# szhang2@ustc.edu.cn
# Date: Aug 24, 2020
#==============================================


import phonopy.units as units
import glob
import numpy as np
import os
try: import fortio
except: raise ImportError('Fail to import fortio. Use "pip install fortio" to install it')

__author__='Shunhong Zhang'

__doc__='Read binary files output by EPW (v5.0.0)'

__note__='''
{0}\nmeaning of variables:
nkf1,   nkf2, nkf3: grid of fine k-mesh
nqf1,   nqf2, nqf3: grid of fine q-mesh
nkfs:   no. of k-points with eigenstates in Fermi shell
nqfs:   no. of q-points for each k-point, 
        where k+sgn*q is in the k-grid, nqfs[nkfs]
nqtotf: total no. of q-points for the fine q-mesh
nmodes: no. of phonon modes\n{0}
'''.format('-'*55)


def read_freq_scipy(outdir='./tmp',seedname='wannier90',prefix='wannier90'):
    from scipy.io import FortranFile
    fil_freq = '{}/{}.freq'.format(outdir,seedname)
    assert os.path.isfile(fil_freq), '{} not found!'.format(fil_freq)
    with FortranFile(fil_freq,'r') as f:
        nqtotf,nmodes = f.read_ints()
        qpts=np.zeros((nqtotf,3),float)
        wf=np.zeros((nqtotf,nmodes),float)
        for iq in range(nqtotf):
            qpts[iq]=f.read_reals(dtype=np.float)
            for imode in range(nmodes): wf[iq,imode]=f.read_reals(dtype=np.float)
    return qpts,wf*units.Rydberg


def read_freq(outdir='./tmp',seedname='wannier90',prefix='wannier90'):
    fil_freq = '{}/{}.freq'.format(outdir,seedname)
    assert os.path.isfile(fil_freq), '{} not found!'.format(fil_freq)
    with fortio.FortranFile(fil_freq) as f:
        nqtotf,nmodes=f.read_record('i4')
        qpts=np.zeros((nqtotf,3),float)
        wf=np.zeros((nqtotf,nmodes),float)
        for iq in range(nqtotf):
            qpts[iq]=f.read_record('f8',shape=3)
            for imode in range(nmodes): wf[iq,imode]=f.read_record('f8')
    print ('Freqs in units of eV')
    return qpts,wf*units.Rydberg


def write_freq(qpts,freqs,filfreqtxt='freq.txt'):
    data =np.concatenate((qpts,freqs),axis=1)
    np.savetxt(filfreqtxt,data,fmt='%10.5f')


def read_egnv(outdir='./tmp',seedname='wannier90'):
    with fortio.FortranFile('{0}/{1}.egnv'.format(outdir,seedname)) as f:
        nkftot,nkf1,nkf2,nkf3,nkfs=f.read_record('i4')
        recl=f.get_record_size()
        data=np.zeros(recl,dtype='byte')
        total=f._read_record_data(data)
        buffer_=bytearray(data[:4])
        nbnd_ = np.frombuffer(buffer_,dtype='i4')[0]
        buffer_=np.array([bytearray(data[i:i+8]) for i in range(4,total,8)])
        ef,ef0,dosef,degaussw,fsthick=np.frombuffer(buffer_,dtype='f8')
        wkfs=np.zeros(nkfs,float)
        xkfs=np.zeros((nkfs,3),float)
        ekf_=np.zeros((nkfs,nbnd_),float)
        for ik in range(nkfs):
            line=f.read_record('f8',shape=4)
            wkfs[ik]=line[0]
            xkfs[ik]=line[1:]
            for ibnd in range(nbnd_): ekf_[ik,ibnd]=f.read_record('f8')
    ekf_ *= units.Rydberg
    ef *= units.Rydberg
    ef0 *= units.Rydberg
    degaussw *= units.Rydberg
    fsthick *= units.Rydberg
    dosef /= units.Rydberg
    nbndfs=max([len(np.where(abs(ekf_[ik]-ef0)<fsthick)[0]) for ik in range(nkfs)])
    ekfs=np.ones((nkfs,nbndfs),float)*ef0-fsthick*10
    for ik in range(nkfs):
        idx=np.where(abs(ekf_[ik]-ef0)<fsthick)[0]
        ekfs[ik,:len(idx)]=ekf_[ik][idx]
    print ('ef  ={:15.8f} eV\nef0 ={:15.8f} eV'.format(ef,ef0))
    print ('min eigenval = {:10.5f}\nmax eigenval = {:10.5f} eV'.format(np.min(ekf_),np.max(ekf_)))
    grid_params = (nkftot,nkf1,nkf2,nkf3,nkfs,nbndfs)
    en_params = (ef,ef0,dosef,degaussw,fsthick)
    return grid_params,en_params,wkfs,xkfs,ekfs



def write_grid_params(grid_params,file=None):
    nkftot,nkf1,nkf2,nkf3,nkfs,nbndfs = grid_params
    print ('# nkftot = {:4d}'.format(nkftot),file=file)
    print ('# nkf1 = {:4d}'.format(nkf1),file=file)
    print ('# nkf2 = {:4d}'.format(nkf2),file=file)
    print ('# nkf3 = {:4d}'.format(nkf3),file=file)
    print ('# nkfs = {:4d}'.format(nkfs),file=file)
    print ('# nbndfs = {:4d}'.format(nbndfs),file=file)


def write_en_params(en_params,file=None):
    ef,ef0,dosef,degaussw,fsthick = en_params
    print ('# Ef = {:10.5f}'.format(ef),file=file)
    print ('# Ef0 = {:10.5f}'.format(ef0),file=file)
    print ('# DOS_Ef = {:10.5f}'.format(dosef),file=file)
    print ('# DeGaussW = {:10.5f}'.format(degaussw),file=file)
    print ('# FS_thick = {:10.5f}'.format(fsthick),file=file)
 

    
def gen_xkff(nkf1,nkf2,nkf3):
    xx=np.linspace(0,1,nkf1,endpoint=False)
    yy=np.linspace(0,1,nkf2,endpoint=False)
    zz=np.linspace(0,1,nkf3,endpoint=False)
    y,z,x = np.meshgrid(yy,zz,xx)
    nkftot=np.prod([nkf1,nkf2,nkf3])
    xkff=np.array([x.T,y.T,z.T]).reshape(3,nkftot).T
    return xkff


def read_ikmap(outdir='tmp',prefix='wannier90',seedname='wannier90'):
    with fortio.FortranFile('{0}/{1}.ikmap'.format(outdir,seedname)) as f:
        nkf_mesh=f.read_record('i4')
        nkf_mesh = int(nkf_mesh)
        ixkf=np.zeros(nkf_mesh,int)
        for ik in range(nkf_mesh):
            ixkf[ik]=f.read_record('i4')
    return ixkf


def read_nks(outdir='tmp',prefix='wannier90',seedname='wannier90'):
    get_ephmat = glob.glob('{}/{}.ephmat*'.format(outdir,seedname))
    npool = len(get_ephmat)
    nks=np.zeros(npool,int)
    for ipool in range(npool):
        with fortio.FortranFile('{0}/{1}.ephmat{2}'.format(outdir,seedname,ipool+1)) as f:
            pool_id,nks[ipool] = f.read_record('i4',shape=2)
    return nks


def calc_nnq(ixkqf):
    return np.array([len(np.where(ikk>0)[0]) for ikk in ixkqf])


def get_ephmat_lines(outdir='tmp',prefix='epw',seedname='ZrN',verbosity=0):
    get_ephmat = glob.glob('{}/{}.ephmat*'.format(outdir,seedname))
    npool = len(get_ephmat)
    if not npool: exit('cannot find {}/{}.ephmat'.format(outdir,seedname))
    nlines=np.zeros(npool,int)
    fmt = 'pool {:2d}, {:2d} ks, {:5d} records'
    for ipool in range(npool):
        with fortio.FortranFile('{}/{}.ephmat{}'.format(outdir,seedname,ipool+1)) as f:
            pool_id,nks_tmp = f.read_record('i4',shape=2)
            while True:
                try:    f.read_record('f8'); nlines[ipool]+=1
                except: break
        if verbosity: print (fmt.format(ipool+1,nks_tmp,nlines[ipool]))
    return nlines


def estimate_ephmat_lines(ipool,nqtotf,nks,nmodes,ekfs,ef0,fsthick,ixkqf,nlines):
    nnk=np.append(0,np.cumsum(nks))[ipool-1]
    nbndfs=ekfs.shape[1]
    eph_idx=[]
    nl=0
    for iq,ik in np.ndindex(nqtotf,nks[ipool-1]):
        if ixkqf[ik+nnk,iq]>0:  
            for ibnd,jbnd in np.ndindex(nbndfs,nbndfs):
                if (abs(ekfs[ik+nnk,ibnd]-ef0)<fsthick and abs(ekfs[ixkqf[ik+nnk,iq]-1,jbnd]-ef0)<fsthick):
                    nl+=nmodes
                    eph_idx.append([iq,ik,ibnd,jbnd])
    if nl!=nlines[ipool-1]: 
        exit('Err! pool {0:4d}, nl={1:5d}, nlines={2:5d}'.format(ipool,nl,nlines[ipool-1]))
    return nl, np.array(eph_idx)


def read_ephmat_one_pool(ipool,nks,ef0,fsthick,ekfs,ixkqf,nqfs,nbndfs,nnq,nlines,
    outdir='./tmp',seedname='wannier90',prefix='pw',eps_acustic=5.):
    # Note: esp_acustic in cm-1, should be converted into eV
    eps_acustic *= units.CmToEv

    qpts,wf = read_freq(outdir=outdir,seedname=seedname,prefix=prefix)
    nqtotf,nmodes=wf.shape
    nkfs=np.sum(nks)
    nnk=np.append(0,np.cumsum(nks))[ipool-1]
    nl, eph_idx = estimate_ephmat_lines(ipool,nqtotf,nks,nmodes,ekfs,ef0,fsthick,ixkqf,nlines)

    print ('ipool={:3d}, nks={:4d}, nnk={:4d} '.format(ipool,nks[ipool-1],nnk))
    g2 = np.zeros((nks[ipool-1],np.max(nqfs),nbndfs,nbndfs,nmodes),float)

    innq=np.zeros(nkfs,int)

    g2_= np.zeros((nks[ipool-1],np.max(nqfs),nbndfs,nbndfs,nmodes),float)
    with fortio.FortranFile('{}/{}.ephmat{}'.format(outdir,seedname,ipool)) as f:
        pool_id,nks_tmp = f.read_record('i4',shape=2)
        if nks_tmp!=nks[ipool-1]: exit('Inconsistency in nks (No. of kpts in pool)!')
        for iq,ik in np.ndindex(nqtotf,nks[ipool-1]):
            if ixkqf[ik+nnk,iq]>0: 
                innq[ik+nnk]+=1
                for imode in range(nmodes):
                    for ibnd,jbnd in np.ndindex(nbndfs,nbndfs):
                        if (abs(ekfs[ik+nnk,ibnd]-ef0)<fsthick and abs(ekfs[ixkqf[ik+nnk,iq]-1,jbnd]-ef0)<fsthick):
                            line=f.read_record('f8')
                            if wf[iq,imode]>=eps_acustic:
                                g2[ik,innq[ik+nnk]-1,ibnd,jbnd,imode]=line


    # These part need refinement
    '''
    with fortio.FortranFile('{0}/{1}.ephmat{2}'.format(outdir,prefix,ipool)) as f:
        pool_id,nks_tmp = f.read_record('i4',shape=2)
        if nks_tmp!=nks[ipool-1]: exit('Inconsistency in nks (No. of kpts in pool)!')
        for (iq,ik,ibnd,jbnd) in eph_idx:
           if ixkqf[ik+nnk,iq]>0:
                for imode in range(nmodes):
                    line=f.read_record('f8',shape=nnq[ik+nnk])
                    if wf[iq,imode]>=eps_acustic:
                        g2_[ik,innq[ik+nnk]-1,ibnd,jbnd,imode]=line
    print (np.allclose(g2,g2_))
    '''

    return g2*units.Rydberg**2
    

def read_ephmat(nks,ef0,fsthick,ekfs,ixkqf,nqfs,nbndfs,outdir='./tmp',seedname='wannier90',prefix='pw',eps_acustic=5.):
    get_ephmat = glob.glob('{}/{}.ephmat*'.format(outdir,seedname))
    npool = len(get_ephmat)
    nlines = get_ephmat_lines(outdir=outdir,prefix=prefix)
    nnq=calc_nnq(ixkqf)
    print ('\nReading ephmat: {0:5d} pools'.format(npool))
    g2=[]
    for ipool in range(1,npool+1):
        g2.append(
        read_ephmat_one_pool(ipool,nks,ef0,fsthick,ekfs,ixkqf,nqfs,nbndfs,nnq,nlines,
        outdir=outdir,seedname=seedname,prefix=prefix,eps_acustic=eps_acustic))
    return g2


def calc_kqmap(nkfs,xkfs,nqtotf,nqf1,nqf2,nqf3, nkf1,nkf2,nkf3,ixkf):
    ixkqf=np.zeros((nkfs,nqtotf),int)
    xqf=gen_xkff(nqf1,nqf2,nqf3)
    nqfs=np.zeros(nkfs,int)
    #ixkff=np.arange(nkf1*nkf2*nkf3)  # full k-mesh
    ixkff=ixkf
    print ('xqf',xqf.shape)
    print ('nqtotf',nqtotf)
    for ik,iq in np.ndindex(nkfs,nqtotf):
        xk=xkfs[ik]
        xq=xqf[iq]
        nkq=kpmq_map(xk,xq,1,nkf1,nkf2,nkf3)
        ixkqf[ik,iq]=ixkff[nkq]
        if ixkqf[ik,iq]>0: nqfs[ik]+=1
    return ixkqf,nqfs


def kpmq_map(xk,xq,sgn,nkf1,nkf2,nkf3):
    # find nkq, the index of k+sgn*q in the fine k-grid
    xxk=xk+float(sgn)*xq
    nxxk=xxk*np.array([nkf1,nkf2,nkf3])
    if max(abs(np.round(nxxk)-nxxk))>1e-4:
        exit('k +/- q not in kmesh!')
    nxxk[0]=int(round(nxxk[0]))%nkf1
    nxxk[1]=int(round(nxxk[1]))%nkf2
    nxxk[2]=int(round(nxxk[2]))%nkf3
    nkq= int(round(nxxk[0]*nkf2*nkf3 + nxxk[1]*nkf3 + nxxk[2]))
    return nkq
    

def test_kpmq():
    nkf1,nkf2,nkf3=(24,24,1)
    nqf1,nqf2,nqf3=(6,6,1)
    kmesh=gen_xkff(nkf1,nkf2,nkf3)
    qmesh=gen_xkff(nqf1,nqf2,nqf3)
    xk=kmesh[2]
    xq=qmesh[20]
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(1,1,figsize=(5,5))
    ax.scatter(kmesh[:,0],kmesh[:,1],s=5,facecolor='g',edgecolor='none')
    ax.scatter(qmesh[:,0],qmesh[:,1],s=20,facecolor='none',edgecolor='r')
    ax.scatter(xk[0],xk[1],marker='s',s=80,facecolor='none',edgecolor='b',label='k')
    ax.scatter(xq[0],xq[1],marker='d',s=80,facecolor='none',edgecolor='m',label='q')

    nkf = kpmq_map(xk, xq, 1, nkf1, nkf2, nkf3)
    ax.scatter(kmesh[nkf,0],kmesh[nkf,1],marker='^',s=80,facecolor='none',edgecolor='c',label='k+q')
    ax.scatter(xk[0]+xq[0],xk[1]+xq[1],marker='^',s=160,facecolor='none',edgecolor='c')
    nkf = kpmq_map(xk, xq, -1, nkf1, nkf2, nkf3)
    ax.scatter(kmesh[nkf,0],kmesh[nkf,1],marker='v',s=80,facecolor='none',edgecolor='c',label='k-q')
    ax.scatter(xk[0]-xq[0],xk[1]-xq[1],marker='v',s=160,facecolor='none',edgecolor='c')

    ax.legend(loc='lower right',scatterpoints=1)
    ax.set_aspect('equal')
    ax.set_xticks([-1,0,1])
    ax.set_yticks([-1,0,1])
    plt.show()
    return fig




#=================================
# MPI part, requires mpi4py
# and openmpi/mpich2
# for parallel processing data
# still under tests
#=================================

import mpi4py.MPI as MPI
import mpi4py

def get_mpi_handles():
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    node_name = MPI.Get_processor_name()
    return comm, size, rank, node_name


# free root means that the root process will not
# take over computational tasks, usually
# it will instead serves as a communicator
def assign_task(ntask,size,rank,free_root=False):
    if free_root:
        if rank==0:
            start = last = 0
        else:
            ave, res = divmod(ntask, size-1)
            ntask_local = [ave+1]*res + [ave]*(size-1-res)
            start = np.append(0,np.cumsum(ntask_local)[:-1])[rank-1]
            last = np.cumsum(ntask_local)[rank-1]
    else:
        ave, res = divmod(ntask, size)
        ntask_local = [ave+1]*res + [ave]*(size-res)
        start = np.append(0,np.cumsum(ntask_local)[:-1])[rank]
        last = np.cumsum(ntask_local)[rank]
    return start, last


def mpi_read_nks(outdir='tmp',prefix='wannier90',seedname='wannier90'):
    comm,size,rank,node=get_mpi_handles()
    nks=None
    if not rank: nks=read_nks(outdir=outdir,prefix=prefix,seedname=seedname)
    nks=comm.bcast(nks,root=0)
    return nks


def mpi_read_egnv(outdir='./tmp',seedname='wannier90'):
    comm,size,rank,node=get_mpi_handles()
    if not rank:
        grid_params,en_params,wkfs,xkfs,ekfs = read_egnv(outdir=outdir,seedname=seedname)
    else:
        grid_params=None
        en_params=None
        wkfs,xkfs,ekfs=(None,None,None)
    comm.barrier()
    grid_params=comm.bcast(grid_params,root=0)
    en_params=comm.bcast(en_params,root=0)
    wkfs,xkfs,ekfs=comm.bcast((wkfs,xkfs,ekfs),root=0)
    return grid_params,en_params,wkfs,xkfs,ekfs


def mpi_read_ephmat(nks,ef0,fsthick,ekfs,ixkqf,nqfs,nbndfs,
    outdir='./tmp',seedname='wannier90',prefix='pw',eps_acustic=5.):

    comm,size,rank,node=get_mpi_handles()
    npool=int(len(os.popen('ls {}/{}.ephmat*'.format(outdir,seedname)).readlines()))
    nnq=calc_nnq(ixkqf)
    nlines = get_ephmat_lines(outdir=outdir,prefix=prefix,seedname=seedname)
    if rank==0: print('\nReading ephmat: {:5d} pools'.format(npool))
    start,last=assign_task(npool,size,rank)
    for ii,i in enumerate(range(start,last)):
        read_ephmat_one_pool(i+1,nks,ef0,fsthick,ekfs,ixkqf,nqfs,nbndfs,nnq,nlines,
        outdir=outdir,seedname=seedname,prefix=prefix,eps_acustic=eps_acustic)
    comm.barrier()

