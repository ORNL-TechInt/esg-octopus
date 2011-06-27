import sys

print("This is thredds.__init__()")

octopus = "/ccs/proj/techint/esg/esg-octopus/"
netcdf = octopus + "java/netcdf/"
sys.path.append(netcdf + "netcdf-4.2.jar")
sys.path.append(netcdf + "slf4j-log4j12-1.5.6.jar")
sys.path.append(netcdf + "slf4j-api-1.5.6.jar")
sys.path.append(netcdf + "log4j-1.2.15.jar")
sys.path.append(netcdf + "jdom.jar")

import org.apache.log4j.Level
import org.jdom.Document
import org.slf4j.LoggerFactory
import thredds.catalog
import thredds.catalog2.xml.writer.ThreddsXmlWriter


def launch():
    print("This is thredds.launch()")

    factory = thredds.catalog.InvCatalogFactory("default", True)
    print("factory:")
    print(type(factory))
    print dir(factory)

    cname = "file:" + octopus \
            + "data/1/ornl.ultrahighres.CESM1.T85F09.B1850.v1.xml"
    # cname = "file:" + octopus + "data/catalog.xml"
    catalog = factory.readXML(cname)
    print("\ncatalog:")
    print(type(catalog))
    print dir(catalog)

    print "\nname: ", catalog.getName()
    print "dataset roots: ", catalog.getDatasetRoots()

    print "datasets: "
    for ds in catalog.getDatasets():
        print "   %s" % ds
        
    print "services: "
    for svc in catalog.getServices():
        print "    %s" % svc
        
    print "base URI: ", catalog.getBaseURI()
    print "version: ", catalog.getVersion()
    
