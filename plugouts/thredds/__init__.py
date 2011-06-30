import os
import sys

print("This is thredds.__init__()")

if "THREDDS_JAVA" in os.environ.keys():
    netcdf = os.environ["THREDDS_JAVA"]
else:
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
import java.net.URI
import java.io

def launch(inpath, outpath):
    print("This is thredds.launch()")
    main = sys.modules['__main__']
    
    factory = thredds.catalog.InvCatalogFactory("default", True)
    
    catalog = thredds.catalog.InvCatalogImpl(outpath,
                                             "1.0",
                                             java.net.URI(outpath))

    cs = main.getServices()
    for sname in cs.keys():
        
        svc = thredds.catalog.InvService(cs[sname]['name'],
                                         cs[sname]['serviceType'],
                                         cs[sname]['base'],
                                         "",
                                         cs[sname]['desc'])

        for p in cs[sname]['properties'].keys():
            for val in cs[sname]['properties'][p]:
                prop = thredds.catalog.InvProperty(p, val)
                svc.addProperty(prop)
                
        catalog.addService(svc)

    catalog.addProperty(thredds.catalog.InvProperty("catalog_version",
                                                    "2"))

    # thredds.catalog.InvDatasetImpl(???)

    catalog.finish()
    factory.writeXML(catalog, outpath)

    
