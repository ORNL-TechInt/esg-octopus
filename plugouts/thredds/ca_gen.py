import sys



octopus = "/home/cui/Dropbox/projects/ccesf/code/backesg/esg/esg-octopus/"
netcdf = octopus + "java/netcdf/"
sys.path.append(netcdf + "cataloggen-0.9.3.jar")
sys.path.append(netcdf + "slf4j-log4j12-1.5.6.jar")
sys.path.append(netcdf + "slf4j-api-1.5.6.jar")
sys.path.append(netcdf + "log4j-1.2.15.jar")
sys.path.append(netcdf + "jdom-b8.jar")
sys.path.append(netcdf + "dods.1.1.5.jar")

from thredds import catalog;
from thredds.cataloggen import CatalogGen;
from thredds.cataloggen.config import CatGenConfigMetadataFactory;
from thredds.cataloggen.config import CatalogGenConfig;
from thredds.cataloggen.config import DatasetSource;

from java.io import PrintStream;
from java.io import File;
from java.io import IOException;
from java.io import InputStream;
from java.net import MalformedURLException;
from java.net import URL;
from java.net import URI;
from java.net import URISyntaxException;
from java.util import List;
from java.util import Iterator;
from java.util import ArrayList;
from java.lang import Object;
from org import jdom
from org.apache import log4j;

print("This is thredds.__init__()")
#tempURI = java.net.URI
inFileName = "/home/cui/Dropbox/projects/ccesf/code/backesg/esg/esg-octopus/plugouts/thredds/config.xml"
outFileName = "/home/cui/Dropbox/projects/ccesf/code/backesg/esg/esg-octopus/plugouts/thredds/cat_out.xml"
arg = [inFileName, outFileName]
my_main = CatalogGen.main(arg)
#tmpURI = java.net.URI( inFileName)
#configFile = java.io.File( inFileName )
#tmpURI = configFile.toURI()
#configDocURL = tmpURI.toURL()
#log = java.lang.StringBuffer();
 
#catGen = thredds.cataloggen.CatalogGen(configDocURL)
#if catGen.isValid(log):
#   catGen.expand()
#   catGen.writeCatalog(outFileName)
     
