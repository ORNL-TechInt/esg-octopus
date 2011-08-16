#!/bin/env python
"""
Pluggable metadata extractor and formatter

 -c, --config <filepath>
    Specify the configuration file. Default: './esg_octopus.cfg'.

 -d, --debug
    Run the program under the python debugger. Default: False.

 -I, --input_format <plugin>
    Use <plugin> to extract metadata from the input file(s).
    Default: None.

 -i, --input_location <path>
    Where to find the input file(s) to be scanned. Default: None.

 -O, --output_format <plugout>
    Use <plugout> to format and write the metadata output. Default: None.

 -o, --output_location <path>
    Where to write the output file(s). Default: None.

 -x, --extra_metadata <path>
    File containing extra metadata to be included in the output.
    Default: None.
"""
import glob
import os
import pdb
import re
import sys

from optparse import *

# ===========================================================================
def main(args):
    """
    Accept and process command line options, import plug{in,out}s, launch.
    """
    root = os.path.dirname(sys.argv[0])
    p = OptionParser()
    p.add_option('-c', '--config',
                 action='store',
                 default='%s/esg_octopus.cfg' % root,
                 dest='config',
                 help='path to configuration file')
    p.add_option('-d', '--debug',
                 action='store_true', default=False, dest='debug',
                 help='start the debugger')
    p.add_option('-I', '--input_format',
                 action='store', default=None, dest='input_format',
                 help='name of input plugin')
    p.add_option('-i', '--input_location',
                 action='store', default=None, dest='input_location',
                 help='location of input file(s)')
    p.add_option('-O', '--output_format',
                 action='store', default=None, dest='output_format',
                 help='name of output plugout')
    p.add_option('-o', '--output_location',
                 action='store', default=None, dest='output_location',
                 help='where to write output file')
    p.add_option('-x', '--extra_metadata',
                 action='store', default=None, dest='extra_metadata',
                 help='where to find extra metadata')
    (o, a) = p.parse_args(args)
    
    if o.debug: pdb.set_trace()
    
    config_load(o.config)

    sys.path.append(config("PluginDir") % root)
    sys.path.append(config("PlugoutDir") % root)

    sys.modules['plugin'] = None
    if o.input_format != None:
        I = __import__(o.input_format)
        sys.modules['plugin'] = I
    
    sys.modules['plugout'] = None
    if o.output_format != None:
        O = __import__(o.output_format)
        sys.modules['plugout'] = O
        
    O.launch(o.input_location, o.output_location, o.extra_metadata)

# ===========================================================================
def config(item):
    """
    Retrieve a configuration value from dict CFG.

    Dictionary CFG is shared among the configuration management
    routines, set_default(), config_load(), and config().
    """
    global CFG
    if item == '':
        return CFG.keys()
    else:
        return CFG[item]

# ===========================================================================
def config_load(filename):
    """
    Call set_defaults to load CFG, then load config file values.

    Dictionary CFG is shared among the configuration management
    routines, set_default(), config_load(), and config().
    """
    global CFG
    set_defaults()
    f = open(filename, 'r')
    for line in f:
        line = re.sub("#.*", "", line)
        if re.match("^\s*$", line) == None:
            (k, v) = re.split("\s*=\s*", line)
            v = v.strip("\r\n")
            if v.startswith('"') and v.endswith('"'):
                v = v.strip('"')
            elif v.startswith("'") and v.endswith("'"):
                v = v.strip("'")
            CFG[k] = v
    f.close()
    
# ===========================================================================
def set_defaults():
    """
    Set default values in the CFG dictionary.

    Dictionary CFG is shared among the configuration management
    routines, set_default(), config_load(), and config().
    """
    global CFG
    CFG = {}
    CFG["PluginDir"] = "./plugins"
    CFG["PlugoutDir"] = "./plugouts"
    CFG[".cf"] = "netcdf"
    
# ===========================================================================
def getData(inpath, extra_metadata):
    return sys.modules['plugin'].getData(inpath, extra_metadata)

# ===========================================================================
def getDatasets(inpath):
    return sys.modules['plugin'].getDatasets(inpath)
    
# ===========================================================================
def getServices():
    """
    Build a services structure from the config. It looks like this:

       {'gridded': {'name':        "gridded",
                    'serviceType': "OpenDAP",
                    'base':        "/thredds/dodsC/",
                    'desc':        "OpenDAP",
                    'properties': {'requires_authorization': [false],
                                   'application': ["Web Browser"]
                                  }
                   },
        'HTTPServer': {'name':        "HTTPServer",
                       'serviceType': "HTTPServer",
                       'base':        "/thredds/fileServer/",
                       'desc':        "HTTPServer",
                       'properties': {'requires_authorization': [true],
                                      'application': ["Web Browser",
                                                      "Web Script"]
                                     }
                      }
        'HRMatPCMDI': {'name':        "HRMatPCMDI",
                       'serviceType': "SRM",
                       'base':        "srm://host.sample.gov:..."
                       'desc':        "SRM",
                       'properties': {'requires_authorization': [false]
                                     }
                      }
       }
    """
    svcs = {}
    kl = config('')
    pdx = 'properties'
    for key in kl:
        if key.startswith('.'):
            continue
        if 2 <= len(key.split('.')):
            v = config(key)
            k = key.split('.')
            if 2 == len(k):
                try:
                    svcs[k[0]][k[1]] = v
                except KeyError:
                    svcs[k[0]] = {}
                    svcs[k[0]][k[1]] = v
            elif 3 == len(k):
                if k[2] == 'name':
                    pname = v
                    vdx = k[0] + '.' + k[1] + '.value'
                    try:
                        svcs[k[0]][pdx][pname].append(config(vdx))
                    except KeyError, e:
                        if k[0] in str(e):
                            svcs[k[0]] = {}
                            svcs[k[0]][pdx] = {}
                            svcs[k[0]][pdx][pname] = []
                            svcs[k[0]][pdx][pname].append(config(vdx))
                        elif pdx in str(e):
                            svcs[k[0]][pdx] = {}
                            svcs[k[0]][pdx][pname] = []
                            svcs[k[0]][pdx][pname].append(config(vdx))
                        elif pname in str(e):
                            svcs[k[0]][pdx][pname] = []
                            svcs[k[0]][pdx][pname].append(config(vdx))
                        else:
                            raise StandardError("unexpected KeyError: '%s'"
                                                % e.str())
                elif k[2] == 'value':
                    pass

    return svcs

# ===========================================================================
sname = sys.argv[0]
if sname.endswith('.py') and '--makelink' in sys.argv:
    pname = re.sub('.py$', '', sname)
    print("creating symlink: %s -> %s" % (pname, sname))
    os.symlink(sname, pname)
elif sname.endswith('.py') and __name__ == '__main__':
    unittest.main()
elif not sname.endswith('.py') and __name__ == '__main__':
    main(sys.argv)
