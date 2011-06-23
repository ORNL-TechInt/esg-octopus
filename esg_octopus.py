#!/bin/env jython

import glob
import os
import re
import sys

from optparse import *

def main(args):
    p = OptionParser()
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

    pl = glob.glob('plugins/*.py')
    # print pl

    if o.input_format != None:
        iname = 'plugins/' + o.input_format
        I = __import__(iname)

    if o.output_format != None:
        iname = 'plugins/' + o.output_format
        O = __import__(iname)

    O.launch()
    
sname = sys.argv[0]
if sname.endswith('.py') and '--makelink' in sys.argv:
    pname = re.sub('.py$', '', sname)
    print("creating symlink: %s -> %s" % (pname, sname))
    os.symlink(sname, pname)
elif sname.endswith('.py') and __name__ == '__main__':
    unittest.main()
elif not sname.endswith('.py') and __name__ == '__main__':
    main(sys.argv)
