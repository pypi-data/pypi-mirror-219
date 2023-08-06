#!/usr/bin/env python


#=======================================
# Some functions to parse qe output
# related to phonon calculations
# Shunhong Zhang
# szhang2@ustc.edu.cn
# Date: Jun 19, 2020
#=======================================


import numpy as np
import os
import sys
import re
import phonopy.units as units
from collections import Counter


def get_qpt_from_phout(outdir='./',filph='ph.out'):
    lines=np.array(open('{0}/{1}'.format(outdir,filph)).readlines())
    idx=np.where([re.search("Calculation of q =",line) for line in lines])
    qpts=np.array([line.split()[4:7] for line in lines[idx]],float)
    idx=np.where([re.search("Number of q in the star =",line) for line in lines])[0]
    if len(idx)//2==len(qpts): idx=idx[::2]
    qweights=np.array([line.split()[-1] for line in lines[idx]],float)
    if qpts.shape[0]!=qweights.shape[0]: 
        exit('number of q-points and weights inconsistent!')
    return qpts,qweights


def get_qe_dynmat(prefix,idyn,verbosity=False):
    fil='{}.dyn{}'.format(prefix,idyn)
    nqpt=int(os.popen('grep -c "Dynamical  Matrix" {0}'.format(fil)).read().split()[0])
    with open(fil) as f:
        comment=f.readline()
        f.readline()
        line=f.readline().split()
        ntyp,nat,ibrav=np.array(line[:3],int)
        celldm=np.append(0,np.array(line[3:],float))
        lines=np.array([f.readline().split() for i in range(ntyp)])
        species=np.array([line[1].strip("'") for line in lines])
        mass=np.array([float(line[-1])/911.4442 for line in lines])
        lines=np.array([f.readline().split() for i in range(nat)],float)
        atom_type=np.array(lines[:,1],int)
        pos=np.array(lines[:,2:5],float)
        qpt=[]
        dyn0=np.zeros((nqpt,nat,nat,3,3,2),float)
        f.readline()
        for iqpt in range(nqpt):
            lines=[f.readline().split() for i in range(4)]
            qpt.append(lines[2][3:6])
            for i,j in np.ndindex(nat,nat):
                f.readline()
                dyn0[iqpt,i,j]=np.fromfile(f,sep=' ',count=18,dtype=float).reshape(3,3,2)
        qpt=np.array(qpt,float)
        for i in range(5): f.readline()
        freq={'THz':np.zeros(nat*3,float),'cm-1':np.zeros(nat*3,float)}
        disp=np.zeros((nat*3,nat,3,2),float)
        for i in range(nat*3):
            line=f.readline().split()
            freq['THz'][i]=float(line[4])
            freq['cm-1'][i]=float(line[7])
            lines=[f.readline().split()[1:-1] for j in range(nat)]
            disp[i]=np.array(lines,float).reshape(nat,3,2)

    from pysupercell.QE_ibrav_lib import make_cell_qe
    counts=np.array([Counter(atom_type)[ityp+1] for ityp in range(ntyp)])
    cell=make_cell_qe(ibrav,celldm,verbosity=verbosity)
    try:
        from pysupercell.pysupercell import cryst_struct
        struct = cryst_struct(cell,species,counts,pos,scale=1)
    except:
        struct = (cell,species,counts,pos,scale)

    dynmat=dyn0[...,0]+1.j*dyn0[...,1]
    disp=disp[...,0]+1.j*disp[...,1]
    return struct,mass,dynmat,freq,disp


def diagonalize_dynmat(dyn,struct):
    amu_ry=units.AMU/units.Me/2.
    ry_to_thz=units.Rydberg/units.THzToEv
    dyn=np.transpose(dyn,[0,2,1,3])
    mass = struct._get_mass()
    for iat,jat in np.ndindex(struct._natom,struct._natom):
        dyn[iat,:,jat] /= np.sqrt(mass[iat]*mass[jat])*amu_ry
    dynmat=dyn.reshape(struct._natom*3,struct._natom*3)
    eigs,evec=np.linalg.eigh(dynmat)
    freq=np.sqrt(abs(eigs))*ry_to_thz*np.sign(eigs)
    disp=evec.T
    disp=disp.reshape(struct._natom*3,struct._natom,3)
    return dynmat,freq,disp


# read phonon frequencies from ph.out, output of ph.x of QE
def get_freq_from_phout(outdir='./',filph='ph.out'):
    lines=open('{0}/{1}'.format(outdir,filph)).readlines()
    idx=np.where([re.search('THz',line) for line in lines])
    data=np.array(lines)[idx]
    freqs=np.array([item.split()[4] for item in data],float)
    nmode=len(set([item.split()[2] for item in data]))
    nq=len(freqs)//nmode
    return freqs.reshape(nq,nmode)


def read_qe_modes(fil='matdyn.modes'):
    print ('parsing file {0}'.format(fil))
    lines=open(fil).readlines()
    idx=np.where([re.search("q =",line) for line in lines])[0]
    nqpt=len(idx)
    idx=np.where([re.search('freq',line) for line in lines])[0]
    nmode=len(idx)/nqpt
    qpts=np.zeros((nqpt,3),float)
    freq_THz=np.zeros((nqpt,nmode),float)
    freq_cm=np.zeros((nqpt,nmode),float)
    modes=np.zeros((nqpt,nmode,nmode/3,6),float)
    print ('no. of q points = {0:3d}'.format(nqpt))
    print ('no. of modes    = {0:3d}'.format(nmode))
    with open(fil) as f:
        for iqpt in range(nqpt):
            f.readline()
            f.readline()
            line=f.readline().split()
            qpts[iqpt]=np.array(line[2:],float)
            f.readline()
            for iband in range(nmode):
                line=f.readline().split()
                freq_THz[iqpt,iband]=float(line[4])
                freq_cm[iqpt,iband]=float(line[7])
                for iat in range(3):
                    line=f.readline().split()
                    modes[iqpt,iband,iat]=np.array(line[1:-1],float)
            f.readline()
    freq={'THz':freq_THz,'cm-1':freq_cm}
    return qpts,freq,modes


def create_qe_disp_struct(sc,iqpt,iband,phase_phi=0,disp=5,filpw='scf.in'):
    # create displacement from QE output phonon modes
    # still under test
    from psupercell.pysupercell import cryst_struct
    qpts,freq,modes=read_qe_modes()
    struct = cryst_struct.load_pwscf_in(fil_pwscf_in=filpw)
    struct.write_poscar_head()
    struct.write_poscar_atoms()
    if len(sc)==3: trans=np.diag(sc)
    elif len(sc)==9: trans=np.array(sc).reshape(3,3)
    else: exit('size of sc should be 3 or 9!')
    print ( ('supercell size:\n',trans))
    mstruct=struct.build_supercell(trans)
    mstruct._system='modulated structure'
    struct.write_poscar_head(filename='MPOSCAR')
    struct.write_poscar_atoms(filename='MPOSCAR')
    pos_cart=mstruct._pos_cart
    disp_cart=np.zeros((mstruct._natom,3),float)
    phase=2.j*np.pi*phase_phi/180
    for idir in range(3):
        norm=np.linalg.norm(modes[iqpt-1,iband-1,:,idir*2:idir*2+1],axis=-1)
        disp_cart[:,idir]=norm*np.exp(phase)
    disp_pos_cart=pos_cart+disp_cart
    disp_pos=np.dot(disp_pos_cart,np.linalg.inv(mstruct._cell))
    mstruct._pos=disp_pos
    mstruct._pos_cart=disp_pos_cart
    return mstruct


def get_epw_ph_linewidth(fil='linewidth.phself'):
    with open(fil) as f:
        f.readline()
        data=np.loadtxt(f)
    subsets=set(data[:,1])
    print ('no. of branches: {0:2d}'.format(len(subsets)))
    print ('max linewidth: {0}'.format(np.max(data[:,-1])))
    print ('min linewidth: {0}'.format(np.min(data[:,-1])))
    if np.where(data[:,3]<0):
       print ('\nWarning: the linewidth for the following data points are negative!')
       for idx in np.where(data[:,3]<0)[0]:
           print ('{0:4.0f} {1:4.0f} {2:12.6f} {3:12.6f}'.format(data[idx,0],data[idx,1],data[idx,2],data[idx,3]))
       print ('\n')
       print ('They are adjusted to zero during plotting\n')
       data[np.where(data[:,3]<0)[0],3]=0
    for isub in subsets:
        idx=np.where(data[:,1]==isub)[0]
    nmode=len(set(data[:,1]))
    nkpt=len(data)/nmode
    lw=data[:,3]
    return lw


def get_gamma_lines(fil='gam.lines'):
    print ('reading gamma from {0}'.format(fil))
    print ('in unit of THz')
    lines=open(fil).readlines()
    idx=np.where([re.search('Broad',line) for line in lines])[0]
    idx=np.append(idx,len(lines))
    gam=[]
    for ii in range(len(idx)-1):
        gam0=[item.rstrip('\n').split() for item in lines[idx[ii]:idx[ii+1]][2::2]]
        gam.append(gam0)
    gam=np.array(gam,float)
    return gam


def get_gamma(outdir='./',filgamma='elph.gamma',isigma=1):
    filgamma='{0}/{1}.{2}'.format(outdir,filgamma,isigma)
    print (filgamma)
    lines=[item.split() for item in open(filgamma).readlines()]
    for line in lines:
        for item in line:
            if item.count('.')>1: 
                print ('Something wrong with file {0}'.format(filgamma))
                print ('Check it carefully. Some very large value in it?')
                exit(1)
    print ('\nreading gamma data from {0}'.format(filgamma))
    print ('in unit of GHz')
    fix='sed -i "s/\([0-9]\)\-\([0-9]\)/\\1 -\\2/g" {0}'.format(filgamma)
    os.system(fix)
    with open(filgamma) as f:
        line=f.readline().split()
        nmode=int(line[2].split(',')[0])
        nqpt=int(line[4])
        gamma=np.zeros((nqpt,nmode),float)
        for iqpt in range(nqpt):
            line=f.readline()
            gamma[iqpt]=np.fromfile(f,count=nmode,sep=' ',dtype=float)
    print ('range of gamma [{0:10.5f} {1:10.5f}]\n'.format(np.min(gamma),np.max(gamma)))
    return gamma


def get_qe_freq(args):
    if not args.prefix:
        try:
            args.prefix=os.popen('ls *.freq.gp 2>/dev/null').readline().split('.')[0]
            print ( ('prefix not specified. We guess prefix="{0}"'.format(args.prefix)))
            yn=input('Is it correct (y/n)')
            if 'n' in yn: args.prefix=input('Input manually, prefix=')
        except:
            print('please use --prefix to specify the prefix of the filename!')
    fil='{0}.freq.gp'.format(args.prefix)
    if args.prefix=='phband': fil=fil.rstrip('.gp')
    if not os.path.isfile(fil): exit('cannot find {0}'.format(fil))
    data=np.loadtxt(open(fil))
    distance=data[:,0]
    freq=data[:,1:]
    return distance,freq


def get_k_node_from_matdyn(distance,filmatdyn='matdyn.in'):
    if not os.path.isfile(filmatdyn): 
        print('{} not found'.format(filmatdyn))
        return None
    lines=open('matdyn.in').readlines()
    idx=np.where([re.search('/',line) for line in lines])[0][0]
    k_node_idx=[int(item.rstrip('\n').split()[3]) for item in lines[idx+2:-1]]
    k_node = distance[np.append(0,np.cumsum(k_node_idx))]
    return k_node
