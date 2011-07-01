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
import thredds.catalog2.xml.writer
import java.net.URI
import java.io

def launch(inpath, outpath):
    print("This is thredds.launch()")
    main = sys.modules['__main__']
    
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

    dsl = main.getDatasets(inpath)
    top = thredds.catalog.InvDatasetImpl(None, dsl[0])
    top.setID(dsl[0])
    top.setName(dsl[0])
    top.addAccess(thredds.catalog.InvAccessImpl(top, "esg-user", svc))
    catalog.addDataset(top)
    for ds in dsl[1:]:
        dsobj = thredds.catalog.InvDatasetImpl(top, ds)
        dsobj.finish()
        top.addDataset(dsobj)
        
    top.finish()
    catalog.finish()

    writetool = "catalog"
    
    # write it using InvCatalogFactory
    if writetool == "catalog":
        factory = thredds.catalog.InvCatalogFactory("default", True)
        factory.writeXML(catalog, outpath)

    # write it using ThreddsXmlWriter
    elif writetool == "txw":
        factory = thredds.catalog2.xml.writer.ThreddsXmlWriterFactory()
        writer = factory.createThreddsXmlWriter()
        writer.writeCatalog(catalog, thang)

    # using thredds.catalog2.xml.writer.stax
    else:
        writer = thredds.catalog2.xml.writer.stax.StaxWriter()
        writer.writeCatalog(catalog, java.io.File(outpath))

        #thang has to be a java.io.File, java.io.Writer, or
        #java.io.OutputStream
    
