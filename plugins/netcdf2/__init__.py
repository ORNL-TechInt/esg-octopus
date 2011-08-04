import cdms2
import os
import pdb

# ---------------------------------------------------------------------------
def getData(inpath, extra_metadata, cfgfunc=None):
    """
    Write the metadata from one netcdf file in ncml format.
    """
    pdb.set_trace()
    f = cdms2.open(inpath)

    out = dif_switch(cfgfunc)

    # introductory material
    out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    out.write('<netcdf'
            + ' xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2'
            + ' location=file:"' + inpath + '">\n')

    # write a list of dimensions
    for dim in f.axes.keys():
        out.write('  <dimension name="%s" length="%d" isUnlimited="%s" />\n'
                  % (dim, len(f.axes[dim]), "???"))
                  
    # write a list of attributes
    for attr in f.attributes.keys():
        out.write('  <attribute name="%s" value="%s" />\n'
                  % (attr, f.attributes[attr]))
    
    # write a list variables, with attributes for each variable
    for name in f.variables.keys():
        var = f.variables[name]
        if var.typecode() == 'f':
            typename = 'float'
        elif var.typecode() == 'd':
            typename = 'double'
            
        out.write('  <variable name="%s" shape="%s" type="%s">\n'
                  % (name, "??", typename))

        for attr in var.attributes.keys():
            out.write('    <attribute name="%s" value="%s" />\n'
                      % (attr, var.attributes[attr]))

    for name in f.axes.keys():
        var = f.axes[name]
        if var.typecode() == 'f':
            typename = 'float'
        elif var.typecode() == 'd':
            typename = 'double'
            
        out.write('  <variable name="%s" shape="%s" type="%s">\n'
                  % (name, "??", typename))

        for attr in var.attributes.keys():
            out.write('    <attribute name="%s" value="%s" />\n'
                      % (attr, var.attributes[attr]))

# ---------------------------------------------------------------------------
def dif_switch(cfgfunc):
    """
    Return a file handle pointing to either 1) an open temp file
    (/tmp/octopus.dif.<pid>), or 2) a writeable StringIO.
    """
    if cfgfunc == None:
        return open('/tmp/octopus.dif.%d' % os.getpid(), 'w')

    outfmt = cfgfunc('dif')
    try:
        outfmt = cfgfunc('dif')
    except KeyError:
        return sys.stdout
    except NameError:
        return open('/tmp/octopus.dif.%d' % os.getpid(), 'w')

    if outfmt == 'file':
        return open('/tmp/octopus.dif.%d' % os.getpid(), 'w')
    elif outfmt == 'string':
        return StringIO()
    else:
        raise StandardError('Invalid dif value in config -- '
                            + 'must be "file://" or "string://"')
    
    
