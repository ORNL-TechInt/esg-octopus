import cdms2
import esgcet.config
import glob
import os
import pdb
import re
import sys

from esgcet.config import loadConfig, splitRecord, SaneConfigParser
from ConfigParser import InterpolationMissingOptionError

from esgcet.publish.thredds import DEFAULT_THREDDS_SERVICE_APPLICATIONS, \
DEFAULT_THREDDS_SERVICE_AUTH_REQUIRED, \
DEFAULT_THREDDS_SERVICE_DESCRIPTIONS

from StringIO import StringIO

# ---------------------------------------------------------------------------
def getData(inpath, extra_metadata):
    # pdb.set_trace()
    f = cdms2.open(inpath)

    # get a handle to the main module so we can call his routines
    main = sys.modules['__main__']
 
    # load info from esg.ini
    cfg = loadConfig(None)

    # load info from this run's transient config
    x = SaneConfigParser({})
    x.read(extra_metadata)

    # pdb.set_trace()
    output = dif_switch()
    
    for mode in ['thredds_aggregation_services',
                 'thredds_file_services',
                 'thredds_offline_services']:
        s = splitRecord(cfg.get('DEFAULT', mode))[0]
        iform(output, 'service/')
        iform(output, 'serviceType="%s"' % s[0])
        iform(output, 'base="%s"' % s[1])
        iform(output, 'name="%s"' % s[2])
        iform(output, 'desc="%s"' % DEFAULT_THREDDS_SERVICE_DESCRIPTIONS[s[0]])
        iform(output, 'property/')
        iform(output, 'name="requires_authorization"')
        iform(output,
              'value="%s"' % DEFAULT_THREDDS_SERVICE_AUTH_REQUIRED[s[0]], -1)
        for app in DEFAULT_THREDDS_SERVICE_APPLICATIONS[s[0]]:
            iform(output, '  property/')
            iform(output, 'name="application"')
            iform(output, 'value="%s"' % app, -1)

        iform(output, "", 0)
    
    iform(output, 'property/')
    iform(output, 'name="catalog_version"')
    iform(output, 'value="2"', -1)

    iform(output, 'dataset/')
    iform(output, 'restrictAccess="esg-user"')
    project = x.get('DEFAULT', 'project')

    iform(output, "ID=%s" % safe_quote(safe_interpolate(cfg,
                                                'project:' + project,
                                                'dataset_id',
                                                x)))
          
    iform(output, "name=%s" % safe_quote(safe_interpolate(cfg,
                                                  'project:' + project,
                                                  'dataset_name_format',
                                                  x)))

    for name, value in x.items('DEFAULT'):
        iform(output, 'property/')
        iform(output, 'name="%s"' % name)
        iform(output, 'value="%s"' % value, -1)
        
    iform(output, 'metadata/')
    iform(output, 'variables/')
    # pdb.set_trace()

    for v in f.variables.keys():
        iform(output, 'variable/')
        iform(output, 'name="%s"' % safe_getattr(f.variables[v], "id", "name"))

        vname = vocabulary_name(f.variables[v])
        iform(output, 'vocabulary_name="%s"' % vname)
        iform(output, 'units="%s"' % safe_getattr(f.variables[v],
                                                  "units"))
        iform(output, safe_getattr(f.variables[v], "long_name"), -1)
        
    for v in f.axes.keys():
        iform(output, 'variable/')
        iform(output, 'name="%s"' % v)
        vname = vocabulary_name(f.axes[v])
        iform(output, 'vocabulary_name="%s"' % vname)
        iform(output, 'units="%s"' % safe_getattr(f.axes[v], "units"))
        iform(output, safe_getattr(f.axes[v], "long_name"), -1)

    # pdb.set_trace()
    try:
        n = output.name
        if n == '<stdout>':
            rval = None
        else:
            rval = 'file:' + n
    except:
        rval = 'string:' + output.getvalue()

    return rval

# ---------------------------------------------------------------------------
def vocabulary_name(var):
    """
    Return the variable's vocabulary name -- standard_name if it's
    available, else long_name if it's available, else short_name.
    """
    for attr in ["standard_name", "long_name", "short_name"]:
        rval = safe_getattr(var, attr)
        if rval is not None:
            return rval
    
# ---------------------------------------------------------------------------
def dif_switch():
    """
    Examine the 'dif' (data interchange format) value of the
    esg_octopus config. If it is not set, return sys.stdout,
    indicating the output of this plugin should be written to stdout.

    If it is 'file', open a file in /tmp with the pid in the name
    for uniqueness and return a handle to that file.

    If it is 'string', create a StringIO buffer and return the
    handle to that.
    """
    main = sys.modules['__main__']

    try:
        outfmt = main.config('dif')
    except KeyError:
        return sys.stdout

    if outfmt == 'file':
        return open('/tmp/octopus.dif.%d' % os.getpid(), 'w')
    elif outfmt == 'string':
        return StringIO()
    else:
        raise StandardError('Invalid dif value in config -- '
                            + 'must be "file://" or "string://"')
    
# ---------------------------------------------------------------------------
def getDatasets(inpath):
    dslist = scan_dir_r(inpath)
    return dslist

# ---------------------------------------------------------------------------
def scan_dir_r(path, rval = []):
    if len(rval) < 1:
        rval.append(os.path.basename(path))
    else:
        rval[0] += "." + os.path.basename(path)

    fdlist = glob.glob(path + "/*")

    for fd in fdlist:
        if os.path.isdir(fd):
            rval = scan_dir_r(path + "/" + fd, rval)
        elif fd.endswith(".nc"):
            rval.append(fd)

    return rval

        
# ---------------------------------------------------------------------------
def iform(output, string, next_indent_level=None):
    global indent_level

    try:
        x = indent_level
    except:
        indent_level = 0
        
    if (0 < len(string.strip())):
        for i in range(0,indent_level):
            output.write('  ')
        output.write(string.strip())
        output.write('\n')
    
    if string.strip().endswith('/'):
        indent_level += 1
    elif next_indent_level != None:
        nil = int(next_indent_level)
        if nil == 0:
            indent_level = 0
        elif nil < 0:
            indent_level += nil
        if indent_level < 0:
            indent_level = 0
            
# ---------------------------------------------------------------------------
def safe_interpolate(cfg, section, option, xtra):
    rval = ''
    try_again = True
    tlen = -1
    while try_again:
        try:
            rval = cfg.get(section, option)
            try_again = False
        except InterpolationMissingOptionError, e:
            k = re.findall('key\s+:\s+(.*)\n', str(e))
            t = re.findall('rawval\s+:\s+(.*)\n', str(e))

            if (0 < tlen) and (tlen <= len(t[0])):
                raise StandardError('tail is not shrinking')
            tlen = len(t[0])
            
            if xtra.has_option('DEFAULT', k[0]):
                cfg.set(section, k[0], xtra.get('DEFAULT', k[0]))
            else:
                cfg.set(section, k[0], '<' + k[0] + '>')
            try_again = True
            
    return rval

# ---------------------------------------------------------------------------
def safe_quote(quotable):
    if ("'" not in quotable) and ('"' not in quotable):
        return "'" + quotable + "'"
    elif ("'" in quotable) and ('"' not in quotable):
        return '"' + quotable + '"'
    elif ('"' in quotable) and ("'" not in quotable):
        return "'" + quotable + "'"
    else:
        quotable = quotable.replace("'", "\\'")
        quotable = quotable.replace('"', '\\"')
        return '"' + quotable + '"'

# ---------------------------------------------------------------------------
def safe_getattr(var, attr, attrname=None):
    try:
        rval = var.__getattribute__(attr)
    except AttributeError:
        rval = None
    return rval
