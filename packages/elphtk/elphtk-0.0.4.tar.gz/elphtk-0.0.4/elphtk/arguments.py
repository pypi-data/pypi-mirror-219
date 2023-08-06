#!/usr/bin/env python


#===========================================================================#
#                                                                           #
#  File:       arguments.py                                                 #
#  Dependence: none                                                         #
#  Usage:      process with arguments                                       #      
#  Author:     Shunhong Zhang <szhang2@ustc.edu.cn>                         #
#  Date:       May 15, 2020                                                 #
#                                                                           #
#===========================================================================#


import argparse

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):    return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):  return False
    else: raise argparse.ArgumentTypeError('Unsupported value encountered.')


def add_control_arguments(parser):
    parser.add_argument('--source',type=str,default='phonopy',help='source file type: phonopy/QE/Abinit')
    parser.add_argument('--restart',type=str2bool,const=False,default=False,nargs='?',help='restart mode or not')
    parser.add_argument('--fromfile',type=str2bool,default=False,help='restart by reading data from file')
    parser.add_argument('--restart_point',type=str,default='weights',help='restart point, can be "weights" or "kpdos"')
    parser.add_argument('--outdir',type=str,default='./tmp',help='directory to store temporary files')
    parser.add_argument('--task',type=str,default=None,help='task to process')
    parser.add_argument('--enable_plot',type=str2bool,default=True,help='enable the plot functionality') 
    parser.add_argument('--show_plot',type=str2bool,default=False,help='show the plot')
    parser.add_argument('--irr_to_BZ',type=str2bool,nargs='?',const=False,help='map kpts in irreducible BZ to 1st BZ')
 

def add_io_arguments(parser):
    parser.add_argument('--poscar', type=str, default='POSCAR', help='POSCAR file')
    parser.add_argument('--procar', type=str, default='PROCAR', help='POSCAR file')
    parser.add_argument('--doscar', type=str, default='DOSCAR', help='DOSCAR file')
    parser.add_argument('--poscar1',type=str,default='POSCAR1',help='the first POSCAR file')
    parser.add_argument('--poscar2',type=str,default='POSCAR2',help='the second POSCAR file')
    parser.add_argument('--foutcar',type=str,default='OUTCAR',help='the VASP OUTCAR file')
    parser.add_argument('--filpw',type=str,default='scf.out',help='QE pw.x output file')
    parser.add_argument('--output', type=str, default='output_plot',
                        help='Filename for the plot. It accepts all image formats supported by matplotlib.')
    parser.add_argument('--verbosity',type=int,default=1,help='level of verbosity')


def add_fig_arguments(parser):
    parser.add_argument('--figname',type=str,default='phband',
                        help='file name for the figure saved')
    parser.add_argument('--figsize', type=eval, default=(5, 4),
                       help='Figure size. Default: %(default)s')
    parser.add_argument('--dpi', type=float, default=600,
                       help='Plot resolution. Default: %(default)s')
    parser.add_argument('--subplot',type=str2bool,nargs='?',const=False,default=False,
                       help='whether or not to plot in subplots. Default: %(default)s')
    parser.add_argument('--marker', type=str, default='o',
                       help='Marker for the fatband plot. Default: %(default)s.')
    parser.add_argument('--markersize', type=float, default=20,
                       help='Marker size. Default: %(default)s.')
    parser.add_argument('--marker_lw',type=float,default=1,
                       help='marker line width')
    parser.add_argument('--marker_color',type=str,default='blue',
                       help='marker color')
    parser.add_argument('--linewidth', type=float, default=0.5,
                       help='line width. Default: %(default)s')
    parser.add_argument('--nplot', type=eval,default=(1,1),help='nrow and ncol of subplots. Default: %(default)s') 
    parser.add_argument('--hratio',type=eval,default=(1,1),help='height ratios of subplots. Default: %(default)s')
    parser.add_argument('--wratio',type=eval,default=(1,1),help='width ratios of subplots. Default: %(default)s')
    parser.add_argument('--alpha',type=float,default=0.8,help='transparency for plot')
    parser.add_argument('--savefig',type=str2bool,nargs='?',const=True,default=True,help='save figure or not')


def add_plot_arguments(parser):
    parser.add_argument('--title', type=str, default=None, help="title of plot. Default: %(default)s")
    parser.add_argument('--subtitles',type=str,default=None,help='title for each subplot. Default: %(default)s')
    parser.add_argument('--style', type=str, default='line', help='style to plot the data points, Default: %(default)s')
    parser.add_argument('--color', type=str, default="red blue green orange violet cyan magenta black yellow olive pink royalblue",
                        help='Color for the marker. It accepts any color specification '
                        'accepted by matplotlib. Color specified as r,g,b tuple should ' 
                        'not have any spaces. Default: %(default)s')
    parser.add_argument('--elim', type=eval, default=(1,-1),
                        help='Energy range for the plot, specified as emin,emax.'
                        'Default is entire band range.')
    parser.add_argument('--efermi', type=float, default=0,
                        help='Fermi energy. Default: %(default)s.')
    parser.add_argument('--shift_fermi',type=str2bool,nargs='?',const=True,default=True,help='shift the fermi energy to 0 or not? Default: %(default)s')
    parser.add_argument('--proj_type',type=str,default='None',
                        help='prjection type. Default: %(default)s')
    parser.add_argument('--proj_index',type=str,default="0",
                        help='index of species/atoms/orbitals for projection. Default: %(default)s')
    parser.add_argument('--proj_spec_orb_index',type=str,default=None,
                        help='for species_orbtials projection. Default: %(default)s')
    parser.add_argument('--label_k', type=str, default=None,
                        help='labels for high symmetry k points. '
                        'Use the form like \Gamma to represent Greek characters.\n'
                        "Example: --label_k '\Gamma X M \Gamma Y M'. Default: %(default)s")
    parser.add_argument('--xlabel_thr',type=int,default=15,help='the threhold for refine the xlabels, read the code or consult the author for details')
    parser.add_argument('--legend_switch',type=str2bool,nargs='?',const=True,default=True,help='switch to control legends. Default: %(default)s')
    parser.add_argument('--legend_content',type=str,default=None,help='customized legend from user. Default: %(default)s')
    parser.add_argument('--legend_pos',type=eval,default=None,help='left up position of legend box. Default: %(default)s')
    parser.add_argument('--legend_loc',type=str,default='upper left',help='location of legend box')
    parser.add_argument('--legend_fontsize',type=int,default=10,help='fontsize for legend texts. Default: %(default)s')
    parser.add_argument('--pow', type=float, default=1,
                        help='Raise orbital weights to the specified integer power. '
                        'Powers larger than 1 help to filter out the ghost energy '
                        'in the unfolded band structures. Default: %(default)s')
    parser.add_argument('--y_nticks',type=int,default=0,help='# of y ticks')
    parser.add_argument('--yticks',type=eval,default=None,help='costomerized yticks')
    parser.add_argument('--ylim',type=eval,default=None,
                        help='limit of the DOS in y axis')
    parser.add_argument('--lylabel',type=str2bool,nargs='?',const=True,default=True,help='write ylabel or not')
    parser.add_argument('--ylabel',type=str,default='$E-E_f$ ($eV$)',help='ylabel')
    parser.add_argument('--ylabel_pos',type=eval,default=(-0.5,0.5),help='ylabel position')
    parser.add_argument('--label_fontsize',type=int,default=12,help='font size for labels')
    parser.add_argument('--spin_color',type=str2bool,nargs='?',const=False,default=False,help='use different colors for spins')
    parser.add_argument('--proj_spinor',type=str2bool,nargs='?',const=False,default=False,help='projected on the sz weights, only used for noncollinear spin polarized calculations')
    parser.add_argument('--proj_spinor_index',type=int,default=-1,help='spinors of single atom or total,-1 for total')
    parser.add_argument('--spinor_dir',type=int,default=2,help='primary direction of spinor bands')
    parser.add_argument('--int_tdos',type=str2bool,nargs='?',const=False,default=False,
                        help='whether or not to plot the integrated DOS. Default: %(default)s')
    parser.add_argument('--int_pdos',type=str2bool,nargs='?',const=False,default=False,help='integrate pdos or not')
    parser.add_argument('--yannotates',type=eval,default=None,help='annotation for yaxis, read the code or consult the author for details')
    parser.add_argument('--ymax',type=float,default=None,help='maximum of y axis')
    parser.add_argument('--vb_index',type=int,default=0,help='index of valance band')
    parser.add_argument('--cb_index',type=int,default=0,help='index of conduction band')
    parser.add_argument('--bandcolor',type=str,default=None,help='color of band plot')
    parser.add_argument('--bgcolor',type=str,default=None,help='background color for the plot')



def add_band_arguments(parser):
    parser.add_argument('--mode',type=str,default='band',help='the mode can be band of mesh')
    parser.add_argument('--xsym_index',type=eval,default=None)
    parser.add_argument('--start_band',type=int,default=0,help='first band to parse')
    parser.add_argument('--last_band',type=int,default=-1,help='last band to parse')
    parser.add_argument('--write_dat',type=str2bool,const=False,default=True,nargs='?',help='write data in dat format')
    parser.add_argument('--nejdos',type=int,default=300,help='number of histogram bins for JDOS')
    parser.add_argument('--sigma',type=float,default=0.01,help='smearing width for JDOS')
    parser.add_argument('--kdim',type=eval,default=0,help='dimension of k mesh')
    parser.add_argument('--filband',type=str,default='band.out',help='file name for band of QE')
    parser.add_argument('--highlight_band',type=eval,default=False,help='index of bands to hilight')
    parser.add_argument('--highlight_band_color',type=str,default='blue',help='color for the highlighted bands')
    parser.add_argument('--nx',type=int,default=0,help='dim of x for mesh mode')
    parser.add_argument('--ny',type=int,default=0,help='dim of y ofr mesh mode')
    parser.add_argument('--shade_bands',type=str2bool,nargs='?',const=False,default=False,help='shading bands')
    parser.add_argument('--shade_band_idx',type=eval,default=None,help='band indice between which are shaded')
    parser.add_argument('--shade_band_color',type=str,default='blue',help='color to shade certain bands')
    parser.add_argument('--shade_band_alpha',type=float,default=0.5,help='transparency of shaded bands')
    parser.add_argument('--startk',type=int,default=0,help='index for the k-point to start band calculation')
    parser.add_argument('--parse_eigenval',type=str2bool,nargs='?',const=False,default=False,help='parse EIGENVAL file')
    parser.add_argument('--max_band_idx',type=int,default=1000,help='index of the highest band to plot')


def add_wan_arguments(parser):
    parser.add_argument('--plus_wan',type=str2bool,nargs='?',const=False,default=False,help='plot the bands from wanniersation for comparison')
    parser.add_argument('--wan_outdir',type=str,default='./',help='directory containing wannier90 output')
    parser.add_argument('--wan_seedname',type=str,default='wannier90',help='seedname for wannierisation')
    parser.add_argument('--wan_efermi',type=float,default=0,help='fermi energy for wannierisation')
    parser.add_argument('--wan_bandpoint',type=int,default=100,help='num of band points for wann band plot')
    parser.add_argument('--wan_markersize', type=float, default=10,help='Marker size. Default: %(default)s.')
    parser.add_argument('--wan_color',type=str,default='g',help='color for the wannier data points')
    parser.add_argument('--write_wan_eig',type=bool,default=False,help='write the eigenvalues in the wannier.eig format')
    parser.add_argument('--wan_legend',type=str,default=None,help='legend of wannier plot')



def add_phonon_arguments(parser):
    parser.add_argument('--filph',type=str,default='band.yaml',help='file containing phonon results')
    parser.add_argument('--top_panel_min',type=float,default=3500,help='min value of top panel after breaking the axis')
    parser.add_argument('--top_panel_max',type=float,default=4000,help='max value of top panel after breaking the axis')
    parser.add_argument('--top_panel_step',type=float,default=200,help='step after breaking the axis')
    parser.add_argument('--bot_panel_min',type=float,default=-500,help='min value of bottom panel after breaking the axis')
    parser.add_argument('--bot_panel_max',type=float,default=2000,help='max value of bottom panel after breaking the axis')
    parser.add_argument('--bot_panel_step',type=float,default=200,help='step after breaking the axis')
    parser.add_argument('--break_yaxis',type=str2bool,nargs='?',const=False,default=False,help='break the yaxis to show the high frequency')
    parser.add_argument('--label_q',type=str,default=None,help='label of q-points')
    parser.add_argument('--freq_unit',type=str,default='THz',help='unit of frequency in plot')
    parser.add_argument('--shade_bands',type=str2bool,nargs='?',const=False,default=False,help='shading bands')
    parser.add_argument('--elph_method',type=str,default='interpolated',help='method to calc el-ph coupling')




if __name__=='__main__':
    print ('\nthis is a collection of arguments for')
    print ('applications in python code elphtk')
