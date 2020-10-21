import argparse
import logging
import os
import re
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element


def initialize_logger(log_level):
    if log_level == "DEBUG":
        logging.basicConfig(level=logging.DEBUG)
    elif log_level == "INFO":
        logging.basicConfig(level=logging.INFO)
    elif log_level == "WARNING":
        logging.basicConfig(level=logging.WARNING)
    else:
        logging.basicConfig(level=logging.ERROR)


def get_all_string_resource_files(project_directory):
    # get all xml files with string resources (english locale)
    english_locale_path_regex = re.compile('^.*/values/?$')
    string_resource_files = []
    for root, _, files in os.walk(project_directory, topdown=False):
        logging.debug("current dir: " + root)
        if english_locale_path_regex.match(root) and "build" not in root:
            for name in files:
                if "strings.xml" in name:
                    string_resource_files.append(os.path.join(root, name))
                else:
                    logging.debug("skipped: " + os.path.join(root, name))

    logging.info("\nFound files: %s", '\n'.join(string_resource_files))
    return string_resource_files


def generate_merged_xml(string_resource_files):
    merged_xml = Element("resources")
    for string_resource_file in string_resource_files:
        xml_data = ET.parse(string_resource_file)
        string_items = list(xml_data.getroot())
        for string_item in string_items:
            merged_xml.append(string_item)
    return merged_xml


def generate_xml_with_new_strings(current_strings_xml, base_xml_file_path="localise.xml"):
    # find new strings in merged_xml
    base_xml = ET.parse(base_xml_file_path)
    old_string_resource_names = [x.get("name") for x in list(base_xml.getroot())]
    new_string_resources = [x for x in list(current_strings_xml) if x.get("name") not in old_string_resource_names]

    # generate xml with new strings
    xml_with_new_strings = Element("resources")
    for new_string_resource in new_string_resources:
        xml_with_new_strings.append(new_string_resource)
    return ET.ElementTree(xml_with_new_strings)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='String resources merger for Android. Will walk through the project '
                                                 'dir, collect all strings.xml files (in default locale). All '
                                                 'collected strings will be used to generate new xml file')
    parser.add_argument('--log-level',
                        choices=['DEBUG', "INFO", "WARNING", "ERROR"],
                        help='Logging level. DEBUG, INFO, WARNING, ERROR')

    parser.add_argument('--path', '-p', metavar='path', type=str, help='Project path')
    parser.add_argument('--base-xml',
                        metavar='path',
                        type=str,
                        help='Base xml file path. Will be used to determinate what strings are not stored in base xml')
    parser.add_argument('--output', '-o', metavar='path', type=str, help='Output file path')

    args = parser.parse_args()

    initialize_logger(args.log_level)
    string_resource_files = get_all_string_resource_files(args.path)
    merged_xml = generate_merged_xml(string_resource_files)
    xml_with_new_strings = generate_xml_with_new_strings(merged_xml, args.base_xml)
    xml_with_new_strings.write(args.output)
