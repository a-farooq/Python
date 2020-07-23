import xml.etree.ElementTree as ET
import glob, os
import json
import pathlib
import pprint
import numpy as np
from lxml import etree
from lxml.etree import parse, tostring
import xpath

ns = "{http://schemas.microsoft.com/developer/msbuild/2003}"
# path = r"c:\QuickBook\ZincFeatures_US_DB\source\QB\Features\Domains\HomepageDashboard"
path = r"c:\QuickBook\ZincFeatures_US_DB\source\QB"
file1 = ""
file2 = ""

tag_dict = dict()
# file_out = open("master_config.vcxproj", "w")


def parse(xml_file):
    global file1, file2

    tree = ET.parse(xml_file)
    # tree = etree.parse(xml_file)

    root = tree.getroot()

    # xml_str = etree.tostring(root, encoding='utf-8')

    xml_file = os.path.basename(xml_file)

    # etree.xpath()
    # children = root.getchildren()
    # for child in children:
    #    ET.dump(child)

    # if file1 == "":
    #    file1 = ET.tostring(root, encoding='utf8').decode('utf8')
    # else:
    #    file2 = ET.tostring(root, encoding='utf8').decode('utf8')

    for child in root:
        child.tag = child.tag.replace(ns, "")
        tuple_str = (child.tag, child.attrib)
        attrib_str = json.dumps(tuple_str)
        # xml_file = os.path.basename(xml_file)
        # print(xml_file)
        # print(attrib_str)
        # print(str)
        # print()
        # root.xpath
        """
        ls_children = list(child)
        if len(ls_children) > 0:
            print("=========================================")
            print(tuple_str)
            print(ls_children)
        """
        # print(ls_children[1])

        content_list = []
        file_list = []
        if attrib_str in tag_dict:
            # content_list = tag_dict[attrib_str]
            # file_list = content_list[0]
            file_list = tag_dict[attrib_str]

        if xml_file not in file_list:
            file_list.append(xml_file)
            # content_list.clear()
            # content_list.insert(0, file_list)
            # content_list.insert(1, len(file_list))

        # file_list.append(xml_file)
        # tag_dict[attrib_str] = content_list
        tag_dict[attrib_str] = file_list

        # print(str)
        # print(child.tag, child.attrib)

    # pprint.pprint(tag_dict)

# print(root.tag)
# print(root[1][1].text)

# for platform in root.iter('Platform'):
#    print(platform.attrib)


file_count = 0

for file in pathlib.Path(path).glob('**/*.vcxproj'):
    # print(file)
    parse(file)
    file_count += 1
    # break

# pprint.pprint(tag_dict)
for key, value in tag_dict.items():
    print(key + "=======" + str(len(value)))

print("File Count: "+str(file_count))

# np.save('my_file.npy', tag_dict)

# print(file1)

"""   
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".vcxproj"):
            fullpath = os.path.join(root, file)
            print(fullpath)
            # parse(fullpath)
            break


os.chdir(r"c:\QuickBook\ZincFeatures_US_DB\source\QB\Features\Domains\HomepageDashboard")
for file in glob.glob("*.vcxproj"):
    print(file)


for file in os.listdir(r"c:\QuickBook\ZincFeatures_US_DB\source\QB\Features\Domains\HomepageDashboard"):
    if file.endswith(".vcxproj"):
        print(file)
"""
