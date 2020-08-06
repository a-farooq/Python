from xml.dom import minidom

Station1 = ['Pentium M', '512MB']
Station2 = ['Pentium Core 2', '1024MB']
Station3 = ['Pentium Core Duo', '1024MB']
StationList = [Station1, Station2, Station3]

DOMimpl = minidom.getDOMImplementation()

# xmldoc = DOMimpl.createDocument(None, "Workstations", None)
xmlfile = "./stations.xml"
# print(xmlfile)
xmldoc = minidom.parse(xmlfile)
print(xmldoc.toprettyxml())

doc_root = xmldoc.documentElement

node = doc_root.getElementsByTagName('Computer')[0]

element = xmldoc.createElement('Processor')
element.setAttribute("a", "1")
node.appendChild(element)
print(xmldoc.toprettyxml())

"""
doc_root = xmldoc.documentElement

for station in StationList:
    #Create Node
    node = xmldoc.createElement("Computer")

    element = xmldoc.createElement('Processor')
    # element.appendChild(xmldoc.createTextNode(station[0]))
    node.appendChild(element)

    element = xmldoc.createElement('Memory')
    # element.appendChild(xmldoc.createTextNode(station[1]))
    node.appendChild(element)

    doc_root.appendChild(node)

nodeList = doc_root.childNodes
for node in nodeList:
    print(node.toprettyxml())

file = open("stations.xml", 'w')
file.write(xmldoc.toprettyxml())
"""
