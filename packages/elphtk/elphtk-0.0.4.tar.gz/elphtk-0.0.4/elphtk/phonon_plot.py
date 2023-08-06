#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
matplotlib.rc('text', usetex=True)
matplotlib.rcParams['text.latex.preamble']=r"\usepackage{amsmath}"
ticks_font = matplotlib.font_manager.FontProperties(family='times new roman', style='normal', size=12, weight='normal', stretch='normal')


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



def print_k_node_xlabels(isym,k_node,xlabels):
    k_node_info ='\n{0}\nhigh symmetry k points\n{0}\n'.format('-'*50)
    k_node_info+='{0:>4s} {1:>10s}   {2:<20s}\n'.format('ik','xticks','xlabels')
    k_node_info+='\n'.join(['{0:4d} {1:10.6f}   {2:<20s}'.format(*tuple(item)) for item in zip(isym,k_node,xlabels)])
    k_node_info+='\n{0}\nhigh symmetry k points\n{0}\n'.format('-'*50)
    print (k_node_info)
    try: print (k_node_info, file=open('k_node_info.dat','w'))
    except: print ('Fail to write k nodes to k_node_info.dat')



def plot_band_framework(ax,k_dist,k_node,xlabels,args,efermi=0,plot_efermi=True):
    if args.elim[1]>args.elim[0]: ax.set_ylim(args.elim)
    if k_node is not None:
        for xi in k_node: ax.axvline(xi, color='gray', zorder=-1,lw=0.7,alpha=0.8)
        ax.set_xticks(k_node)
        for tick in ax.get_xticklines(): tick.set_visible(False)
        if xlabels is not None:
            try: ax.set_xticklabels(xlabels,fontsize=args.label_fontsize)
            except: print ('fail to set xtick with k-point label')
        else:
            ax.set_xticklabels([])
    else:
        ax.set_xticks([])
    ax.set_xlim(k_dist[0],k_dist[-1])
    if plot_efermi: ax.axhline(efermi, color='gray', ls='--', zorder=-1,alpha=0.8)
    if args.bgcolor: ax.patch.set_facecolor(args.bgcolor)
    if args.title: ax.set_title(output)
    ax.tick_params(top='off',right='off',direction='out')
    ax.get_yaxis().set_tick_params(direction='out')
    ax.get_xaxis().set_tick_params(length=0.0)
    if args.yticks: ax.set_yticks(args.yticks)
    for label in ax.get_yticklabels():
        label.set_fontsize(args.label_fontsize)
    if args.shade_bands:
        idx_list=args.shade_band_idx
        for i in range(0,len(idx_list),2):
            if i==len(idx_list)-1: break
            print('shade region between band {0} and {1}'.format(idx_list[i],idx_list[i+1]))
            y1=energy[0,:,idx_list[i]-1]
            y2=energy[0,:,idx_list[i+1]-1]
            ax.fill_between(k_dist, y1, y2, where=y2 >= y1,facecolor=args.shade_band_color,
            interpolate=True,alpha=args.shade_band_alpha)


def plot_phband(distance,freq,k_node,xlabels,args):
    #print_k_node_xlabels(isym,k_node,xlabels)
    fig, ax=plt.subplots(1,1,figsize=args.figsize)
    dists=np.tile(distance,(freq.shape[1],1)).T
    if 'line' in args.style:  ax.plot(distance,freq,color=args.color.split()[0])
    if 'dot' in args.style:   ax.scatter(dists,freq,facecolor=args.color.split()[0],edgecolor='none',s=args.markersize)
    ax.set_ylabel('$\omega$ $\mathrm{('+args.freq_unit+')}$')
    for label in ax.get_yticklabels() :
        label.set_fontproperties(ticks_font)
    if args.break_yaxis: fig,ax,ax2 = plot_break_yaxis(distance,freq,args)
    if xlabels is not None: labels=['${0}$'.format(label) for label in xlabels]
    plot_band_framework(ax,distance,k_node,xlabels,args)
    fig.tight_layout()
    if args.savefig:    fig.savefig('{}_{}'.format(args.figname,args.source),dpi=args.dpi)
    if args.show_plot:  plt.show()
    return fig


def plot_gibbs():
    fil='gibbs-temperature.dat'
    data=np.loadtxt(open(fil))
    fig=plt.figure(figsize=(4,4))
    ax=fig.add_subplot(111)
    ax.plot(data[:,0],data[:,1],color='g')
    ax.set_xlabel('$\mathrm{T (K)}$')
    ax.set_ylabel('$\mathrm{G (eV)}$')
    fig.tight_layout()
    fig.savefig('Gibbs-T',dpi=400)
    return fig


def plot_qe_ph(distance,freq,k_node,args):
    import phonopy.units as units
    xlabels=None
    if args.label_q is not None: xlabels=args.label_q.split()
    else: print ('\nQlabels not found\nuse --label_q to specify labels for q-points\n')
    check_imag_freq(freq/units.THzToCm)
    nqpt,nmode=freq.shape
    print ('no. of qpts     ={0:4d}'.format(nqpt))
    print ('no. of modes    ={0:4d}'.format(nmode))
    save_tag = args.savefig
    args.savefig=False
    fig = plot_phband(distance,freq,k_node,xlabels,args)
    ax=fig.axes[0]
    if args.plot_gamma:
        gamma=get_gamma(outdir=args.outdir,filgamma='elph.gamma',isigma=args.isigma)
        plot_gamma(ax,distance,freq,gamma,args)
    if args.phlw:
        lw=get_epw_ph_linewidth()
        ax.scatter(np.tile(distance,(nmode,1)).T,freq,s=args.markersize*lw,facecolor='r',edgecolor='none')
    if args.break_yaxis:
        fig,ax,ax2 = plot_break_yaxis(distance,freq,args)
    fig.tight_layout()
    if save_tag: fig.savefig('{}_{}'.format(args.figname,args.source),dpi=args.dpi)
    if args.show_plot: plt.show()
    return fig


def plot_break_yaxis(distance,freq,args):
    import matplotlib.gridspec as gridspec
    print ('break y-axis into two parts')
    nrow=2
    ncol=1
    gs=gridspec.GridSpec(nrow,ncol,height_ratios=[item for item in args.hratio],width_ratios=[item for item in args.wratio])
    fig=plt.figure(figsize=args.figsize)
    top=fig.add_subplot(gs[0])
    bot=fig.add_subplot(gs[1],sharex=top)
    top.plot(distance,freq,'g-')
    bot.plot(distance,freq,'r-')
    top.set_xlim(np.min(distance),np.max(distance))
    bot.set_xlim(np.min(distance),np.max(distance))
    bot.set_ylim(args.bot_panel_min,args.bot_panel_max)
    bot.set_yticks(np.arange(args.bot_panel_min,args.bot_panel_max,args.bot_panel_step))
    top.set_ylim(args.top_panel_min,args.top_panel_max)
    top.set_yticks(np.arange(args.top_panel_min,args.top_panel_max,args.top_panel_step))
    top.spines['bottom'].set_visible(False)
    bot.spines['top'].set_visible(False)
    bot.xaxis.tick_bottom()
    top.xaxis.tick_top()
    top.tick_params(labeltop='off')
    #bot.tick_params(labelbottom='off')
    try:
        k_node=get_k_node_from_matdyn(distance)
        for xx in k_node: top.axvline(xx,c='gray',alpha=0.7)
        for xx in k_node: bot.axvline(xx,c='gray',alpha=0.7)
        for tick in top.get_xticklines(): tick.set_visible(False)
        for tick in bot.get_xticklines(): tick.get_visible(False)
        bot.set_xticks(k_node)
        bot.set_xticklabels(['${0}$'.format(item) for item in args.label_q.split()])
    except:
        pass
    plt.ylabel('Frequency (cm$^{-1}$)')
    if args.freq_unit=='THz': plt.ylabel('Frequency (THz)')
    fig.tight_layout()
    return fig,top,bot


def plot_gamma(ax,distance,freq,gamma,args):
    nqpt,nmode=freq.shape
    if gamma.shape!=freq.shape:
        print ('\nThe shape of gamma (EPC) inconsistent with freq, gamma not plotted!')
    else:
        neg_idx=np.where(gamma<0)
        gamma_ = np.zeros_like(gamma)
        gamma_[neg_idx] = -gamma[neg_idx]
        gamma[neg_idx] = 0.
        ax.scatter(np.tile(distance,(nmode,1)).T,freq,s=gamma *args.markersize,edgecolor='none',facecolor='r',alpha=0.8,zorder=-1)
        if neg_idx[0].shape>1:
            print ('\nNote: some negative gamma detected, marked in blue')
            ax.scatter(np.tile(distance,(nmode,1)).T,freq,s=gamma_*args.markersize,edgecolor='none',facecolor='b',alpha=0.5,zorder=-2)
