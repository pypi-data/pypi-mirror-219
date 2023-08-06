**Python modules and programs to handle outputs of the xshells code.**

# xsplot

xsplot is a python module and also a command line utility that can display:

- time evolution of quantities stored in the `energy.*` files,
- slices and spectra produced by the `xspp` program from simulation fields.

For instance, from command line:

    python -m xsplot energy.bench -c Eu   # displays kinetic energy ('Eu') as a function of time
    
The same things within a python script or notebook:

    import matplotlib.pyplot as plt
    import xsplot
    y = xsplot.load_diags('energy.bench')
    plt.plot(y['t'],y['Eu'])

# pyxshells

pyxshells is a python module to work with `field*` files from simulations.
For instance:

     import pyxshells
     f = pyxshells.load_field('fieldU.bench')
     kinetic_energy = f.energy()
     print(kinetic_energy)

# DOCUMENTATION
For more info, see <https://nschaeff.bitbucket.io/xshells/Ch3.html>
