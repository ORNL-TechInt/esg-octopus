#!/bin/env jython

import glob
import os
import pdb
import re
import sys

from optparse import *

# ===========================================================================
def main(args):
    p = OptionParser()
    p.add_option('-c', '--config',
                 action='store', default='./esg_octopus.cfg', dest='config',
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

    sys.path.append(config("PluginDir"))
    sys.path.append(config("PlugoutDir"))

    if o.input_format != None:
        I = __import__(o.input_format)

    if o.output_format != None:
        O = __import__(o.output_format)

    O.launch()

# ===========================================================================
def config(item):
    global CFG
    return CFG[item]

# ===========================================================================
def config_load(filename):
    global CFG
    CFG = {}
    f = open(filename, 'r')
    for line in f:
        line = re.sub("#.*", "", line)
        if re.match("^\s*$", line) == None:
            (k, v) = re.split("\s*=\s*", line)
            CFG[k] = v.strip("\r\n")
    f.close()
    print CFG
    
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
