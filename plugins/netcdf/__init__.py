import glob
import os

print("This is netcdf.__init__()")

def getDatasets(inpath):
    dslist = scan_dir_r(inpath)
    return dslist

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

        
