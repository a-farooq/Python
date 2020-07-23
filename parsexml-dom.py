from xml.dom import minidom
import pathlib
import os
import io

ns = "{http://schemas.microsoft.com/developer/msbuild/2003}"
master_vcx = r"C:\\QuickBook\\ZincRainbowPG_US_NB\\source\\master_vcxproj.props"
# path = r"C:\\QuickBook\\ZincRainbowPG_US_NB\\source\\QB\\Features\\Domains\\HomepageDashboard"
# path = r"C:\\QuickBook\\ZincRainbowPG_US_NB\\source\\QB\\Features"
# path = r"C:\\QuickBook\\ZincRainbowPG_US_NB\\source\\QB\\Platform"
# path = r"C:\\QuickBook\\ZincRainbowPG_US_DB\\source\\QB\\Deployment"
# path = r"C:\\QuickBook\\ZincRainbowPG_US_DB\\source\\QB\\CompanionApps"
# path = r"C:\\QuickBook\\ZincRainbowPG_US_DB\\source\\QB\\QA"
# path = r"C:\\QuickBook\\ZincRainbowPG_US_DB\\source\\QB\\Automation"
# path = r"C:\\QuickBook\\ZincRainbowPG_US_DB\\source\\QB\\CustomerSolutions"
# path = r"C:\\QuickBook\\ZincRainbowPG_US_DB\\source\\QB\\CompanionApps\\QBFileDrTool\\CrashRpt"
# path = r"C:\\QuickBook\\ZincRainbowPG_US_DB\\source\\QB\\CompanionApps\\QBFileDrTool"
path = r"C:\\QuickBook\\ZincRainbowPG_US_NB\\source\\QB"
tgt_tag_list = [("Platform", "Win32"), ("TargetFrameworkVersion", "v4.7"), ("WindowsTargetPlatformVersion", "8.1"),
                ("CharacterSet", "MultiByte"), ("CLRSupport", "false"), ("UseOfMfc", "false"),
                ("WholeProgramOptimization", "false")]
tag_list = [("Platform", "Win32")]
# , "Platform", "WindowsTargetPlatformVersion", "CharacterSet", "CLRSupport", "UseOfMfc"]
outfile = "output.xml"
master_path_list = []
xmlns_attr = "http://schemas.microsoft.com/developer/msbuild/2003"
DefaultTargets_attr = "Build"
ToolsVersion_attr = "14.0"


def write_to_file(xmldoc, filename):
    global outfile

    with open(outfile, "wb") as fh:
        fh.write(b'\xef\xbb\xbf')
        fh.write(xmldoc.toprettyxml(indent="  ", encoding="utf-8"))

    with open(outfile, "r") as fread, open(filename, "w") as fwrite:
        for line in fread.readlines():
            # print(line)
            if not line.strip():
                continue
            else:
                fwrite.write(line)


def write_to_config_file(xmldoc, config_file):
    # print("Inside write_to_config_file")
    write_to_file(xmldoc, config_file)


def write_to_master_file(xmldoc):
    # print("Inside write_to_master_file")
    write_to_file(xmldoc, master_vcx)


def is_tag_with_attrs_exist(cur_root, tag, attrs):
    for child in cur_root.childNodes:

        if child.nodeType is not 1:  # not ELEMENT_NODE
            continue
        else:
            # print("Element node found")
            pass

        # print(child.tagName, child.attributes.items())
        if child.tagName == tag:
            # print("============Found Tag")

            if child.attributes.items() == attrs:
                # print("============Found Attributes too")
                # found = True
                cur_root = child
                return True, cur_root

    return False, cur_root


# find created path list (of each target tag) into master config file. Add it if not present.
def find_add_path_to_master(path_list):
    # print("Inside find_add_path_to_master")
    path_list.reverse()
    # print(path_list)

    if os.stat(master_vcx).st_size == 0:
        print("File is empty")
        return

    xmldoc = minidom.parse(master_vcx)

    # print(xmldoc.toprettyxml())

    master_root = xmldoc.documentElement

    # print(master_root.tagName)

    # print(xmldoc.childNodes[0].tagName)

    cur_root = master_root

    # path_list is a list of dictionaries
    # each dict has tag against list of attributes
    for item in path_list:
        # print(item.keys())
        tag = list(item.keys())[0]
        attrs = list(item.values())[0]

        # print(tag, attrs)

        found = False
        # print("tagName: %s" % cur_root.tagName)

        if item is path_list[-1]:
            # print("Last element of list")

            text = cur_root.childNodes[0].nodeValue
            if str(tag) in text:
                # print("####Found full path####")
                found = True
                pass

        else:
            found, cur_root = is_tag_with_attrs_exist(cur_root, tag, attrs)

        # target tag is not found, add it to master config
        if not found:
            print("Not found, Adding Tag \"%s\" in master config file" % (str(tag)))
            # add_remaining_nodes()
            item_index = path_list.index(item)
            for item2 in path_list[item_index:]:
                tag = list(item2.keys())[0]
                attrs = list(item2.values())[0]

                # print("cur root tagName: %s" % cur_root.tagName)
                # print(tag, attrs)

                if item2 is path_list[-1]:
                    new_node = xmldoc.createTextNode(str(tag))
                    cur_root.appendChild(new_node)
                    break

                new_node = xmldoc.createElement(str(tag))

                for tup in attrs:
                    key, val = tup
                    new_node.setAttribute(key, val)

                cur_root.appendChild(new_node)
                cur_root = new_node
                # break
            write_to_master_file(xmldoc)

            if path_list not in master_path_list:
                master_path_list.append(path_list.copy())
            # print(xmldoc.toprettyxml())
            break


# find target tag into project config file (e.g. vcxproj) and create path list till the root tag
def create_path_list(tag_tuple, doc):
    # print("Inside create_path_list() for %s" % str(tag_tuple))
    tag = tag_tuple[0]
    tag_val = tag_tuple[1]
    same_name_tags = doc.getElementsByTagName(tag)

    if len(same_name_tags) == 0:
        print("Target tag \"%s\" not found in project config file" % tag)
        return

    root = doc.documentElement
    # print(root.tagName)

    path_list = []
    for tag in same_name_tags:
        # print("++++++++++++++++++++++")

        if str(tag.tagName) == "Platform":
            parent = tag.parentNode
            node = parent.getElementsByTagName("Configuration")
            same_name_tags.append(node[0])
            pass

        tag_dict = dict()

        tag_val = tag.firstChild.nodeValue
        # tag_text = tag.childNodes[0].nodeValue
        # tag_dict[tag_text] = []
        tag_dict[tag_val] = []
        # print(tag_dict)
        path_list.append(tag_dict)  # adding text string of target tag as a dict

        tag_dict = dict()
        # Adding target tag and its attributes as a dict
        if tag.hasAttributes():
            tag_dict[tag.tagName] = tag.attributes.items()
        else:
            tag_dict[tag.tagName] = []

        path_list.append(tag_dict)
        # print(tag.tagName)

        node = tag.parentNode
        tgt_tag_parent = node

        # adding parents of target tag as a dict
        while node is not root:
            tag_dict = dict()

            if node.hasAttributes():
                tag_dict[node.tagName] = node.attributes.items()
            else:
                tag_dict[node.tagName] = []

            path_list.append(tag_dict)
            node = node.parentNode

        find_add_path_to_master(path_list)

        if path_list not in master_path_list:
            master_path_list.append(path_list.copy())

        path_list.clear()

        # if tag_val == str(tag_text):
        #    tgt_tag_parent.removeChild(tag)

        # break

    return


def insert_import_master_tag(xmldoc, xml_file):
    root = xmldoc.documentElement

    master_tag = "Import"
    master_attrs = [("Project", "$(DEV_PATH)\\master_vcxproj.props")]
    found, dummy = is_tag_with_attrs_exist(root, master_tag, master_attrs)

    if not found:
        # insert_import_master_tag(xmldoc, master_tag, master_attrs[0])

        fchild = root.firstChild
        new_node = xmldoc.createElement(master_tag)
        new_node.setAttribute(master_attrs[0][0], master_attrs[0][1])
        # root.appendChild(new_node) # to add as last child
        root.insertBefore(new_node, fchild)  # to add as first child

        # write_to_config_file(xmldoc, xml_file)
    return xmldoc


# xml_file is the project config file e.g. *.vcxproj
def parse_proj_config(xml_file):
    xmldoc = minidom.parse(xml_file)
    # root = xmldoc.documentElement

    # print(xmldoc.toprettyxml())

    for tag_tuple in tag_list:
        # print("Project config file: %s" % xml_file)
        create_path_list(tag_tuple, xmldoc)
        # break

    # write_to_config_file(xmldoc, xml_file)


def add_empty_tgt_tag_in_proj_config(xmldoc, path_list, item, cur_root):
    print("Adding empty target tag")
    item_index = path_list.index(item)
    # iterate over the path list for the remaining tags starting from item and add each one
    for item2 in path_list[item_index:]:
        tag = list(item2.keys())[0]
        attrs = list(item2.values())[0]

        # print("cur root tagName: %s" % cur_root.tagName)
        # print(tag, attrs)

        if item2 is path_list[-1]:
            # Add empty tag
            new_node = xmldoc.createTextNode("")
            cur_root.appendChild(new_node)
            break

        new_node = xmldoc.createElement(str(tag))

        for tup in attrs:
            key, val = tup
            new_node.setAttribute(key, val)

        cur_root.appendChild(new_node)
        cur_root = new_node
        # break
    # write_to_config_file(xmldoc, xml_file)
    # print(xmldoc.toprettyxml())


# find created path list (of each target tag) into project config file.
# Add empty tag if not present.
# Delete tag if present
def find_add_remove_path_in_config(xmldoc, xml_file):
    print("Inside find_add_remove_path_in_config")
    # path_list.reverse()
    # print(path_list)

    if os.stat(xml_file).st_size == 0:
        print("File is empty")
        return

    # print(xmldoc.toprettyxml())
    root = xmldoc.documentElement

    """
    if root.getAttribute("xmlns") == xmlns_attr:
        root.removeAttribute("xmlns")
    else:
        root.setAttribute("xmlns", xmlns_attr)
    """

    if root.getAttribute("DefaultTargets") == DefaultTargets_attr:
        root.removeAttribute("DefaultTargets")

    if root.getAttribute("ToolsVersion") == ToolsVersion_attr:
        root.removeAttribute("ToolsVersion")

    # if root.getAttribute("DefaultTargets") == "":
    #    root.setAttribute("DefaultTargets", DefaultTargets_attr)

    # if root.getAttribute("ToolsVersion") == "":
    #    root.setAttribute("ToolsVersion", ToolsVersion_attr)

    for path_list in master_path_list:

        # print(xmldoc.childNodes[0].tagName)

        cur_root = root

        # master_path_list is a list of path_list
        # path_list is a list of dictionaries
        # each dict has tag against list of attributes
        for item in path_list:
            # print(item.keys())
            tag = list(item.keys())[0]
            attrs = list(item.values())[0]

            # print(tag, attrs)

            found = False
            # print("cur_root.tagName: %s" % cur_root.tagName)

            if item is path_list[-1]:
                # print("Last element of list")
                text = ""
                if len(cur_root.childNodes) > 0:
                    text = cur_root.childNodes[0].nodeValue

                if str(tag) == str(text):
                    # print("####Found full path####")
                    # Remove tag as it has been moved to master config file
                    print("Removing target tag \"{}\" from project config file".format(cur_root.tagName))

                    if cur_root.tagName == "Configuration":
                        projectConfig_node = cur_root.parentNode
                        itemGroup_node = projectConfig_node.parentNode
                        project_node = itemGroup_node.parentNode
                        project_node.removeChild(itemGroup_node)
                    else:
                        parent_node = cur_root.parentNode
                        parent_node.removeChild(cur_root)

                    found = True
                    # write_to_config_file(xmldoc, xml_file)

                    # while not parent_node.hasChildNodes():
                    #    node = parent_node
                    #    parent_node = node.parentNode
                    #    parent_node.removeChild(node)
                else:
                    # tag has another value which will override master file value
                    # Do nothing
                    found = True
                    pass

            else:
                found, cur_root = is_tag_with_attrs_exist(cur_root, tag, attrs)

            # target tag is not found, add it to master config
            if not found:
                # print("Target tag \"%s\" not found in project config file" % (str(tag)))

                # add_empty_tgt_tag_in_proj_config(xmldoc, path_list, item, cur_root)

                """
                item_index = path_list.index(item)
                for item2 in path_list[item_index:]:
                    tag = list(item2.keys())[0]
                    attrs = list(item2.values())[0]

                    # print("cur root tagName: %s" % cur_root.tagName)
                    # print(tag, attrs)

                    if item2 is path_list[-1]:
                        # Add empty tag
                        new_node = xmldoc.createTextNode("")
                        cur_root.appendChild(new_node)
                        break

                    new_node = xmldoc.createElement(str(tag))

                    for tup in attrs:
                        key, val = tup
                        new_node.setAttribute(key, val)

                    cur_root.appendChild(new_node)
                    cur_root = new_node
                    # break
                # write_to_config_file(xmldoc, xml_file)
                # print(xmldoc.toprettyxml())
                """
                break
    # write_to_config_file(xmldoc, xml_file)
    return xmldoc


def update_proj_file(xml_file):
    xmldoc = minidom.parse(xml_file)

    xmldoc = find_add_remove_path_in_config(xmldoc, xml_file)
    xmldoc = insert_import_master_tag(xmldoc, xml_file)

    write_to_config_file(xmldoc, xml_file)


def update_proj_configs():
    for file in pathlib.Path(path).glob("**/*.vcxproj"):
        # print(file)
        fullpath = str(file).replace("\\", "\\\\")
        print(fullpath)
        update_proj_file(fullpath)
        # break


def create_master_config():
    for file in pathlib.Path(path).glob("**/*.vcxproj"):
        # print(file)
        fullpath = str(file).replace("\\", "\\\\")
        print(fullpath)
        parse_proj_config(fullpath)
        # break


def main():
    create_master_config()
    update_proj_configs()


if __name__ == '__main__':
    main()
