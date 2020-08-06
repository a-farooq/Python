from xml.dom import minidom
import pathlib


ns = "{http://schemas.microsoft.com/developer/msbuild/2003}"
path = r"C:\\QuickBook\\ZincFeatures_US_DB\\source\\QB\\Features\\Domains\\HomepageDashboard"
tag_list = ["Platform", "WindowsTargetPlatformVersion", "CharacterSet", "CLRSupport", "TargetFrameworkVersion"]
master_vcx = "master.vcxproj"


def check_master(path_list):
    path_list.reverse()
    print(path_list)

    xmldoc = minidom.parse(master_vcx)
    # print(xmldoc.toprettyxml())

    master_root = xmldoc.documentElement
    print(master_root.tagName)

    # print(xmldoc.childNodes[0].tagName)
    # parent = xmldoc.childNodes[0]
    # print(parent.tagName)
    for child in master_root.childNodes:
        if child.nodeType == 1:
            print(child.tagName, child.attributes.items())
        pass

    """
    for child in master_root.childNodes:
        if child.nodeType == 1:
            print(child.nodeValue)
        else:
            print(False)

    if master_root.hasChildNodes():
        print(master_root.childNodes.length)
        print(True)
    else:
        print(False)
    return
    """

    if master_root.hasChildNodes():
        print(master_root.childNodes[1].firstChild.data)

    for item in path_list:
        # print(item.keys())
        tag = list(item.keys())[0]

        print(tag)
        # if isinstance(item, dict):
        #    k, v = item.items()
        #    print(k, v)


def process(tag, doc):
    same_name_tags = doc.getElementsByTagName(tag)

    if len(same_name_tags) == 0:
        return

    root = doc.documentElement
    print(root.tagName)

    # tag_dict = {}

    # for child in root.childNodes:
    #    print(child.nodeName, child.nodeValue, child.attributes)

    # print(type(platform))
    # print(platform[0])
    # print(platform[1])
    print("++++++++++++++++++++++")
    cloned = False
    path_list = []
    for tag in same_name_tags:
        """
        if not cloned:
            new_node = tag.cloneNode(True)
            root.appendChild(new_node)
            cloned = True
        """
        # if tag.nodeType == tag.TEXT_NODE:
        # print(tag.childNodes[0].nodeValue)
        tag_dict = dict.fromkeys([tag.childNodes[0].nodeValue], [])
        path_list.append(tag_dict)
        # path_list.append(tag.childNodes[0].nodeValue)
        if tag.hasAttributes():

            # tag_dict[tag.tagName] = tag.attributes.items()
            tag_dict = dict.fromkeys([tag.tagName], [tag.attributes.items()])
            # print(tag_dict)
            path_list.append(tag_dict)
        else:
            tag_dict = dict.fromkeys([tag.tagName], [])
            path_list.append(tag_dict)
            # path_list.append(tag.tagName)

        # print(tag.tagName)

        # print(path_list)
        parent = tag.parentNode

        while parent is not root:
            # print(parent.tagName)
            if parent.hasAttributes():
                # attrs = dict(parent.attributes.items())
                # print(attrs)
                # print(attrs.keys(), attrs.values())
                # tag_dict = {}
                tag_dict = dict.fromkeys([parent.tagName], [parent.attributes.items()])
                # tag_dict[parent.tagName] = parent.attributes.items()
                # print(tag_dict)

                path_list.append(tag_dict)
                # print("path list: %s" % path_list)
            parent = parent.parentNode

        # parent = tag.parentNode
        # parent.removeChild(tag)
        # print(platform.parentNode.tagName)

        print(path_list)
        check_master(path_list)
        path_list.clear()
        break

    return
    file_handle = open("master-bkup.vcxproj", "w")
    doc.writexml(file_handle)
    file_handle.close()
    # print(platform.firstChild.data)


def parse(xml_file):
    xmldoc = minidom.parse(xml_file)

    for tag in tag_list:
        process(tag, xmldoc)
        break


for file in pathlib.Path(path).glob("**/*.vcxproj"):
    # print(file)
    """
    d1 = {"a": 1, "b": 2}
    print(d1)
    d2 = {"b": 2, "a": 1}
    print(d2)
    if d1 == d2:
        print(True)
    else:
        print(False)
    break
    """
    fullpath = str(file).replace("\\", "\\\\")
    print(fullpath)
    parse(fullpath)
    break

"""    
print(path)
for file in pathlib.Path(path).glob('**/*.vcxproj'):
    print(file)
    parse(file)
    break
"""
