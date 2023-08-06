#
#  Copyright (c) 2010-2016 Centre National de la Recherche Scientifique.
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

"""Python module to handle Xshells fields."""

from numpy import *
import os
import struct
import shtns


class Grid:
    """ a radial grid + finite difference approximation to derivatives. """
    def update_deriv(self):
        nr = len(self.r)
        self.Gr = zeros((nr,3))     # gradient
        self.Lr = zeros((nr,3))     # laplace radial d2/dr2 + 2/r.d/dr
        for ir in range(1, nr-1):
            drm = self.r[ir] - self.r[ir-1]
            drp = self.r[ir+1] - self.r[ir]
            t = 1.0/((drm+drp)*drp*drm)
            self.Gr[ir,0] = -drp*drp*t
            self.Gr[ir,1] = (drp*drp - drm*drm)*t
            self.Gr[ir,2] = drm*drm*t
            self.Lr[ir,:] = self.Gr[ir,:]*2./self.r[ir]
            self.Lr[ir,0] += 2.*drp*t
            self.Lr[ir,1] -= 2.*(drm+drp)*t
            self.Lr[ir,2] += 2.*drm*t

    def r_to_idx(self, rr):
        """ return the index in the grid for which the radius is the closest to rr."""
        i = len(grid)-2;
        while (grid[i] > rr) and (i>0):
            i -= 1
        if (rr-grid[i]) > (grid[i+1]-rr):
            i += 1;
        return i;	# i is always between 0 and len(grid)-1

    def __init__(self, r_array):
        self.r = r_array.copy()
        self.r.flags.writeable = False      # protect from overwriting
        self.update_deriv()

    def __repr__(self):
        return 'xshells grid, ro={}, rf={}, nr={}'.format(self.r[0], self.r[-1], len(self.r))

class Spectral:
    """A spectral field (can be scalar or poloidal/toroidal)."""
    def __init__(self, grid, sht):
        self.grid = grid
        if isinstance(sht, tuple):
            self.lmax = sht[0]
            self.mmax = sht[1]
            self.mres = sht[2]
            if self.lmax > 1:
                self.sht = shtns.sht(self.lmax, self.mmax, self.mres)
                l, m = self.sht.l, self.sht.m
            else:
                l = arange(0,self.lmax+1)
                m = l*0.0
                if (self.mmax==1) and (self.mres==1):
                    l = hstack((l,arange(1,self.lmax+1)))
                    m = hstack((m,arange(1,self.lmax+1)))
        else:
            self.lmax = sht.lmax
            self.mmax = sht.mmax
            self.mres = sht.mres
            self.sht = sht
            l, m = sht.l, sht.m
        self.l = l
        self.m = m
        self.l2 = l*(l+1.0)
        self.curl = 0
        self.time = 0

    def __repr__(self):
        header = self.encode_header(self.ncomp(),
                                    shtns.nlm_calc(self.lmax, self.mmax, self.mres),
                                    self.data.dtype)
        header = struct.unpack('=16i8d64s832s', header)
        info = (('lmax', header[1]),
                ('mmax', header[2]),
                ('mres', header[3]),
                ('nlm', header[4]),
                ('nr', header[5]),
                ('ir', (self.irs,self.ire)),
                ('r', (self.grid.r[self.irs],self.grid.r[self.ire])),
                ('version', header[0]),
                ('BC', (header[8],header[9])),
                ('ncomp', header[13]),
                ('iter', header[14]),
                ('step', header[15]),
                ('time', header[19]),
                ('id', header[24].decode().strip('\x00')))
        return ', '.join(['='.join([str(a) for a in ent]) for ent in info])

    def __add__(self, other):
        assert all(self.grid.r == other.grid.r), 'spectral objects must be on same grid'
        assert self.ncomp() == other.ncomp(), 'spectral objects must have same number of components'
        out = clone_field(self, copy=True)
        out.data += other.data
        return out

    def __iadd__(self, other):
        assert all(self.grid.r == other.grid.r), 'spectral objects must be on same grid'
        assert self.ncomp() == other.ncomp(), 'spectral objects must have same number of components'
        self.data += other.data
        return self
        
    def __sub__(self, other):
        assert all(self.grid.r == other.grid.r), 'spectral objects must be on same grid'
        assert self.ncomp() == other.ncomp(), 'spectral objects must have same number of components'
        out = clone_field(self, copy=True)
        out.data -= other.data
        return out
        
    def __isub__(self, other):
        assert all(self.grid.r == other.grid.r), 'spectral objects must be on same grid'
        assert self.ncomp() == other.ncomp(), 'spectral objects must have same number of components'
        self.data -= other.data
        return self

    def __mul__(self, val):
        out = clone_field(self, copy=True)
        out.data *= val
        return out

    def __imul__(self, val):
        self.data *= val
        return self

    def __truediv__(self, val):
        out = clone_field(self, copy=True)
        out.data /= val
        return out

    def __itruediv__(self, val):
        self.data /= val
        return self

    def set_BC(self, bci, bco):
        self.BC = (bci, bco)

    def encode_header(s, nc, nlm, dtype, iteration=0, step=0):
        """prepare header for writing to a file."""
        r = s.grid.r
        irs = s.irs
        ire = s.ire
        if nlm==0:
            nlm = shtns.nlm_calc(s.lmax, s.mmax, s.mres)
        h = bytearray(1024)
        version = 12
        if dtype == complex64:
            version |= 4096     # mark as single precision
        struct.pack_into('=8i',h,0, version, s.lmax,s.mmax,s.mres,nlm,len(r), irs, ire)
        struct.pack_into('=8i',h,32, s.BC[0], s.BC[1], 0, 0, shtns.sht_orthonormal, nc, iteration, step)
        struct.pack_into('=8d9s',h,64, r[irs], r[ire], 0, s.time, 0,0,0,0, b'pyxshells')
        return h

    def alloc(self, irs, ire, ncomp, dtype=complex128, filename=None):
        self.irs = irs
        self.ire = ire
        nlm = shtns.nlm_calc(self.lmax, self.mmax, self.mres)
        if filename==None:
            self.data = zeros((ire-irs+3, ncomp, nlm), dtype=dtype) # alloc memory
        else:
            h = self.encode_header(ncomp, nlm, dtype)
            f = open(filename, "wb")    # create file
            f.write(h)                  # write header
            self.grid.r.astype(float64).tofile(f)       # write grid
            f.close()
            nr = len(self.grid.r)
            self.data = memmap(filename, dtype=dtype, mode='r+', shape=(ire-irs+3, ncomp, nlm), offset=1024+nr*8)       # data mapped to file

    def nelem(self):
        return self.data.shape[2]

    def ncomp(self):
        return self.data.shape[1]

    def nshells(self):
        return self.data.shape[0]

    def sh(self, ir, icomp=0):
        return self.data[ir - self.irs+1, icomp, :]

    def set_sh(self, S, ir, icomp=0):
        self.data[ir - self.irs+1, icomp, :] = S

    def r_spectrum(self, ir):
        v2 = self.r_energy(ir)
        if v2.ndim > 1:
            v2 = v2.sum(axis=0)      # merge pol and tor energies
        El = zeros(self.lmax+1)
        Em = zeros(self.mmax+1)
        for lm in range(0, self.nelem()):
            l=self.l[lm]
            m=self.m[lm]//self.mres
            El[l] += v2[lm]
            Em[m] += v2[lm]
        return El,Em

    def delta_r(self, ir):      # layer weight for radial integration.
        ir_p = ir+1
        ir_m = ir-1
        if ir == self.irs:
            ir_m = ir
        elif ir == self.ire:
            ir_p = ir
        return (self.grid.r[ir_p]-self.grid.r[ir_m])*0.5

    def shell_volume(self):     # volume occupied by field.
        return (4./3.*pi)*(self.grid.r[self.ire]**3 - self.grid.r[self.irs]**3)

    def energy(self):
        Etot = 0.0
        for ir in range(self.irs, self.ire+1):
            r2dr = square(self.grid.r[ir]) * self.delta_r(ir)
            Etot += r2dr * sum(self.r_energy(ir))
        return Etot

    def energy_split(self):
        Es,Ea,Ez,Enz = 0.,0.,0.,0.
        for ir in range(self.irs, self.ire+1):
            r2dr = self.grid.r[ir]**2 * self.delta_r(ir)
            v2 = self.r_energy(ir)
            Es += r2dr * sum(v2[...,(self.l-self.m)&1==0], axis=-1)
            Ea += r2dr * sum(v2[...,(self.l-self.m)&1==1], axis=-1)
            Ez += r2dr * sum(v2[...,self.m==0], axis=-1)
            Enz += r2dr * sum(v2[...,self.m>0], axis=-1)
        return array([Es, Ea, Ez, Enz])

    def rms(self):
        return sqrt(2.*self.energy()/self.shell_volume())

    def copy_data_from(self, src):
        """copy data from other field, with possibly different spherical harmonic truncation."""
        if any(src.grid.r[src.irs:src.ire] != self.grid.r[self.irs:self.ire]):
            raise Exception("radial domains mismatch")
        lmax = min(self.lmax, src.lmax)
        mmax = min(self.mmax*self.mres, src.mmax*src.mres)
        self.data[:,:,:] = 0
        for m in range(0, mmax+1, self.mres):
            if (m % src.mres == 0):
                od = self.sht.idx(m,m)
                os = src.sht.idx(m,m)
                n = lmax+1-m
                self.data[:,:,od:od+n] = src.data[:,:,os:os+n]

    def tofile(self, filename, iteration=0, step=0):
        """write field to file"""
        h = self.encode_header(self.ncomp(), self.nelem(), self.data.dtype, iteration, step)
        f = open(filename, "wb")
        f.write(h)      # write header
        self.grid.r.astype(float64).tofile(f)       # write grid
        self.data.tofile(f)
        f.close()

    def r_array(self):
        return self.grid.r[self.irs:self.ire+1].reshape(-1,1).copy()

    def theta_array(self):
        return arccos(self.sht.cos_theta)

    def phi_array(self):
        return (2.*pi)/(self.sht.nphi*self.mres) * array(range(0,self.sht.nphi))


class ScalarSH(Spectral):
    """A 3D scalar field described by its Poloidal and Toroidal components, in spherical harmonic expansion."""
    def alloc(self, irs, ire, ncomp=1, dtype=complex128, filename=None):
        Spectral.alloc(self, irs, ire, ncomp, dtype=dtype, filename=filename)

    def grad_r(self, ir):       # gradient of scalar field
        if (ir>self.irs) and (ir<self.ire) :        # bulk
            G = self.grid.Gr[ir,:]
            S = G[0]*self.sh(ir-1) + G[1]*self.sh(ir) + G[2]*self.sh(ir+1)
        else:
            r = self.grid.r
            bc = self.BC[1]
            ii,ig = ir-1,ir+1
            if ir==self.irs:    # inner boundary condition
                bc = self.BC[0]
                ii,ig = ir+1,ir-1
                if r[ir] == 0:
                    return self.sh(ii) * (self.l2==2) / r[ii]       # only l=1
            if bc == 0:     # zero bc
                S = self.sh(ii) / (r[ii] - r[ir])
            elif bc == 2:   # free-slip bc OR imposed flux bc
                S = self.sh(ig)   # imposed flux stored in the ghost shell
            else:       # order 1 approx OR fixed temperature bc
                dr_1 = 1.0/(r[ii] - r[ir])
                S = (self.sh(ii) - self.sh(ir))*dr_1
        return S

    def r_energy(self, ir):
        v2 = square(abs(self.sh(ir,0)))     # scalar field
        v2[self.m==0] *= 0.5            # count m>0 twice (+m and -m)
        return v2

    def spat_shell(self, ir):
        return self.sht.synth(self.sh(ir).astype(complex128))

    def spat_merid(self, phi=0, ang=0):
        nr = self.ire-self.irs+1
        c = empty((nr, self.sht.nlat), double)
        cc = empty(self.sht.spat_shape, double)
        for ir in range(0, nr):
            q = self.sh(ir+self.irs).astype(complex128)
            if phi != 0:
                q = self.sht.Zrotate(q,phi)
            self.sht.SH_to_spat(q, cc)
            c[ir,:] = cc[:,0]
        return c

    def spat_equat(self):
        nr = self.ire-self.irs+1
        r = self.grid.r[self.irs:self.ire+1].reshape(nr,1)
        c = empty((nr, self.sht.nphi+1), double)
        for ir in range(0, nr):
            cc = self.spat_shell(ir+self.irs)
            c[ir,0:-1] = cc[self.sht.nlat//2,:]
        c[:,-1] = c[:,0]      # add cyclic
        return c

    def spat_full(self):
        if not hasattr(self.sht, 'spat_shape'):
            self.sht.set_grid()
        v = empty((self.ire-self.irs+1, self.sht.spat_shape[0], self.sht.spat_shape[1]), double)
        for ir in range(v.shape[0]):
            self.sht.SH_to_spat(self.sh(ir+self.irs).astype(complex128), v[ir])
        return v

    def from_spat_full(self, v):
        """ reconstruct a Scalar field from a spatial representatio. """
        if v.shape != (self.ire-self.irs+1, self.sht.spat_shape[0], self.sht.spat_shape[1]):
            raise RuntimeError("spatial field has wrong shape")
        for ir in range(v.shape[0]):
            self.data[ir+1, 0, :] = self.sht.analys(v[ir])


class PolTor(Spectral):
    """A 3D vector field described by its Poloidal and Toroidal components, in spherical harmonic expansion."""
    def alloc(self, irs, ire, ncomp=2, dtype=complex128, filename=None):
        Spectral.alloc(self, irs, ire, ncomp, dtype=dtype, filename=filename)

    def set_pol(self, ir, p):
        self.data[ir - self.irs+1, 0, :] = p

    def set_tor(self, ir, t):
        self.data[ir - self.irs+1, 1, :] = t

    def pol(self, ir):
        if self.curl == 0:
            return self.data[ir - self.irs+1, 0, :]     # poloidal (read/write)
        else:
            return self.data[ir - self.irs+1, 1, :].copy()      # pol(curl) = toroidal

    def tor(self, ir):
        if self.curl == 0:
            return self.data[ir - self.irs+1, 1, :]     # toroidal (read/write)
        else:
            r = self.grid.r
            l2_r2 = self.l2/(r[ir]**2)
            if (ir>self.irs) and (ir<self.ire) :        # bulk
                Lr = -self.grid.Lr[ir,:]
                T = Lr[0]*self.sh(ir-1) + (Lr[1]+l2_r2)*self.sh(ir) + Lr[2]*self.sh(ir+1)       # T_curl = -lap(P)
            else:
                bc = self.BC[1]
                ii,ig = ir-1, ir+1
                if ir==self.irs:    # inner boundary condition
                    bc = self.BC[0]
                    ii,ig = ir+1, ir-1
                    if r[ir] == 0:      # T = 0
                        return zeros(self.nelem(), dtype=complex)
                r_1 = 1.0/r[ir]
                dr_1 = 1.0/(r[ii] - r[ir])
                if (bc == 0) or (bc == 1):  # zero or no-slip bc
                    dr_2 = dr_1**2 * 2.
                    T = (dr_2 + l2_r2)*self.sh(ir) - dr_2*self.sh(ii) + 2./(dr_1-r_1)*self.sh(ig)
                if bc == 2: # free-slip bc
                    T = (-2.*r_1*dr_1) * self.sh(ii)
                elif bc == 3:   # magnetic bc
                    cg = 2.*r_1*(r_1 - dr_1)    # ghost coeff
                    dr_2 = 2.*dr_1*dr_1
                    r_2 = r_1*r_1
                    dx = 2.*r_1*dr_1
                    if ir==self.irs:
                        T = (dr_2 + dx*self.l + (self.l**2 - self.l)*r_2) * self.sh(ir)  -  dr_2 * self.sh(ii)  +  cg * self.sh(ig)
                    else:
                        T = (dr_2 - dx*(self.l+1) + (self.l-2)*(self.l+1)*r_2) * self.sh(ir)  -  dr_2 * self.sh(ii)  -  cg * self.sh(ig)
                else:       # ???
                    T = zeros(self.nelem(), dtype=complex)
            return T

    def rad(self, ir):
        r = self.grid.r
        if r[ir]==0:
            Q = 2 * self.pol(ir+1) * (self.l==1) / r[ir+1]      # non-zero only for l=1
        else:
            Q = self.pol(ir) * self.l2 / r[ir]
        return Q

    def sph(self, ir):
        r = self.grid.r
        if (ir>self.irs) and (ir<self.ire) :        # bulk
            Gr = self.grid.Gr[ir,:]
            S = Gr[0]*self.pol(ir-1) + (Gr[1] + 1.0/r[ir])*self.pol(ir) + Gr[2]*self.pol(ir+1)
        else:
            bc = self.BC[1]
            ii,ig = ir-1,ir+1
            if ir==self.irs:    # inner boundary condition
                bc = self.BC[0]
                ii,ig = ir+1,ir-1
                if r[ir] == 0:
                    return self.rad(ir)
            if self.curl == 0:
                if bc == 0:     # zero bc
                    S = zeros(self.nelem(), dtype=complex)
                elif bc == 1:   # no-slip bc
                    S = self.sh(ir)/r[ir] + self.sh(ig)     # P/r + dP/dr  [dp/dr stored at ig]
                elif bc == 2:   # free-slip bc
                    S = self.sh(ii) / (r[ii] - r[ir])
                elif bc == 3:   # magnetic bc
                    r_1 = 1.0/r[ir]
                    l = self.l
                    if ir==self.irs:
                        S = (self.sh(ir) * (l+1) - self.sh(ig)) * r_1
                    else:   # ir==self.ire
                        S = (self.sh(ig) - l * self.sh(ir)) * r_1                   
                else:       # order 1 approx:
                    r_1 = 1.0/r[ir]
                    dr_1 = 1.0/(r[ii] - r[ir])
                    S = (r_1 - dr_1)*self.sh(ir) + dr_1*self.sh(ii)
            else:   # curl !
                r_1 = 1.0/r[ir]
                dr_1 = 1.0/(r[ii] - r[ir])
                if bc == 2: # free-slip bc
                    S = (r_1+r_1) * self.sh(ir,1)       # dT/dr = T/r
                elif bc == 3:   # magnetic bc
                    S = dr_1 * self.sh(ii,1)
                else:       # order 1 approx:
                    S = (r_1 - dr_1)*self.sh(ir,1) + dr_1*self.sh(ii,1)
        return S

    def tor_full(self):
        if self.curl == 0:
            return self.data[1:self.ire-self.irs+2, 1, :].squeeze()     # toroidal (read/write)
        else:
            r = self.grid.r[self.irs+1:self.ire].reshape(-1, 1)
            l2_r2 = self.l2/(r**2)
            T = empty_like(self.data[1:self.ire-self.irs+2, 1, :].squeeze())
            # bulk calculation all in one go
            Pl = self.data[1:self.ire-self.irs, 0].squeeze()
            Pd = self.data[2:self.ire-self.irs+1, 0].squeeze()
            Pu = self.data[3:self.ire-self.irs+2, 0].squeeze()
            shape = ones(len(T.shape), int)
            shape[0] = -1
            Lr = -self.grid.Lr[self.irs+1:self.ire, :]
            Lr0 = Lr[:, 0].reshape(shape)
            Lr1 = Lr[:, 1].reshape(shape) + l2_r2
            Lr2 = Lr[:, 2].reshape(shape)
            T[1:-1] = Lr0 * Pl + Lr1 * Pd + Lr2 * Pu
            # innermost points with old routine
            T[0] = PolTor.tor(self, self.irs)
            # outermost points with old routine
            T[-1] = PolTor.tor(self, self.ire)
            return T

    def pol_full(self):
        if self.curl == 0:
            return self.data[1:self.ire-self.irs+2, 0]
        else:
            return self.data[1:self.ire-self.irs+2, 1].copy()

    def rad_full(self):
        pol = self.pol_full()
        r = self.grid.r
        Q = pol * self.l2 / r[self.irs:self.ire+1, newaxis]
        if r[self.irs] == 0:
            Q[0] = 2 * pol[1] * (self.l == 1) / r[1]
        return Q

    def sph_full(self):
        pol = self.pol_full()
        sph = empty_like(pol)
        # inner point with old routine
        sph[0] = PolTor.sph(self, self.irs)
        # bulk calculation
        Pl = pol[0:-2]
        Pd = pol[1:-1]
        Pu = pol[2:]
        shape = ones(len(Pd.shape), int)
        shape[0] = -1
        r = self.grid.r[self.irs+1:self.ire].reshape(shape)
        Gr = self.grid.Gr[self.irs+1:self.ire]
        Gr0 = Gr[:, 0].reshape(shape)
        Gr1 = Gr[:, 1].reshape(shape) + 1.0 / r
        Gr2 = Gr[:, 2].reshape(shape)
        sph[1:-1] = Gr0 * Pl + Gr1 * Pd + Gr2 * Pu
        # outer point with old routine
        sph[-1] = PolTor.sph(self, self.ire)
        return sph

    def r_energy(self, ir):
        v2 = empty((2,self.data.shape[2]))
        sph = self.sph(ir)
        rad = self.rad(ir)
        tor = self.tor(ir)
        v2[0, :] = (sph * sph.conj()).real * self.l2 + (rad * rad.conj()).real # poloidal energy
        v2[1, :] = (tor * tor.conj()).real * self.l2                           # toroidal energy
        v2[:,self.m==0] *= 0.5          # count m>0 twice (+m and -m)
        return v2

    def to_point(self, ir, cost, phi):
        q = self.rad(ir).astype(complex128)
        s = self.sph(ir).astype(complex128)
        t = self.tor(ir).astype(complex128)
        return self.sht.SHqst_to_point(q, s, t, cost, phi)

    def to_spat_m(self, ir, im):
        idx0 = self.sht.idx(im, im)
        idx1 = self.sht.idx(self.sht.lmax, im)+1
        q = self.rad(ir)[idx0:idx1].astype(complex128)
        s = self.sph(ir)[idx0:idx1].astype(complex128)
        t = self.tor(ir)[idx0:idx1].astype(complex128)
        vr = empty(self.sht.nlat, complex128)
        vt = empty_like(vr)
        vp = empty_like(vr)
        self.sht.SHqst_to_spat_m(q, s, t, vr, vt, vp, im)
        return vr, vt, vp

    def spat_shell(self, ir):
        q = self.rad(ir).astype(complex128)
        s = self.sph(ir).astype(complex128)
        t = self.tor(ir).astype(complex128)
        vr = empty(self.sht.spat_shape, double)
        vt = empty_like(vr)
        vp = empty_like(vr)
        self.sht.SHqst_to_spat(q, s, t, vr, vt, vp)
        return vr,vt,vp

    def spat_merid(self, phi=0, ang=0):
        nr = self.ire-self.irs+1
        vr = empty((nr, self.sht.nlat), double)
        vt = empty_like(vr)
        vp = empty_like(vr)
        vrr = empty(self.sht.spat_shape, double)
        vtt = empty_like(vrr)
        vpp = empty_like(vrr)
        for ir in range(0, nr):
            q = self.rad(ir+self.irs).astype(complex128)
            s = self.sph(ir+self.irs).astype(complex128)
            t = self.tor(ir+self.irs).astype(complex128)
            if phi != 0:
                q = self.sht.Zrotate(q,phi)
                s = self.sht.Zrotate(s,phi)
                t = self.sht.Zrotate(t,phi)
            self.sht.SHqst_to_spat(q, s, t, vrr, vtt, vpp)
            vr[ir,:] = vrr[:,0]
            vt[ir,:] = vtt[:,0]
            vp[ir,:] = vpp[:,0]
        if ang:
            ct = self.sht.cos_theta
            st = sqrt(1.0 - ct*ct)
            r = self.grid.r[self.irs:self.ire+1, newaxis]
        if ang & 1:
            vp /= r * st
            vp[:, st==0.0] = 0.0
        if ang & 2:
            vt /= sqrt(square((r*ct)) + square(r*st))
        return vr, vt, vp

    def spat_axi(self, ang=0):
        nr = self.ire-self.irs+1
        r = self.grid.r[self.irs:self.ire+1]
        # initialize an shtns object for just the axisymmetric modes
        sht = shtns.sht(self.sht.lmax, 0, 1)
        sht.set_grid(self.sht.nlat, 1)
        ct = sht.cos_theta
        st = sqrt(1.0 - ct**2)
        vp = empty((nr, self.sht.nlat), double)
        vpol = empty_like(vp)
        v0 = empty_like(vp)

        m0inds = array([self.sht.idx(int(ell), 0) for ell in sht.l])
        specarr = sht.spec_array()
        for i in range(nr):
            ir = i + self.irs
            specarr[:] = self.tor(ir)[m0inds]
            sht.SHtor_to_spat(specarr, v0[i], vp[i])
            specarr[:] = self.pol(ir)[m0inds]
            sht.SHtor_to_spat(specarr, vpol[i], v0[i])
        vpol[:] = -r[:, newaxis] * st * v0
        # compute the poloidal fields
        if ang & 1:
            vp /= r[:, newaxis] * st            
        return r, ct, vp, vpol, v0

    def spat_equat(self):
        nr = self.ire-self.irs+1
        r = self.grid.r[self.irs:self.ire+1].reshape(nr,1)
        vs = empty((nr, self.sht.nphi+1), double)
        vp = empty_like(vs)
        vz = empty_like(vp)
        for ir in range(0, nr):
            vrr, vtt, vpp = self.spat_shell(ir+self.irs)
            vs[ir,0:-1] = vrr[self.sht.nlat//2,:]
            vp[ir,0:-1] = vpp[self.sht.nlat//2,:]
            vz[ir,0:-1] = -vtt[self.sht.nlat//2,:]
        vs[:,-1] = vs[:,0]      # add cyclic
        vp[:,-1] = vp[:,0]
        vz[:,-1] = vz[:,0]
        return vs, vp, vz

    def spat_full(self):
        if not hasattr(self.sht, 'spat_shape'):
            self.sht.set_grid()
        qarr = self.rad_full().astype(complex128)
        sarr = self.sph_full().astype(complex128)
        tarr = self.tor_full().astype(complex128)
        v = empty((self.ire-self.irs+1, 3, self.sht.spat_shape[0], self.sht.spat_shape[1]), double)
        for ir in range(v.shape[0]):
            self.sht.SHqst_to_spat(qarr[ir], sarr[ir], tarr[ir], v[ir, 0], v[ir, 1], v[ir, 2])
        return v

    def from_spat_full(self, v):
        """ reconstruct a Pol/Tor field from a spatial 3D vector field. The field will be projected on a divergenceless field. """
        if v.shape != (self.ire-self.irs+1, 3, self.sht.spat_shape[0], self.sht.spat_shape[1]):
            raise RuntimeError("spatial field has wrong shape")
        r = self.grid.r
        l_2 = empty_like(self.l2)
        l_2[0] = 0
        l_2[1:] = 1.0/self.l2[1:]
        for ir in range(v.shape[0]):
            Q,S,T = self.sht.analys(v[ir, 0], v[ir, 1], v[ir, 2])
            self.data[ir+1, 0, :] = Q * l_2 * r[ir + self.irs]
            self.data[ir+1, 1, :] = T

    def spat_line(self, xyz0, xyz1, cartesian=False, udv=False):
        """computes the spatial vector along a line from r0 to r1"""
        assert not (cartesian and udv), 'cannot specify both cartesian and udv'
        r = self.grid.r
        xyz0 = asarray(xyz0).astype(double)
        xyz1 = asarray(xyz1).astype(double)
        vr = xyz1 - xyz0
        nv = linalg.norm(vr)
        vr /= nv
        r0 = dot(xyz0, xyz0)
        r1 = dot(xyz1, xyz1)
        bb = dot(vr, xyz0)
        ir0, ir1 = searchsorted(r, (r0, r1))
        # force the final point to be within the sphere
        if ir1 < self.irs:
            ir1 = self.irs
        if ir1 > self.ire:
            ir1 = self.ire
        # calculate the increments
        if (bb < 0.):
            irinc = -1
            if ir0 > self.ire:
                ir0 = self.ire
            if r[ir0] * r[ir0] > r0:
                ir0 -= 1
        else:
            irinc = +1
            if r[ir0] * r[ir0] < r0:
                ir0 += 1
            if ir0 < self.irs:
                ir0 = self.irs
        d = bb*bb + r*r - r0
        # find where the increment reverses
        ir_rev = searchsorted(d, 0)
        # get the radial indices
        ir = arange(ir0, ir_rev, irinc)
        if len(ir):
            rev = len(ir)
            ir = r_[ir, arange(ir_rev, ir1)]
            irinc = ones_like(ir)
            irinc[:rev] = -1
        else:
            ir = arange(ir0, ir1, irinc)
            irinc = ones_like(ir)
        # find the line coordinate
        alpha = -bb + irinc * sqrt(d[ir])
        # calculate the cartesian and spherical coordinates
        xyz = c_[[x + alpha * v for x, v in zip(xyz0, vr)]]
        rr = linalg.norm(xyz, axis=0)
        cost = xyz[2].ravel() / rr
        phi = arctan2(xyz[1], xyz[0])
        rtp = c_[rr, cost, phi]
        # compute spherical vector values
        urtp = array([self.to_point(i, ct, ph)
                      for i, ct, ph in zip(ir, cost, phi)])
        # convert to cartesian
        if cartesian or udv:
            cost = cost[:, newaxis]
            sint = sqrt((1.0 + cost)*(1.0 - cost))
            cp, sp = cos(phi[:, newaxis]), sin(phi[:, newaxis])
            vz = urtp[:, 0, newaxis] * cost + urtp[:, 1, newaxis] * sint
            vs = urtp[:, 0, newaxis] * sint + urtp[:, 1, newaxis] * cost
            vx = vs * cp - urtp[:, 2, newaxis] * sp
            vy = vs * sp + urtp[:, 2, newaxis] * cp
            uxyz = c_[vx, vy, vz]
            if cartesian:
                return alpha, xyz, uxyz
            if udv:
                # get the tangent vector for the line
                dr = empty_like(xyz)
                dr[:, 0] = (xyz[:, 1] - xyz[:, 0]) / (alpha[1] - alpha[0])
                dr[:, 1:-1] = (xyz[:, 2:] - xyz[:, :-2]) / (alpha[2:] - alpha[:-2])
                dr[:, -1] = (xyz[:, -1] - xyz[:, -2]) / (alpha[-1] - alpha[-2])
                dr /= linalg.norm(dr, axis=0, keepdims=True)
                # dot (in a vector sense) with the cartesian velocity vector
                u = sum(dr.T * uxyz, axis=1)
                return alpha, u
        return alpha, rtp, urtp

    def zavg(self):
        """Compute the vertically averaged field."""
        ire = self.ire
        irs = self.irs
        r = self.grid.r
        ct = self.sht.cos_theta
        ct_sorter = ct.argsort()
        r2 = r*r
        r_1 = 1.0 / r
        # generate the cylindrical grid
        ns = self.sht.nlat // 2
        s = arange(ns) * r[ire] / (ns-1)
        s2 = s*s
        # find the tangent cylinder
        is_tc = 0
        while s[is_tc] < r[irs]:
            is_tc += 1
        vs1 = zeros((ns, self.sht.nphi+1), double)
        vp1 = zeros_like(vs1)
        vs2 = zeros_like(vs1)
        vp2 = zeros_like(vs1)
        vsvp = zeros_like(vs1)
        # r derivatives
        r_p = empty_like(r)
        r_p[irs:ire+1] = r_[r[irs+1:ire+1], r[ire]]
        r_m = empty_like(r)
        r_m[irs:ire+1] = r_[r[irs], r[irs:ire]]
        
        for ir in range(irs, ire+1):
            vr, vt, vp = self.spat_shell(ir)
            it = 1
            is_max = searchsorted(s, r[ir])
            z = sqrt(r2[ir] - s2[:is_max])
            ztop = sqrt(r2[ire] - s2[:is_max])
            cost = z * r_1[ir]
            sint = s[:is_max] * r_1[ir]
            H_1 = r_[1.0 / (ztop[:is_tc] - sqrt(r2[irs]-s2[:is_tc])),
                     0.5 / ztop[is_tc:]]
            dz = sqrt(r_p[ir]*r_p[ir] - s2[:is_max]) - sqrt(r_m[ir]*r_m[ir] - s2[:is_max])
            # only go vertically at origin
            if r[ir] == 0:
                cost[:] = 1.0
                sint[:] = 0.0
            # handle the equator differently
            is_cross = searchsorted(s, r_m[ir])
            try:
                dz[is_cross] = sqrt(r_p[ir] * r_p[ir] - s2[is_cross]) + z[is_cross]
            except IndexError:
                pass
            dz *= 0.5 * H_1
            # at edge only one point contribues
            ind = (s[:is_max] == r[ire])
            dz[ind] = 1.0
            H_1[ind] = 1.0
            cost[ind] = 0.0
            sint[ind] = 0.0
            # find the intersection
            it = ct_sorter[searchsorted(ct, cost, sorter=ct_sorter)]+1
            nit = self.sht.nlat - 1 - it
            # interpolation coefficients
            a = ((cost - ct[it]) / (ct[it-1] - ct[it]))[:, newaxis]
            b = 1.0 - a
            dz = dz[:, newaxis]
            # interpolate
            vrn = vr[it-1]*a + vr[it]*b
            vrs = vr[nit+1]*a + vr[nit]*b
            vtn = vt[it-1]*a  + vp[it]*b
            vts = vt[nit+1]*a + vp[nit]*b
            vpn = vp[it-1]*a  + vp[it]*b
            vps = vp[nit+1]*a + vp[nit]*b
            # project onto cylindrical grid
            vsn = vrn*sint[:, newaxis] + vtn*cost[:, newaxis]
            vss = vrs*sint[:, newaxis] - vts*cost[:, newaxis]
            # compute products
            vsn2 = vsn * vsn * dz
            vss2 = vss * vss * dz
            vpn2 = vpn * vpn * dz
            vps2 = vps * vps * dz
            vsvpn = vsn * vpn * dz
            vsvps = vss * vps * dz
            vsn *= dz
            vss *= dz
            vpn *= dz
            vps *= dz
            # inside the tangent cylinder north and south are stored on adjacent points
            vs1[:is_tc:2, :-1] += vsn[:is_tc:2]
            vs1[1:is_tc:2, :-1] += vss[:is_tc:2]
            vs2[:is_tc:2, :-1] += vsn2[:is_tc:2]
            vs2[1:is_tc:2, :-1] += vss2[:is_tc:2]
            vp1[:is_tc:2, :-1] += vpn[:is_tc:2]
            vp1[1:is_tc:2, :-1] += vps[:is_tc:2]
            vp2[:is_tc:2, :-1] += vpn2[:is_tc:2]
            vp2[1:is_tc:2, :-1] += vps2[:is_tc:2]
            vsvp[:is_tc:2, :-1] += vsvpn[:is_tc:2]
            vsvp[1:is_tc:2, :-1] += vsvps[:is_tc:2]
            # outside the tangent cyclinder there is no mixing of grids
            vs1[is_tc:is_max, :-1] += (vsn[is_tc:] + vss[is_tc:])
            vs2[is_tc:is_max, :-1] += (vsn2[is_tc:] + vss2[is_tc:])
            vp1[is_tc:is_max, :-1] += (vpn[is_tc:] + vps[is_tc:])
            vp2[is_tc:is_max, :-1] += (vpn2[is_tc:] + vps2[is_tc:])
            vsvp[is_tc:is_max, :-1] += (vsvpn[is_tc:] + vsvps[is_tc:])
        # add cyclic
        vs1[:, -1] = vs1[:, 0]
        vs2[:, -1] = vs2[:, 0]
        vp1[:, -1] = vp1[:, 0]
        vp2[:, -1] = vp2[:, 0]
        vsvp[:, -1] = vsvp[:, 0]
        return s, is_tc, vs1, vp1, vs2, vp2, vsvp
    
    def curl_from_TQS(self):
        """computes the curl of a field having 3 components in the order (toroidal, radial, spheroidal), and stores it as a poloidal/toroidal field"""
        if self.ncomp() < 3:
            raise Exception("3 components needed")
        self.curl = 0       # reset curl flag
        r = self.grid.r
        # innermost point, order 1 approximation
        ir = self.irs
        ii = ir + 1
        r_1 = 1.0 / r[ir]
        T = self.sh(ir, 1)
        Sd = self.sh(ir, 2)
        Si = self.sh(ii, 2)
        dx = 1/(r[ii] - r[ir])
        T[:] = r_1 * (T-Sd) - dx*(Si - Sd)
        # bulk
        T = self.data[2:self.ire-self.irs+1, 1]
        Sl = self.data[1:self.ire-self.irs, 2]
        Sd = self.data[2:self.ire-self.irs+1, 2]
        Su = self.data[3:self.ire-self.irs+2, 2]
        shape = ones(len(T.shape), int)
        shape[0] = -1
        r_1 = 1.0 / self.grid.r[self.irs+1:self.ire].reshape(shape)
        W = self.grid.Gr[self.irs+1:self.ire]
        W0 = W[:, 0].reshape(shape)
        W1 = W[:, 1].reshape(shape)
        W2 = W[:, 2].reshape(shape)
        T[:] = r_1 * T - (W0 * Sl + (W1+r_1)*Sd + W2 * Su)
        # outermost point, order one aproximation
        ir = self.ire
        T = self.sh(ir, 1)
        Sd = self.sh(ir, 2)
        r_1 = 1.0 / r[ir]
        ii = ir - 1
        Si = self.sh(ii, 2)
        dx = 1/(r[ii] - r[ir])
        T[:] = r_1 * (T-Sd) - dx*(Si - Sd)
        # l=0 is zero after curl
        self.data[0:self.ire-self.irs+1, :, 0] = 0.0


class VectorSH(Spectral):
    """A 3D vector field described by its Radial, Spheroidal and Toroidal components, in spherical harmonic expansion."""
    def alloc(self, irs, ire, ncomp=3, dtype=complex128, filename=None):
        Spectral.alloc(self, irs, ire, ncomp, dtype=dtype, filename=filename)

    def set_rad(self, ir, q):
        self.data[ir - self.irs+1, 0, :] = q

    def set_sph(self, ir, s):
        self.data[ir - self.irs+1, 1, :] = s

    def set_tor(self, ir, t):
        self.data[ir - self.irs+1, 2, :] = t

    def rad(self, ir):
        if self.curl == 0:
            return self.data[ir - self.irs+1, 0, :]     # radial (read/write)
        else:
            raise ValueError("curl not implemented")
            return 0

    def sph(self, ir):
        if self.curl == 0:
            return self.data[ir - self.irs+1, 1, :]     # spheroidal (read/write)
        else:
            raise ValueError("curl not implemented")
            return 0

    def tor(self, ir):
        if self.curl == 0:
            return self.data[ir - self.irs+1, 2, :]     # toroidal (read/write)
        else:
            raise ValueError("curl not implemented")
            return 0

    def rad_full(self):
        if self.curl == 0:
            return self.data[1:self.ire-self.irs+2, 0, :].squeeze()
        else:
            raise ValueError("curl not implemented")
            return 0

    def sph_full(self):
        if self.curl == 0:
            return self.data[1:self.ire-self.irs+2, 1, :].squeeze()
        else:
            raise ValueError("curl not implemented")
            return 0

    def tor_full(self):
        if self.curl == 0:
            return self.data[1:self.ire-self.irs+2, 2, :].squeeze()
        else:
            raise ValueError("curl not implemented")
            return 0

    def r_energy(self, ir):
        v2 = empty((2,self.data.shape[2]))
        sph = self.sph(ir)
        rad = self.rad(ir)
        tor = self.tor(ir)
        v2[0, :] = (sph * sph.conj()).real * self.l2 + (rad * rad.conj()).real # poloidal energy
        v2[1, :] = (tor * tor.conj()).real * self.l2                           # toroidal energy
        v2[:,self.m==0] *= 0.5          # count m>0 twice (+m and -m)
        return v2

    def to_point(self, ir, cost, phi):
        q = self.rad(ir).astype(complex128)
        s = self.sph(ir).astype(complex128)
        t = self.tor(ir).astype(complex128)
        return self.sht.SHqst_to_point(q, s, t, cost, phi)

    def to_spat_m(self, ir, im):
        idx0 = self.sht.idx(im, im)
        idx1 = self.sht.idx(self.sht.lmax, im)+1
        q = self.rad(ir)[idx0:idx1].astype(complex128)
        s = self.sph(ir)[idx0:idx1].astype(complex128)
        t = self.tor(ir)[idx0:idx1].astype(complex128)
        vr = empty(self.sht.nlat, complex128)
        vt = empty_like(vr)
        vp = empty_like(vr)
        self.sht.SHqst_to_spat_m(q, s, t, vr, vt, vp, im)
        return vr, vt, vp

    def spat_shell(self, ir):
        q = self.rad(ir).astype(complex128)
        s = self.sph(ir).astype(complex128)
        t = self.tor(ir).astype(complex128)
        vr = empty(self.sht.spat_shape, double)
        vt = empty_like(vr)
        vp = empty_like(vr)
        self.sht.SHqst_to_spat(q, s, t, vr, vt, vp)
        return vr,vt,vp

    def spat_merid(self, phi=0, ang=0):
        nr = self.ire-self.irs+1
        vr = empty((nr, self.sht.nlat), double)
        vt = empty_like(vr)
        vp = empty_like(vr)
        vrr = empty(self.sht.spat_shape, double)
        vtt = empty_like(vrr)
        vpp = empty_like(vrr)
        for ir in range(0, nr):
            q = self.rad(ir+self.irs).astype(complex128)
            s = self.sph(ir+self.irs).astype(complex128)
            t = self.tor(ir+self.irs).astype(complex128)
            if phi != 0:
                q = self.sht.Zrotate(q,phi)
                s = self.sht.Zrotate(s,phi)
                t = self.sht.Zrotate(t,phi)
            self.sht.SHqst_to_spat(q, s, t, vrr, vtt, vpp)
            vr[ir,:] = vrr[:,0]
            vt[ir,:] = vtt[:,0]
            vp[ir,:] = vpp[:,0]
        if ang:
            ct = self.sht.cos_theta
            st = sqrt(1.0 - ct*ct)
            r = self.grid.r[self.irs:self.ire+1, newaxis]
        if ang & 1:
            vp /= r * st
            vp[:, st==0.0] = 0.0
        if ang & 2:
            vt /= sqrt(square((r*ct)) + square(r*st))
        return vr, vt, vp

    def spat_equat(self):
        nr = self.ire-self.irs+1
        r = self.grid.r[self.irs:self.ire+1].reshape(nr,1)
        vs = empty((nr, self.sht.nphi+1), double)
        vp = empty_like(vs)
        vz = empty_like(vp)
        for ir in range(0, nr):
            vrr, vtt, vpp = self.spat_shell(ir+self.irs)
            vs[ir,0:-1] = vrr[self.sht.nlat//2,:]
            vp[ir,0:-1] = vpp[self.sht.nlat//2,:]
            vz[ir,0:-1] = -vtt[self.sht.nlat//2,:]
        vs[:,-1] = vs[:,0]      # add cyclic
        vp[:,-1] = vp[:,0]
        vz[:,-1] = vz[:,0]
        return vs, vp, vz

    def spat_full(self):
        if not hasattr(self.sht, 'spat_shape'):
            self.sht.set_grid()
        qarr = self.rad_full().astype(complex128)
        sarr = self.sph_full().astype(complex128)
        tarr = self.tor_full().astype(complex128)
        v = empty((self.ire-self.irs+1, 3, self.sht.spat_shape[0], self.sht.spat_shape[1]), double)
        for ir in range(v.shape[0]):
            self.sht.SHqst_to_spat(qarr[ir], sarr[ir], tarr[ir], v[ir, 0], v[ir, 1], v[ir, 2])
        return v

""" decode fp48 values to numpy float64 (complex128). dtype of x must be int16, where 3 consecutive values represent an fp48 number.
    The first int16 number is the exponent shift """
def fp48_read_stream(x):
    exp_shift = (int64(x[0]) + 959) << 40   # x[0] as a signed value
    x = x.view(uint16)  # unsigned for zero extend
    y = int64(x[1::3]) + (int64(x[2::3]) << 16) + (int64(x[3::3]) << 32)    # construct the fp48
    exma_msk = 0x00007FFFFFFFFFFF   # mask for exponent and mantissa
    sign_msk = 0x0000800000000000   # mask for sign bit
    z = y & exma_msk    # remove sign bit
    y = ((y&sign_msk)<<16) | ((z + exp_shift)<<12)     # compute value
    y[z==0] = 0   # zero
    y[z==exma_msk] = (exma_msk<<16)   # nan
    return y.view(complex128)

def decode_header(f):
    bswap = False
    ### read header
    head = f.read(1024)
    head_pattern = '16i8d64s832s'
    h = struct.unpack('=' + head_pattern, head)     # try native order first
    if (h[5]<0) or (shtns.nlm_calc(h[1],h[2],h[3]) != h[4]):    # test nr, lmax,mmax,mres, nlm
        bswap = True
        h = struct.unpack(('>' if (struct.pack('=h',1)==struct.pack('<h',1)) else '<') + head_pattern, head)    # swap endian
    nr, irs, ire = h[5], h[6], h[7]
    r = fromfile(f, dtype=float64, count=nr)    # read radial grid
    dtyp = 'complex64' if (h[0] & 4096) else 'complex128'    # single or double precision
    if (h[0] & (4096*4)):  dtyp = 'fp48'  # fp 48 compression
    if bswap:
        r = r.byteswap()
    info = {'lmax':h[1], 'mmax':h[2], 'mres':h[3], 'nlm':h[4], 'nr':nr, 'ir':(irs,ire), 'r':(r[irs],r[ire]),
     'version':h[0]&4095, 'BC':(h[8],h[9]), 'ncomp':h[13], 'iter':h[14], 'step':h[15], 'time':h[19], 'shtnorm':h[12],
     'id':h[24].decode().strip('\x00'), 'dtype':dtyp, 'varltr':(h[0]&8192==8192), 'bswap':bswap}
    return info, r

def load_field(filename, lazy=True, sht=None, grid=None):
    """load_field(filename, lazy=True) -> PolTor or ScalarSH depending on file content."""
    f = open(filename, "rb")
    ### read header and radial grid
    h, r = decode_header(f)
    lmax, mmax, mres = h['lmax'], h['mmax'], h['mres']
    nlm, nr, ncomp = h['nlm'], h['nr'], h['ncomp']
    version, shtnorm, bswap = h['version'], h['shtnorm'], h['bswap']
    it, step = h['iter'], h['step']
    if version not in (11,12,13):
        print('version=',version)
        raise Exception("File version not supported")
    if nlm != shtns.nlm_calc(lmax,mmax,mres):
        raise Exception("Spherical harmonic size mismatch")
    if h['dtype'] == 'fp48':
        fp48 = True
        lazy = False
    else:
        fp48 = False
        dtyp = dtype(h['dtype'])
    if bswap:
        dtyp = dtyp.newbyteorder()      # change byte order
    if grid is None:
        grid = Grid(r)
    if sht is None:
        sht = (lmax, mmax, mres)
    if (ncomp==2):
        S = PolTor(grid, sht)       # create Spectral object
    else:
        S = ScalarSH(grid, sht)     # create Spectral object
    S.irs, S.ire = h['ir']
    S.set_BC(h['BC'][0], h['BC'][1])
    S.time = h['time']

    if h['varltr']:      # variable l-truncation
        ltr = fromfile(f, dtype=uint16, count=nr)   # read ltr
        if bswap:  ltr = ltr.byteswap()
        ltr = hstack((ltr[0], ltr, ltr[-1]))        # add ghost ltr
        ltr[ltr>lmax] = lmax  # also saturate at lmax.
        print("variable l-truncation =",ltr)
        S.alloc(S.irs, S.ire)
        for ir in range(S.irs-1, S.ire+2):
            ltrr = int(ltr[ir+1])
            mlim = min(mmax,ltrr//mres)
            nlmr = shtns.nlm_calc(ltrr, mmax, mres)
            for ic in range(0, ncomp):
                if fp48:  # fp48
                    buf = fp48_read_stream( fromfile(f, dtype=int16, count=nlmr*6+1) )
                else:
                    buf = fromfile(f, dtype=dtyp, count=nlmr)
                buf2 = zeros(nlm, dtype=complex128)
                lms,lmd = 0,0
                for im in range(0,mlim+1):
                    nlr = ltrr+1-im*mres
                    buf2[lmd:lmd+nlr] = buf[lms:lms+nlr]
                    lms += nlr
                    lmd += lmax+1-im*mres
                if lms != nlmr:
                    print(ir,ic,"something went wrong", lms, nlmr)
                S.set_sh(buf2, ir, ic)
    else:
        ### load data
        nshells = S.ire - S.irs + 3     # include ghost shells
        if lazy:
            data = memmap(f, dtype=dtyp, mode='r', shape=(nshells, ncomp, nlm), offset=1024+nr*8)
        else:
            if fp48:  # fp48
                data_raw = fromfile(f, dtype=int16, count=nshells*(nlm*6+1)*ncomp).reshape(nshells*ncomp, -1)
                data = zeros((nshells*ncomp, nlm), dtype=complex128)
                for k in range(nshells*ncomp):
                    data[k,:] = fp48_read_stream(data_raw[k,:])
            else:
                    data = fromfile(f, dtype=dtyp, count=nshells*nlm*ncomp).astype(complex128)
        S.data = data.reshape(nshells, ncomp, nlm)
    f.close()
    return S

def get_field_info(filename, disp=True):
    f = open(filename, "rb")
    ### read header
    info, r = decode_header(f)
    f.close()
    if disp:
        print(info)
    return info, r

def load_grid(filename):
    info, r = get_field_info(filename, disp=False)
    return r

def clone_field(s, ncomp=0, copy=False, dtype=complex128, filename=None):
    """returns field of same size and properties as s, with zero data or a copy of the data, optionally a different number of components."""
    if ncomp==0:
        ncomp = s.ncomp()
    if hasattr(s, 'sht'):
        sht = s.sht
    else:
        sht = (s.lmax, s.mmax, s.mres)
    if ncomp==2:
        clone = PolTor(s.grid, sht)
    else:
        clone = ScalarSH(s.grid, sht)
    clone.BC = s.BC
    clone.alloc(s.irs, s.ire, ncomp, dtype=dtype, filename=filename)
    if copy:
        copyto(clone.data, s.data)      # copy data
        clone.curl = s.curl
    return clone

def load_parody(filename, field):
    """load a parody 'D'-file and convert to xshells format. 'field' can be 'U','B', or 'T' for velocity, magnetic and temperature fields respectively"""
    f=open(filename,"rb")

    ### header
    head=f.read(72)
    h = struct.unpack(">iiiidiidiiiiiiii", head)		## apparently, parody files are big endian.
    par = {}
    par['version'] = h[1]
    par['time'] = h[4]
    par['dt'] = h[7]
    par['nlm'] = h[10]
    par['NG'],par['NR'] = h[13],h[14]

    nlm = par['nlm']
    NR = par['NR']
    NG = par['NG']-1	# convert from 1-based fortran to 0-based index

    print(par)
    if par['version'] != 3:
         print("error, only version 3 is supported")
         return 0

    ### radial grid
    r = zeros(NR)
    for i in range(0, NR):
        x = f.read(16)
        r[i] = struct.unpack(">idi", x)[1]
    print("radial grid from r=%f to %f" % (r[0], r[-1]))

    #### l,m list
    larr = zeros(nlm, dtype=int)
    marr = zeros(nlm, dtype=int)
    for lm in range(0, nlm):
        x = f.read(16)
        s = struct.unpack(">iiii", x)
        larr[lm], marr[lm] = s[1],s[2]
    lmax, mmax = amax(larr), amax(marr)
    mres = sort(unique(marr))
    if len(mres) > 1:
        mres = mres[1]-mres[0]
    else:
        mres = 1    
    print("lmax=",amax(larr), "  mmax=",amax(marr), "  mres=",mres)

    # omega, omega_old, couple, couple_old  ==> ignored
    x = f.read(16*4)
    #s = struct.unpack(">idiidiidiidi", x)
    #omega, omega_old = s[1],s[4]
    #couple, couple_old = s[7],s[10]

    ## generate xshells grid
    grid = Grid(r)        ## generate xshells grid

    ### convert spherical harmonic coefficients to orthonormalized as used by xshells.
    renorm = sqrt(2*pi) * (1-2*(marr&1))
    renorm[marr==0] = sqrt(4*pi)

    if field == 'T':
        Flm = ScalarSH(grid, (int(lmax),int(mmax),int(mres)))
        Flm.BC = (1,1)  # default to fixed flux
        ic,nc = 4,1
    else:
        Flm = PolTor(grid, (int(lmax),int(mmax),int(mres)))
        Flm.BC = (0,0)  # default to no-slip
        ic,nc = 0,2
    if field == 'B':
        Flm.BC = (3,3)  # default to magnetic BC
        Flm.alloc(0,NR-1)
        ic,nc = 2,2
        #### data within inner-core:
        for ir in range(0,NG):
            for k in range(0,2):	# magnetic field only (2 components)
                s = f.read(4)	# skip record header
                x = fromfile(f, dtype='>d', count=2*nlm)
                zlm = (x[0::2] + 1j*x[1::2]) * renorm			# Btor, Bpol
                Flm.set_sh(zlm, ir, 1-k)
                s = f.read(4)
            f.seek((2*nlm*8 + 8)*2, 1)		# skip 2 Adams
    else:
        Flm.alloc(NG, NR-1)
        f.seek((2*nlm*8 +8)*4*NG, 1)        # skip inner-core
    Flm.time = par["time"]

    #### data within fluid:
    for ir in range(NG,NR):
        f.seek((2*nlm*8 + 8)*ic, 1)		# skip ignored fields
        for k in range(ic,ic+nc):	    # components of the requested field
            s = f.read(4)	# skip record header
            x = fromfile(f, dtype='>d', count=2*nlm)
            zlm = (x[0::2] + 1j*x[1::2]) * renorm
            Flm.set_sh(zlm, ir, (1-(k-ic))&(nc-1))      # put into right component
            s = f.read(4)
        f.seek((2*nlm*8 + 8)*(10-(ic+nc)), 1)		# skip 5 Adams + all ignored fields

    print(f.tell(), " bytes parsed.")
    f.close()
    return Flm
