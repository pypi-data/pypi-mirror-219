#!/usr/bin/env python

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
