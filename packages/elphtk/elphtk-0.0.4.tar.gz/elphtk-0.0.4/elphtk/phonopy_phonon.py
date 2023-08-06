#!/usr/bin/env python

import os
import numpy as np
try:    import yaml
except: ImportError("You need to install python-yaml")
try:
    from yaml import CLoader as Loader
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def get_yaml_data(filename):
    if not os.path.isfile(filename):
        exit('cannot find {0}'.format(filename))
    print ('parsing file: {0}'.format(filename))
    return yaml.load(open(filename), Loader=Loader)
    

def parse_yaml(filename,evec=False):
    data = get_yaml_data(filename)
    frequencies = []
    distances = []
    labels = []
    eigenvec=[]
    seg_points=[]
    qpt=[]
    data_mode='band'
    try:
        nx,ny,nz=data['mesh']
        print ('uniform q-mesh:',data['mesh'])
        data_mode='mesh'
    except: print ('band mode')

    for j, v in enumerate(data['phonon']):
        qpt.append([float(item) for item in v['q-position']])
        if 'label' in v: labels.append(v['label'])
        else: pass
        frequencies.append([f['frequency'] for f in v['band']])
        try: distances.append(v['distance'])
        except: data_mode='mesh'
        if evec:
           try: eigenvec.append([f['eigenvector'] for f in v['band']])
           except: raise Exception('not eigenvector read!')
    try: seg_points=[0]+data['segment_nqpoint']
    except: pass
    if labels: labels=[labels[0]]+labels[1::2]
    else:
        try:
            for j, v in enumerate(data['labels']):
                labels+=v
            labels=[labels[0]]+labels[1::2]
        except:
            pass
    freq=np.array(frequencies)
    qpt=np.array(qpt)
    distances=np.array(distances)
    eigenvec=np.array(eigenvec)
    xsym=np.append(0,distances[np.cumsum(seg_points)-1][1:])
    return (data_mode,qpt,distances,freq,eigenvec,xsym,labels)


def check_imag_freq(freq):
    if np.min(freq)>=0: return
    idx=np.where(freq==np.min(freq))
    print ('\n{0}'.format('-'*40))
    print ('Imaginary mode detected:')
    print ('freq (THz) : {0:10.4f} i'.format(np.min(freq)))
    print ('imode      : {0:10d}'.format(idx[1][0]+1))
    print ('iqpt       : {0:10d}'.format(idx[0][0]+1))
    print ('{0}\n'.format('-'*40))
    return idx


def write_freq(distance,freq):
    nqpt,nband=freq.shape
    with open('freq.dat','w') as fw:
        for iband in range(nband):
            fw.write('\n'.join(['{0:12.7f} {1:12.7f}'.format(*tuple(item)) for item in zip(distance,freq[:,iband])])+'\n\n')
    with open('phonopy.freq.gp','w') as fw:
        for iqpt in range(nqpt):
            fw.write('{:12.7f}'.format(distance[iqpt]))
            fw.write(('{:12.7f}'*nband+'\n').format(*tuple(freq[iqpt])))



