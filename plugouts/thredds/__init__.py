import pdb
import os
import sys

# print("This is thredds.__init__()")

# if "THREDDS_JAVA" in os.environ.keys():
#     netcdf = os.environ["THREDDS_JAVA"]
# else:
#     octopus = "/ccs/proj/techint/esg/esg-octopus/"
#     netcdf = octopus + "java/netcdf/"
    
# sys.path.append(netcdf + "netcdf-4.2.jar")
# sys.path.append(netcdf + "slf4j-log4j12-1.5.6.jar")
# sys.path.append(netcdf + "slf4j-api-1.5.6.jar")
# sys.path.append(netcdf + "log4j-1.2.15.jar")
# sys.path.append(netcdf + "jdom.jar")

# import org.apache.log4j.Level
# import org.jdom.Document
# import org.slf4j.LoggerFactory
# import thredds.catalog
# import thredds.catalog2.xml.writer
# import java.net.URI
# import java.io

from StringIO import StringIO

TAG = '0tag'
ATTR = '1attr'
CHLD = '2children'
SPACE = ' ' * 100

# ---------------------------------------------------------------------------
def launch(inpath, outpath, extra_metadata):
    # print("This is thredds.launch()")
    main = sys.modules['__main__']
    
    data = main.getData(inpath, extra_metadata)

    out = StringIO()
    if data == None:
        sys.exit()
    elif data.startswith('file:'):
        filename = data[len('file:'):]
        result = xmlify(open(filename, 'r'))
    elif data.startswith('string:'):
        result = xmlify(StringIO(data[len('string:'):]))
    else:
        dif = data.split(':')[0]
        raise StandardError('Data interchange format not recognized: %s'
                            % dif[0 : min(10, len(dif))])

    f = open(outpath, 'w')
    f.write(result)
    f.close()
    
# ---------------------------------------------------------------------------
def depth(str):
    return len(str) - len(str.lstrip())

# ---------------------------------------------------------------------------
def xmlify(stream):
    root = xmlement('ROOT')

    # build an xmlement structure
    d, line = cleanread(stream)
    while line != None:
        xml_add_child(root, line, d, stream)
        d, line = cleanread(stream)

    # expand the xmlement structure into XML code
    result = StringIO()
    xmlify_element_list(root, '', result)
    rval = result.getvalue()
    result.close()
    return rval

# ---------------------------------------------------------------------------
def xml_add_child(parent, line, cdepth, stream):
    tag = line.rstrip('/').lstrip()
    child = xmlement(tag)
    parent[CHLD].append(child)

    d, line = cleanread(stream)
    while (d != None) and (cdepth < d):
        if line.endswith('/'):
            xml_add_child(child, line, d, stream)
        else:
            k, v = line.strip().split("=", 1)
            child[ATTR][k] = v

        d, line = cleanread(stream)

    if (d != None):
        stream.seek(-1 * (len(line)+1), 1)
        
# ---------------------------------------------------------------------------
def cleanread(stream):
    line = stream.readline()
    if line == '':
        return None, None
    else:
        d = depth(line)
        line = line.rstrip('\n')
        return d, line
    
# ---------------------------------------------------------------------------
def xmlify_element_list(parent, indent, result):
    for elem in parent[CHLD]:
        result.write(indent + '<' + elem[TAG])
        for k in elem[ATTR].keys():
            result.write(' ' + k + '=' + elem[ATTR][k])
        if len(elem[CHLD]) <= 0:
            result.write('/>\n')
        else:
            result.write('>\n')
            xmlify_element_list(elem, indent + '  ', result)
            result.write(indent + '</' + elem[TAG] + '>\n')
        
# ---------------------------------------------------------------------------
def xmlement(tag = ''):
    elem = {}
    elem[TAG] = tag
    elem[ATTR] = {}
    elem[CHLD] = []
    return elem

# # ---------------------------------------------------------------------------
# def xmlify(stream, out):

#     line = stream.readline()

#     while line != '':
#         line = line.rstrip('\n')
#         if not line.endswith('/'):
#             raise StandardError("parse error")

#         tag = line.rstrip('/')
#         out.write('<' + tag + ' ')
#         xd = xml_start(stream, out, tag, depth(line))

#         while depth(line) < xd:
#             xd = xml_content(stream, out, depth(line))

#         out.write('</' + tag + '>\n')

#         line = stream.readline()
            
# # ---------------------------------------------------------------------------
# def xml_contents(stream, out, p_depth):
#     # !@! here we are!
#     pass

# # ---------------------------------------------------------------------------
# def xml_start(stream, out, tag, p_depth):
#     line = stream.readline().rstrip('\n')
#     m_depth = depth(line)
#     while (p_depth < m_depth) and (not line.endswith('/')):
#         attr = line.lstrip()
#         out.write(attr + ' ')

#         line = stream.readline().rstrip('\n')
#         m_depth = depth(line)

#     out.write(">\n")
#     stream.seek(-1 * (len(line)+1))

#     return m_depth

#     catalog = thredds.catalog.InvCatalogImpl(outpath,
#                                              "1.0",
#                                              java.net.URI(outpath))

#     cs = main.getServices()
#     for sname in cs.keys():
        
#         svc = thredds.catalog.InvService(cs[sname]['name'],
#                                          cs[sname]['serviceType'],
#                                          cs[sname]['base'],
#                                          "",
#                                          cs[sname]['desc'])

#         for p in cs[sname]['properties'].keys():
#             for val in cs[sname]['properties'][p]:
#                 prop = thredds.catalog.InvProperty(p, val)
#                 svc.addProperty(prop)
                
#         catalog.addService(svc)

#     catalog.addProperty(thredds.catalog.InvProperty("catalog_version",
#                                                     "2"))

#     dsl = main.getDatasets(inpath)
#     top = thredds.catalog.InvDatasetImpl(None, dsl[0])
#     top.setID(dsl[0])
#     top.setName(dsl[0])
#     top.addAccess(thredds.catalog.InvAccessImpl(top, "esg-user", svc))
#     catalog.addDataset(top)
#     for ds in dsl[1:]:
#         dsobj = thredds.catalog.InvDatasetImpl(top, ds)
#         dsobj.finish()
#         top.addDataset(dsobj)
        
#     top.finish()
#     catalog.finish()

#     writetool = "catalog"
    
#     # write it using InvCatalogFactory
#     if writetool == "catalog":
#         factory = thredds.catalog.InvCatalogFactory("default", True)
#         factory.writeXML(catalog, outpath)

#     # write it using ThreddsXmlWriter
#     elif writetool == "txw":
#         factory = thredds.catalog2.xml.writer.ThreddsXmlWriterFactory()
#         writer = factory.createThreddsXmlWriter()
#         writer.writeCatalog(catalog, thang)

#     # using thredds.catalog2.xml.writer.stax
#     else:
#         writer = thredds.catalog2.xml.writer.stax.StaxWriter()
#         writer.writeCatalog(catalog, java.io.File(outpath))

#         #thang has to be a java.io.File, java.io.Writer, or
#         #java.io.OutputStream
    
