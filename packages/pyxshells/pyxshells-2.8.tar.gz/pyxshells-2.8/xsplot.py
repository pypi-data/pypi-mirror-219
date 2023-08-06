#
#  Copyright (c) 2010-2021 Centre National de la Recherche Scientifique.
#  written by Nathanael Schaeffer (CNRS, ISTerre, Grenoble, France).
#
#  nathanael.schaeffer@univ-grenoble-alpes.fr
#
#  This software is governed by the CeCILL license under French law and
#  abiding by the rules of distribution of free software. You can use,
#  modify and/or redistribute the software under the terms of the CeCILL
#  license as circulated by CEA, CNRS and INRIA at the following URL
#  "http://www.cecill.info".
#
#  The fact that you are presently reading this means that you have had
#  knowledge of the CeCILL license and that you accept its terms.
#

"""XSHELLS Python/Matplotlib plotting module to load and display xspp output."""

import numpy as np
from numpy import sin,cos,arccos,sqrt,pi

## test if we are displaying on screen or not.
import os
nodisplay = True
if 'DISPLAY' in os.environ:
    if len(os.environ['DISPLAY']) > 0:
        nodisplay = False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description='XSPP Python module to load and display xspp output.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('fnames', nargs='+', default=None,
                        help='list of files to display (one figure per file)')
    parser.add_argument('--nodisplay', action='store_true',
                        help='set to inhibit display of the figure (forces a save)')
    parser.add_argument('-z', '--zoom', type=str, default="1",
                        help='zoom level for color bar')
    parser.add_argument('-c', '--components', type=str, default="",
                        help='component list to display')
    clin = parser.parse_args()
    nodisplay = nodisplay + clin.nodisplay

try:
    import matplotlib
    if nodisplay:
        matplotlib.use("Agg")

    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    from matplotlib import cm
    #cmap = cm.PuOr
    #cmap = cm.Spectral_r
    #cmap = cm.BrBG
    #cmap = cm.PiYG
    cmap = plt.cm.RdBu_r
    #cmap = cm.seismic
    #cmap = cm.afmhot
    #cmap = cm.gist_heat

    # a cool formatter:
    fmt=ticker.ScalarFormatter(useMathText=True)
    fmt.set_powerlimits((-3,3))
    # simple formatter:
    #fmt="%g"

    ## tuning
    #rc("font", family="sans")
    #rc("font", size=14)
    #rc('text', usetex=1)
    #rc('mathtext', fontset='stix')

    ## try to uncomment if you have problems with latex fonts.
    #from matplotlib import rcParams
    #rcParams['text.usetex']=True
    #rcParams['text.latex.unicode']=True

except:
    cmap, fmt, plt = None,None,None
    print("[xsplot] Warning: matplotlib not found, trying gnuplot instead (line plots only).")
    if __name__ != "__main__":
        print("[xsplot] Note that xsplot provides a basic matplotlib-like interface: xsplot.plot(), xsplot.show(), ...")


#########################################################################################################################################
#### functions for plotting that mimic the matplotlib interface, but uses gnuplot and also forwards to matplotlib (plt) if available ####
def plot(x,y,label=""):
    if plt is not None: plt.plot(x,y,label=label)
    plot.data.append((x,y,label))
plot.data = []      # record the data to plot in these variables attached to the plot function.
plot.opts = {}      # same for the plot options.
def yscale(a):
    if plt is not None: plt.yscale(a)
    if a == 'log':  plot.opts["logscale y 10"] = None
    elif "logscale y 10" in plot.opts:   del plot.opts["logscale y 10"]
def xlabel(a):
    if plt is not None: plt.xlabel(a)
    plot.opts["xlabel"] = a
def title(a):
    if plt is not None: plt.title(a)
    plot.opts["title"] = a
def grid(which='both'):
    if plt is not None: plt.grid(which=which)
    if "grid" in plot.opts:  del plot.opts["grid"]
    else:  plot.opts["grid"] = None
def legend(loc='best'):
    if plt is not None: plt.legend(loc=loc)
def render_gnuplot(fname=None, wait=True):
    if len(plot.data) == 0: return
    import subprocess
    try:
        gnuplot = subprocess.Popen(["/usr/bin/gnuplot"], stdin=subprocess.PIPE)
    except:
        return
    if fname is not None:   # write to png file
        gnuplot.stdin.write(b"set terminal png\n")
        gnuplot.stdin.write(b"set output '%s'\n" % fname.encode())
    elif nodisplay:     # write to ascii terminal
        gnuplot.stdin.write(b"set term dumb size 150 28 ansi\n")   # color output with: 'ansi' or 'ansi256'. b&w ouput with 'mono' or nothing.
        gnuplot.stdin.write(b"set colorsequence classic\n")
        gnuplot.stdin.write(b"set tics nomirror scale 0.3\n")
    gnuplot.stdin.write(b"set style data lines\n")
    gnuplot.stdin.write(b"set key above\n")
    for k in plot.opts.keys():
        if plot.opts[k] is not None:
            gnuplot.stdin.write(b"set %s '%s'\n" % (k.encode(), plot.opts[k].encode()))
        else:
            gnuplot.stdin.write(b"set %s\n" % k.encode())
    gnuplot.stdin.write(b"plot '-' using 1:2 title '%s' with linespoints" % plot.data[0][2].encode())
    for k in range(1,len(plot.data)):
        gnuplot.stdin.write(b", '-' using 1:2 title '%s' with linespoints" % plot.data[k][2].encode())
    gnuplot.stdin.write(b"\n");
    for k in range(0,len(plot.data)):
        for (i,j) in zip(plot.data[k][0],plot.data[k][1]):
            gnuplot.stdin.write(b"%g %g\n" % (i,j))
        gnuplot.stdin.write(b"e\n")
    gnuplot.stdin.flush()
    if fname is None:   # ascii or x11
        if not nodisplay:  gnuplot.stdin.write(b"pause mouse close\n")  # x11
        elif plt is not None:
            plt.savefig('xsplot.png')   # ascii: also save to png with matplotlib
            fname='xsplot.png'
        else:   # ascii: also save to png with gnuplot
            gnuplot.stdin.write(b"set terminal png\n")
            gnuplot.stdin.write(b"set output 'xsplot.png'\n")
            gnuplot.stdin.write(b"replot\n")
            fname='xsplot.png'
    gnuplot.stdin.write(b"quit\n")
    if wait:    gnuplot.communicate()   # wait for plot to finish
    if nodisplay:
        print(" => plot saved to '%s'" % fname)
def show():
    if (not nodisplay) and (plt is not None):  plt.show()   # x11 with matplotlib
    else:  render_gnuplot()    # x11 or terminal with gnuplot
def savefig(fname):
    if plt is not None:  plt.savefig(fname)     # save to file with matplotlib
    else:  render_gnuplot(fname=fname)     # save to file with gnuplot
def figure():
    if plt is not None:  plt.figure()
    if nodisplay or plt is None:
        render_gnuplot(wait=False)  # display the current data before starting the new figure!
    plot.data, plot.opts = [], {}
def loglog(x,y,label=""):
    plot.opts["logscale y 10"] = None
    plot.opts["logscale x 10"] = None
    if plt is not None:
        plt.yscale('log')
        plt.xscale('log')
    plot(x,y,label)
### matlplotlib replacement ends ###


def get_levels(mi,ma, nlevels, czoom):
    if isinstance(czoom, tuple):
        levels = np.linspace(czoom[0],czoom[1],nlevels+1)
        ext = 'both'
    else:
        if (mi<0) and (ma>0):
            m = max(-mi,ma)
            mi,ma = -m,m    # symmetric color scale
        if czoom == 1:
            levels = np.linspace(mi,ma,nlevels+1)
            ext = 'neither'
        else:
            c = (ma+mi)/2
            d = (ma-mi)/2
            levels = np.linspace(c-d/czoom,c+d/czoom,nlevels+1)
            ext = 'both'
    return levels, ext


def load_merid(file,ang=0):
    """ r,cost,V = load_merid(file,ang=0). If ang=1 : convert Up to angular velocity, if ang=2 convert Ut to angular velocity."""
    print('loading',file)
    a=np.loadtxt(file,comments='%')
    s = a.shape
    ir0 = 1

    ct = a[0,1:s[1]].reshape(1,s[1]-1)
    r = a[ir0:s[0],0].reshape(s[0]-ir0,1)

    a = a[ir0:s[0],1:s[1]]

    if ang > 0:
        st = sqrt(1-ct*ct)
        x = r*st
        y = r*ct
        #convert Up to angular velocity
        if (ang==1):
            print( np.amax(abs(x)) )
            a=a/x
            a[:,s[1]-2] = a[:,s[1]-3]   #remove nan
            a[:,0] = a[:,1]         #remove nan
        # convert Ut to angular velocity
        if (ang==2):
            a=a/sqrt(square(x) + square(y))

    return r,ct,a

def plot_merid(r,ct,a, strm=0, czoom=1, rg=0, rm=0, shift=0, title='', levels=20, cbar=1, cmap=cmap):
    """ m = plot_merid(r,ct,a, czoom=1, rg=0, rm=0, shift=0, title='')"""

    r = r.reshape(r.size,1)
    ct = ct.reshape(1,ct.size)
    st = sqrt(1-ct*ct)
    x = r*st
    y = r*ct + 1.1*shift

    mi,ma = np.amin(a), np.amax(a)
    m = max(-mi,ma)
    print('max value=',m)

    if m>0:
        levels, ext = get_levels(mi,ma, levels, czoom)
        plt.contourf(x,y,a,levels,cmap=cmap, extend=ext)

    theta = np.linspace(-pi/2,pi/2,100)
    if rg>0:
        plt.plot(rg*cos(theta)+1.1*shift,rg*sin(theta),color='gray')
    if rm>0:
        plt.plot(rm*cos(theta)+1.1*shift,rm*sin(theta),color='gray')

    plt.axis('equal')
    plt.axis('off')
    if m>0 and cbar>0:
        plt.colorbar(orientation='vertical',fraction=0.07,pad=0.02,format=fmt)

    ms = np.amax(abs(strm))
    if ms > 0:          # plot contour of strm (stream lines)
        lev2 = arange(ms/18,ms,ms/9)
        plt.contour(np.array(x),np.array(y),strm,lev2,colors='k')
        plt.contour(np.array(x),np.array(y),strm,flipud(-lev2),colors='k')

    if title != '':
        rmax = np.amax(r)
        plt.text(0.75*rmax+1.1*shift,0.8*rmax,title, fontsize=28)

    return m


def load_disc(file,mres=1):
    """ r,phi, vr,vp,vz = plot_disc(file, mres=1)"""
    print('loading',file)
    a=np.loadtxt(file,comments='%')
    s = a.shape
    ir0 = 0

    n0 = int((s[1]-1)/3)
    Np = mres*n0 +1
    ip = np.mgrid[0:Np]
    ip[len(ip)-1] = 0   # ip loops around
    phi = ip*2*pi/(Np-1)
    for i in range(1, mres):
        ip[(i*n0):((i+1)*n0)] = ip[0:n0]    # when mres > 1, we need to copy data around
    r = a[ir0:s[0],0].reshape(s[0]-ir0,1)

    vr = a[:, 1+ip*3]
    vp = a[:, 2+ip*3]
    vz = a[:, 3+ip*3]

    return r,phi, vr,vp,vz


def plot_disc(r,phi,b, czoom=1, rg=0, rm=0, title='',cmap=cmap, levels=20):
    """ plot_disc(r,phi,v, czoom=1, rg=0, rm=0, title='')"""

    r = r.reshape(r.size,1)
    phi = phi.reshape(1,phi.size)
    x = r*cos(phi)
    y = r*sin(phi)

    mi,ma = np.amin(b), np.amax(b)
    m = max(-mi,ma)
    print('max value=',m)
    if m > 0.0:
        levels, ext = get_levels(mi,ma, levels, czoom)
        p = plt.contourf(x,y,b,levels,cmap=cmap, extend=ext)
        plt.axis('equal')
        plt.axis('off')

        #if czoom == 1:
            #clim(-m/czoom,m/czoom)
        #plt.subplots_adjust(left=0.02, bottom=0.02, right=0.98, top=0.98, wspace=0.1, hspace=0.1)
        plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.2, hspace=0.2)
        #fmt = ticker.FormatStrFormatter("%.3e")
        fmt=ticker.ScalarFormatter(useMathText=True)
        fmt.set_powerlimits((-3,3))
        plt.colorbar(format=fmt)

        theta = np.linspace(-pi/2,pi/2,100)
        if rg>0:
            plt.plot(rg*cos(theta),rg*sin(theta),color='gray')
            plt.plot(-rg*cos(theta),rg*sin(theta),color='gray')
        if rm>0:
            plt.plot(rm*cos(theta),rm*sin(theta),color='gray')
            plt.plot(-rm*cos(theta),rm*sin(theta),color='gray')
        if title != '':
            plt.figtext(0.65, 0.9, title, fontsize=28)

    return m

def load_surf(file):
    """ theta,phi, ur,ut,up = load_surf(file)"""
    print('loading',file)
    a=np.loadtxt(file,comments='%')
    s = a.shape

    t = a[0,1:s[1]:3]
    t = t * 180./pi
    p = a[1:s[0],0]
    p = p * 180./pi

    ur = a[1:s[0],1::3].T   # transpose
    ut = a[1:s[0],2::3].T
    up = a[1:s[0],3::3].T

    return t,p,ur,ut,up


def plot_surf(theta, phi, vx, czoom=1, rg_r=0, title='', cmap=cmap, levels=20, whole=True):
    """ Aitoff projection: plot_surf(theta, phi, vx, czoom=1, rg_r=0, title='', cmap=cmap, levels=20, whole=True ) where theta and phi are latitude and longitude in degrees."""

    mi,ma = np.amin(vx), np.amax(vx)
    m = max(-mi,ma)
    print('max value=',m)
    if m > 0.0:
        t = (90.-theta)*pi/180.

        p = phi.reshape(phi.size)
        mres=1
        while p[-1]*(mres+1) <= 360: mres+=1    # find mres
        print('mres =',mres)
        if whole and mres>1:
            ip = np.mgrid[0:phi.size*mres+1]
            ip = np.mod(ip,phi.size)   # ip loops around
            p = np.linspace(-pi/2,pi/2, ip.size)     # assumes a regular grid in phi
        else:
            ip = np.mgrid[0:phi.size+1]
            ip[-1] = 0   # ip loops around
            p = (p[ip] - 180)*pi/360  # longitude
            p[-1] = pi/2         # last phi value.
            if mres>1:     # partial surface coverage, do some correction
                p[-1] = p[-2] + (p[1]-p[0])
                p -= (p[-1]+p[0])/2

        t = t.reshape(t.size, 1)
        p = p.reshape(1, p.size)
        print('=> Aitoff projection')
        al = arccos(cos(t)*cos(p))
        al = al / sin(al)
        x = 2*al * (cos(t)*sin(p))
        y = al * (sin(t)*(p*0+1))

        if rg_r > 0:        # compute the tangent cylinder.
            pp = np.linspace(-pi/2,pi/2,100)
            tt = arccos(rg_r)
            al = arccos(cos(tt)*cos(pp))
            al = al / sin(al)
            xg = 2*al * (cos(tt)*sin(pp))
            yg = al * (sin(tt)*(pp*0+1))

        b = vx[:,ip]

        levels, ext = get_levels(mi,ma, levels, czoom)
        plt.contourf(x,y,b,levels,cmap=cmap, extend=ext)

        plt.axis('equal')
        plt.axis('off')
        #plt.subplots_adjust(left=0.02, bottom=0.1, right=0.98, top=0.95, wspace=0.1, hspace=0.1)
        #plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.2, hspace=0.2)
        #plt.subplots_adjust(left=0.01, bottom=0.1, right=0.99, top=0.99, wspace=0.2, hspace=0.2)
        cb=plt.colorbar(orientation='horizontal',fraction=0.05,pad=0.01,format=fmt)
    #   cb.ax.yaxis.get_major_locator()._nbins=4
    #   plt.clim(-m/czoom,m/czoom)
        plt.xlim(-3.2,3.2)
        plt.ylim(-1.6,1.6)

        if rg_r > 0:        # show the tangent cylinder.
            plt.plot(xg,yg,color='gray')
            plt.plot(xg,-yg,color='gray')

        plt.plot(2*p,p*0,color='gray',linestyle='dashed');  # show equator
        if title != '':
            plt.text(2.6, 1.2, title, fontsize=20 )

    return m

def stream_surf(theta, phi, vt, vp, col=0, czoom=1, rg_r=0, projection='aitoff', cmap=cmap):
    """ streamlines and colormap with projection: stream_surf(theta, phi, vt, vp, col, czoom=1, rg_r=0, title='', projection='aitoff' )"""

    vm=sqrt(np.amax(vt*vt + vp*vp))
    print('max vector value=',vm)
    mi,ma = np.amin(col), np.amax(col)
    m = max(-mi,ma)
    print('max scalar value=',m)

    ax=subplot(111,projection=projection)
    if (vm+m) > 0.0:
        t = (90.-theta)*pi/180.

        phi = phi.reshape(phi.size)
        ip = np.mgrid[0:phi.size+1]
        ip[ip.size-1] = 0   # ip loops around
        p = (phi[ip] - 180.)*pi/180.    # longitude
        p[ip.size-1] = pi           # last phi value.

        t = t.reshape(t.size, 1)
        p = p.reshape(1, p.size)
        print('=> %s projection' % projection)
        x = ones(t.shape)*p
        y = t*ones(p.shape)

        strmcol='k'

        if m>0:
            d = col[:,ip]
            levels, ext = get_levels(mi,ma, 10, czoom)
            plt.pcolormesh(x,y,d,shading='gouraud',cmap=cmap)
            plt.clim(levels[0],levels[-1])
            cb=plt.colorbar(orientation='horizontal',fraction=0.05,pad=0.05,format=fmt)
            cb.ax.yaxis.get_major_locator()._nbins=4
            strmcol='m'     # better seen when there is a colormap in the background...

        if vm>0:
            b = vp[:,ip]
            c = -vt[:,ip]*sin(pi/2-y)       ## mulitply by sin(theta) to workaround a bug
            v2=sqrt(b*b + c*c)
            plt.streamplot(x,y,b,c, color=strmcol,linewidth=v2*(5./vm))

        plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='off') # labels along the bottom edge are off

    return m+vm

def plot_spec(filename,ir_list=None):
    """loads a spectrum as saved by xspp"""
    sp = np.loadtxt(filename, comments='%')
    r = sp[:,0]				# radius
    nr = sp.shape[0]
    if ir_list is None:
        ir_list = [10,nr//2,nr-11]		# list of radius indices to plot

    with open(filename) as f:
        a = f.readline()
        if a.startswith('% [XSHELLS] Energy spectrum : MMAX='):
            l = np.arange(0, sp.shape[1]-1)
            for ir in ir_list:
                loglog(l, sp[ir,1:], label="r=%g" % r[ir])
            xlabel('$\ell$')

        if a.startswith('% [XSHELLS] Energy spectrum : LMAX='):
            m = np.arange(0, sp.shape[1]-1) + 1
            for ir in ir_list:
                loglog(m, sp[ir,1:], label="r=%g" % r[ir])
            xlabel('$m+1$')

        grid(which='both')
        legend(loc='best')

def clean_diags(data):
    """Remove jumps back in time and duplicate times due to restarts of computation. Operates in-place on the dictionary returned by load_diags()."""
    if not 't' in data:
        return
    #### find restarts that jump back in time:
    t = data['t']
    ix = np.where(t[1:] < t[:-1])[0]   # find jumps back in time
    n = len(ix)
    count = 0
    while n > 0:
        i1 = ix[n-1]+1     # index of time of last restart
        i0 = np.argmax(t[:i1] >= t[i1])  # find first time matching the last restart time
        for k in data.keys():
            data[k] = np.delete(data[k], np.s_[i0:i1])    # delete duplicate range
        count += 1
        while n>0 and ix[n-1] > i0:  n -= 1    # skip restarts in the already deleted range
    if count > 0:  print('%d jumps back in time cleaned' % count)

    #### find normal restarts:
    t = data['t']
    ix = np.where(t[1:] == t[:-1])[0]    # find normal restarts
    if (len(ix) > 0):
        for k in data.keys():
            data[k] = np.delete(data[k], ix)   # remove duplicate values due to restarts
        print('%d normal restarts cleaned' % len(ix))

    #### double check that we are clean now:
    t = data['t']
    ix = np.where(t[1:] <= t[:-1])[0]    # is the record clean now?
    if len(ix) > 0:  print('cleaning failed !')

def load_diags(filename, print_header=True, clean=True):
    """returns a dictionary of time series for easy lookup (or a numpy array if no header found)"""
    import re   # regular expression
    RE=re.compile(r'[,\s\t]+')  # regex to split up header fields
    d = {}      # empty dict

    def update_dict(data, header, ntimes):
        header = header.lstrip('% \n')        # the header
        field=RE.split(header)[0:-1]
        ntimes += data.shape[0]
        for i in range(0,len(field)):
            x=np.empty(ntimes)
            x[:] = np.nan
            x[-data.shape[0]:] = data[:,i]
            if field[i] in d:       # field name already exists:
                xo = d[field[i]]    # previous field data
                if len(xo) == ntimes:    # this is a name collision, needs disambiguation:
                    field[i] = '%s_%d' % (field[i],i)
                else:
                    x[0:len(xo)] = xo   # keep previous field data
            d[field[i]] = x
        return ntimes

    f = open(filename, 'r')
    h = f.readline()
    lno = 1
    while len(h)<3:  h,lno = f.readline(), lno+1   # skip empty lines
    header = None
    param = None
    ### custom reading loop, which is more than 2 times faster than loadtxt or genfromtxt.
    l=[]
    ncol, ntimes = 0, 0
    while h != '':
        if h[0] != '%':
            icmt = h.find('%')   # is there a comment?
            if icmt>0:  h=h[:icmt]    # remove comment
            try:
                ll = np.array(h.split(),dtype=np.float64)
                if ncol == 0:
                    ncol = len(ll)
                if len(ll) == ncol:
                    l.append(ll)
                else:
                    raise ValueError
            except ValueError:
                print("Warning: malformed line %d skipped" % lno)
        elif h.startswith('%PAR%'): # we have a parameter list
            if print_header and h != param: print(h)
            param = h
        elif h != header:   # we have a new different header !
            if ncol > 0:    # we already have some data
                ntimes = update_dict(np.array(l), header, ntimes)
                l=[]
                ncol=0
            header = h    # new header
            if print_header: print(header)
        h = f.readline()
        lno += 1
    data = np.array(l)
#   data = loadtxt(filename,comments='%')      # load data
    if header is not None:        # there is a header
        ntimes = update_dict(data, header, ntimes)
        data = d
        if clean:  clean_diags(data)
#   data = genfromtxt(filename, comments='%', names=True)   # faster than loadtxt
    return data

def get_slice_name(tag):
    comp = { 0: '', 1: '_r', 2: r'_\theta', 3: r'_\phi', 4: '_s', 5: '_x', 6: '_y', 7: '_z', 8: '_P', 9: '_T', 15: '_{rms}' }
    tag = int(tag)
    if (tag&15) in comp.keys():
        name = comp[tag&15]
    else: name = ''
    if (tag>>4)&4095 > 0:
        name = chr(((tag >> 4)&63) +64) + name
        if (tag >> 10)&63 > 0:
            name = chr(((tag >> 10)&63) +64) + name
    return name

def load_slice_npy(filename):
    """load a field slice produced by xspp in numpy format, return a dictionary with coordinates and fields"""
    a = np.load(filename)      # load numpy data directly
    if len(a.shape) == 2:
        a = a.reshape(1,a.shape[0],a.shape[1])  # tolerance for 1 component data stored as 2D array.
    x = a[0,1:,0]
    y = a[0,0,1:]
    data = a[:,1:,1:]
    d = {}      # dictionary
    # identify slice type
    plottype = int(a[0,0,0]) >> 16
    if plottype == 0:      # a merid slice
        d['r'], d['theta'] = x, y
    elif plottype == 1:    # a disc slice (periodic)
        b=np.empty_like(a)
        b[:,:,0:-1] = a[:,:,1:]             # copy
        b[:,:,-1]   = a[:,:,1]              # loop around
        b[:,0,-1]   = 2*b[:,0,-2]-b[:,0,-3] # next phi-step (not necessarily a full disc)
        d['r'], d['phi'] = x, b[0,0,:]
        data = b[:,1:,:]
    elif plottype == 2:    # a spherical slice
        d['theta'], d['phi'] = y, x
        data = np.transpose(data, (0,2,1))  # [exchange axis 1 and 2]
    d['data'] = data
    name = [] # empty list
    for i in range(0, a.shape[0]):
        # decode field name and component
        name.append(get_slice_name(int(a[i,0,0])))
    d['name'] = name
    return d

### utility function to invert a color-map
def invert_cmap(cmap,i=[0,1,2]):
    from matplotlib.colors import ListedColormap
    x=np.linspace(-1,1,256)
    x=np.abs(x)**(0.8)*np.sign(x)   # avoid too much dark in the middle
    cmap_orig = cm.get_cmap(cmap,256)((x+1.)/2.)
    new = cmap_orig.copy()
    new[:,[0,1,2]] = 1. - cmap_orig[:,i]
    return ListedColormap(new)

def get_cmap(name=''):
    #from matplotlib.colors import LinearSegmentedColormap
    #cmap = LinearSegmentedColormap.from_list('berlin', np.loadtxt('python/tofino.txt'))
    cmap = cm.RdBu_r
    #cmap = invert_cmap(cm.RdBu_r,[2,1,0])   # BuKY : blue-black-yellow
    #cmap = invert_cmap(cm.RdBu)
    #cmap = invert_cmap(cm.PuOr_r,[2,0,1])
    #cmap = invert_cmap(cm.RdBu,[1,0,2])
    if len(name) > 0:
        if   name[0] == 'T':  cmap = cm.inferno   # temperature
        elif name[0] == 'C':  cmap = cm.viridis   # composition
        #elif name[0] == 'B':  cmap = cm.PRGn_r    # magnetic field
        elif name[0] == 'B':  cmap = invert_cmap(cm.PuOr,[2,1,0])    # magnetic field
        #elif name[0] == 'B':  cmap = cm.BrBG    # magnetic field
        #elif name[0] == 'B':  cmap = invert_cmap(cm.RdBu,[2,1,0])    # magnetic field
        #elif name[0] == 'B':  cmap = invert_cmap(cm.PuOr,[2,0,1])    # magnetic field
        #elif name[0] == 'B':  cmap = invert_cmap(cm.RdBu,[1,0,2])    # magnetic field
    return cmap

def plot_slice(y, i=0, czoom=1, title_prefix='', levels=20, cmap=None, name=None):
    """plot a field slice produced by xspp in numpy format"""
    if type(y) == str:      # if filename, load it
        y = load_slice_npy(y)
    # choose colormap:
    if cmap is None:
        cmap = get_cmap(y['name'][i])
    # choose correct plot type
    if 'r' in y.keys():
        if 'theta' in y.keys():  # a merid plot
            plot_merid(y['r'], cos(y['theta']), y['data'][i,:,:], cmap=cmap, czoom=czoom, levels=levels)
        elif 'phi' in y.keys():  # a disc plot (periodic)
            plot_disc(y['r'], y['phi'], y['data'][i,:,:], cmap=cmap, czoom=czoom, levels=levels)
    elif 'theta' in y.keys() and 'phi' in y.keys():    # a surf plot
        plot_surf(y['theta']*180./pi, y['phi']*180./pi, y['data'][i,:,:], cmap=cmap, czoom=czoom, levels=levels)
    if y['name'][i] != '':
    	title( title_prefix + '$' + y['name'][i] + '$' )
    return name

def slice2vtk(fname_vtk, y, phi=0, r=1, z=0):
    """export a slice or slices (special numpy arrays from xspp) to vtk format for paraview.
        The second parameter 'y' is a numpy array directly loaded from a slice, or a tuple of several such arrays. Do NOT use load_slice_npy()!
    """
    try:    # somtimes the module is named pyevtk, and sometimes evtk. Try both.
        from pyevtk.hl import structuredToVT
    except ImportError:
        from evtk.hl import structuredToVTK
    def add_periodic(y):
        a=np.empty_like(y)
        a[:,:,0:-1] = y[:,:,1:]           # copy
        a[:,:,-1] = y[:,:,1]              # loop around
        a[:,0,-1] = 2*a[:,0,-2]-a[:,0,-3]     # next phi-step (not necessarily a full disc)
        phi = a[0,0,:].reshape(1,-1)
        a = a[:,1:,:]       # remove phi coordinate from data
        return a, phi

    if type(y) == tuple:
        y = np.vstack(y)
    tags = y[:,0,0].astype(int)
    slicetype = tags >> 16
    ## assign field names:
    names = []
    for tag in tags:
        name = get_slice_name(tag)
        names.append(name.replace('_','').replace('\\','').replace('{','').replace('}',''))

    pd = {}
    if all(slicetype == 0):     # a meridian cut
        r = y[0,1:,0].reshape(-1,1)
        th = y[0,0,1:].reshape(1,-1)
        st,ct = sin(th),cos(th)
        sp,cp = sin(phi),cos(phi)
        n1,n2 = y.shape[1]-1, y.shape[2]-1

        for k in range(y.shape[0]):
            if (tags[k]&15) in (0,1,2,3):       # scalar, and r,theta,phi components only.
                pd[names[k]] = y[k,1:,1:].reshape(-1, n2, 1).copy()
        # detect and handle vectors:
        for k in range(y.shape[0]-2):
            if all((tags[k:k+3] & 15) == np.array([3,4,7])):     # phi,s,z
                vx = y[k+1,1:,1:]*cp - y[k,1:,1:]*sp
                vy = y[k+1,1:,1:]*sp + y[k,1:,1:]*cp
                pd[names[k+1][:-1]] = (vx.reshape(-1, n2, 1).copy(), vy.reshape(-1, n2, 1).copy(), y[k+2,1:,1:].reshape(-1, n2, 1).copy())
    elif all(slicetype == 1):   # a disc (periodic), coords are s,phi,z
        a, phi = add_periodic(y)
        r = y[0,1:,0].reshape(-1,1)
        sp,cp = sin(phi),cos(phi)
        st,ct = 1., 0.
        n1,n2 = y.shape[1]-1, y.shape[2]

        for k in range(y.shape[0]):
            pd[names[k]] = a[k,:,:].reshape(-1, n2, 1).copy()
        # detect and handle vectors:
        for k in range(y.shape[0]-2):
            if all((tags[k:k+3] & 15) == np.array([4,3,7])):     # s,phi,z
                vx = a[k,:,:]*cp - a[k+1,:,:]*sp
                vy = a[k,:,:]*sp + a[k+1,:,:]*cp
                pd[names[k][:-1]] = (vx.reshape(-1, n2, 1).copy(), vy.reshape(-1, n2, 1).copy(), a[k+2,:,:].reshape(-1, n2, 1).copy())
    elif all(slicetype == 2):   # a shpere
        y = y.swapaxes(1,2)
        a, phi = add_periodic(y)
        th = y[0,1:,0].reshape(-1,1)
        sp,cp = sin(phi),cos(phi)
        st,ct = sin(th),cos(th)
        n1,n2 = y.shape[1]-1, y.shape[2]

        for k in range(y.shape[0]):
            pd[names[k]] = a[k,:,:].reshape(-1,n2,1).copy()
        # detect and handle vectors:
        for k in range(y.shape[0]-2):
            if all((tags[k:k+3] & 15) == np.array([1,2,3])):     # r,theta,phi
                vz = a[k,:,:]*ct - a[k+1,:,:]*st
                vs = a[k,:,:]*st + a[k+1,:,:]*ct
                vx = vs*cp - a[k+2,:,:]*sp
                vy = vs*sp + a[k+2,:,:]*cp
                pd[names[k][:-1]] = (vx.reshape(-1, n2, 1).copy(), vy.reshape(-1, n2, 1).copy(), vz.reshape(-1, n2, 1).copy())
    else:
        print("slice2vtk ERROR !")

    X = np.empty( (n1, n2, 1), dtype='float32' )   # store as float32
    Y = np.empty_like(X)
    Z = np.empty_like(X)
    X[:,:,0] = r*st*cp
    Y[:,:,0] = r*st*sp
    Z[:,:,0] = r*ct + z
    structuredToVTK(fname_vtk, X, Y, Z, pointData = pd)


if __name__ == "__main__":
    pos = None      # positivity flag
    czoom = eval(clin.zoom)
    figsze = (12,8)
    px = ''
    for fn in clin.fnames:
        print(fn)
        if fn.endswith(".npy"):     # we have a new numpy file format
            a = load_slice_npy(fn)    # load numpy data
            comp = range(0,a['data'].shape[0])
            if clin.components != '':
                comp = eval(clin.components + ',')
            print(comp)
            for idx in comp:
                if np.amax(abs(a['data'][idx,1:,1:])) > 0:
                    plt.figure(figsize=figsze)
                    if len(clin.fnames) > 1:    # include filename in title if we have more than one
                        px = fn + ' '
                    plot_slice(a, idx, czoom=czoom, title_prefix=px)
                    if nodisplay:
                        plt.savefig(fn.replace('.npy', '-%d.png' % idx))
                else:
                    print('zero')
        else:
            with open(fn) as f:
                a = f.readline()
                while len(a)<3: a=f.readline()    # skip empty lines
                if a == '%plot_merid.py\n':
                    plt.figure(figsize=figsze)
                    plot_merid(*load_merid(fn), czoom=czoom)
                    plt.title(fn)
                if a == '%plot_disc.py\n':
                    r,phi, vr,vp,vz = load_disc(fn)
                    vv = (vr,vp,vz)
                    ss = (r"$s$",r"$\phi$",r"$z$")
                    comp = (0,1,2)
                    if clin.components != '':
                        comp = eval(clin.components + ',')
                    for idx in comp:
                        v,s = vv[idx],ss[idx]
                        if np.amax(abs(v)) > 0:
                            plt.figure(figsize=figsze)
                            plot_disc(r, phi, v, czoom=czoom)
                            plt.title("%s %s" % (fn,s))
                if a == '%plot_surf.py\n':
                    t,p,vr,vt,vp = load_surf(fn)
                    vv = (vr,vt,vp)
                    ss = (r"$r$",r"$\theta$",r"$\phi$")
                    comp = (0,1,2)
                    if clin.components != '':
                        comp = eval(clin.components + ',')
                    for idx in comp:
                        v,s = vv[idx],ss[idx]
                        if np.amax(abs(v)) > 0:
                            plt.figure(figsize=figsze)
                            plot_surf(t, p, v, czoom=czoom)
                            plt.title("%s %s" % (fn,s))
                if a.startswith('% [XSHELLS] Energy spectrum'):
                    irlist = None
                    if clin.components != '':
                        irlist = eval(clin.components + ',')
                        print(irlist)
                    figure()
                    plot_spec(fn,ir_list=irlist)
                if a.lstrip('% \n')[0] == 't':     # energy and diagnostics file
                    if pos is None: pos=True
                    d = load_diags(fn)
                    t = d['t']
                    job = fn
                    if fn.startswith('energy.'):
                        job = job[7:]
                    keys = ('Eu','Eb')
                    if clin.components != '':
                        keys = clin.components.replace(',',' ').split()
                    for k in keys:
                        plot(t, d[k], label=k + ' ' + job)
                        if any(d[k] < 0.0): pos=False
                    if pos: yscale('log')
                    xlabel('t')
                    grid()
                    legend(loc='best')
                    title(job)
                elif a.startswith('% [XSHELLS] line'):     # profile along a line
                    d = load_diags(fn)
                    alpha = d['alpha']
                    job = fn
                    keys = ('vr','vt','vp','value')
                    if clin.components != '':
                        keys = clin.components.split(',')
                    for k in keys:
                        try:
                            plot(alpha, d[k], label=k + ' ' + job)
                        except:
                            pass
                    xlabel('alpha')
                    grid()
                    legend(loc='best')
                    title(job)
                elif nodisplay:
                    savefig(fn + '.png')

    if pos is not None:
        yscale('log' if pos else 'linear')
    show()  # always works.
