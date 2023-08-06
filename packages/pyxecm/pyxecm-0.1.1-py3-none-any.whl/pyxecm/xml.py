""" XML helper module

Class: XML
Methods:

searchSetting: search a JSON-like setting inside an XML text telement
replaceInXmlFiles: Replace all occurrences of the search pattern with the replace string in all
                   XML files in the directory and its subdirectories.

"""

__author__ = "Dr. Marc Diefenbruch"
__copyright__ = "Copyright 2023, OpenText"
__credits__ = ["Kai-Philip Gatzweiler"]
__maintainer__ = "Dr. Marc Diefenbruch"
__email__ = "mdiefenb@opentext.com"

import logging
import os
import re
# import regex as re

# we need lxml instead of stadard xml.etree to have xpath capabilities!
from lxml import etree

# import xml.etree.ElementTree as etree
from .assoc import Assoc

logger = logging.getLogger("pyxecm")


class XML:
    @classmethod
    def getXmlElement(cls, xml_content: str, xpath: str):
        # Parse XML content into an etree
        tree = etree.fromstring(xml_content)

        # Find the XML element specified by XPath
        element = tree.find(xpath)

        return element

    @classmethod
    def modifyXmlElement(cls, xml_content: str, xpath: str, new_value: str):
        """Update the text (= content) of an XML element

        Args:
            xml_content (str): the content of an XML file
            xpath (str): XML Path to identify the XML element
            new_value (str): new text (content)
        """
        element = cls.getXmlElement(xml_content=xml_content, xpath=xpath)

        if element is not None:
            # Modify the XML element with the new value
            element.text = new_value
        else:
            logger.warning("XML Element -> {} not found.".format(xpath))

    @classmethod
    def searchSetting(
        cls,
        element_text: str,
        setting_key: str,
        is_simple: bool = True,
        is_escaped: bool = False,
    ):
        # the simple case covers settings like this:
        # &quot;syncCandidates&quot;:true,
        # "syncCandidates":true,
        # in this case the setting value is a scalar like true, false, a number or none
        # the regular expression pattern searches for a setting name in "..." followed
        # by a colon (:). The value is taken from what follows the colon until the next comma (,)
        if is_simple:
            if is_escaped:
                pattern = r"&quot;{0}&quot;:[^,]*".format(setting_key)
            else:
                pattern = r'"{0}":[^,]*'.format(setting_key)
        # the more complex case is a string value that may itself have commas,
        # so we cannot look for comma as a delimiter like in the simple case
        # but we take the value for a string delimited by double quotes ("...")
        else:
            if is_escaped:
                pattern = r"&quot;{0}&quot;:&quot;.*&quot;".format(setting_key)
            else:
                pattern = r'"{0}":"([^"]*)"'.format(setting_key)

        match = re.search(pattern, element_text)
        if match:
            setting_line = match.group(0)
            setting_value = setting_line.split(":")[1]
            return setting_value
        else:
            return None

    @classmethod
    def replaceSetting(
        cls,
        element_text,
        setting_key,
        new_value: str,
        is_simple: bool = True,
        is_escaped: bool = False,
    ):
        if is_simple:
            if is_escaped:
                pattern = r"&quot;{0}&quot;:[^,]*".format(setting_key)
            else:
                pattern = r'"{0}":[^,]*'.format(setting_key)
        else:
            if is_escaped:
                pattern = r"&quot;{0}&quot;:&quot;.*&quot;".format(setting_key)
            else:
                pattern = r'"{0}":"([^"]*)"'.format(setting_key)

        new_text = re.sub(pattern, new_value, element_text)

        return new_text

    @classmethod
    def replaceInXmlFiles(
        cls,
        directory: str,
        search_pattern: str,
        replace_string: str,
        xpath: str = "",
        setting: str = "",
        assoc_elem: str = "",
    ) -> bool:
        """Replaces all occurrences of the search pattern with the replace string in all XML files
            in the directory and its subdirectories.

        Args:
            directory (string): directory to traverse for XML files
            search_pattern (sting): string to search in the XML file. This can be empty
                                    if xpath is used!
            replace_string (string): replacement string
            xpath (string): narrow down the replacement to an XML element that es defined by the XPath
                            for now the XPath needs to be constructed in a way the it returns
                            one or none element.
            setting (string): narrow down the replacement to the line that includes the setting with this name.
                              This parameter is optional.
            assoc_elem (string): lookup a specific assoc element. This parameter is optional.
        Returns:
            boolean: True if a replacement happened, False otherwise
        """
        # Define the regular expression pattern to search for
        # search pattern can be empty if an xpath is used. So
        # be careful here:
        if search_pattern:
            pattern = re.compile(search_pattern)

        found = False

        # Traverse the directory and its subdirectories
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                # Check if the file is an XML file
                if file.endswith(".xml"):
                    # Read the contents of the file
                    file_path = os.path.join(subdir, file)

                    # if xpath is given we do an intelligent replacement
                    if xpath:
                        xml_modified = False
                        logger.info("Replacement with xpath...")
                        logger.info(
                            "XML path -> {}, setting -> {}, assoc element -> {}".format(
                                xpath, setting, assoc_elem
                            )
                        )
                        tree = etree.parse(file_path)
                        if not tree:
                            logger.erro(
                                "Cannot parse XML tree -> {}. Skipping...".format(
                                    file_path
                                )
                            )
                            continue
                        root = tree.getroot()
                        # find the matching XML element using the given XPath:
                        elements = root.xpath(xpath)
                        if not elements:
                            logger.info(
                                "The XML file -> {} does not have any element with the given XML path -> {}. Skipping...".format(
                                    file_path, xpath
                                )
                            )
                            continue
                        for element in elements:
                            # as XPath returns a list
                            #                            element = elements[0]
                            logger.info(
                                "Found XML element -> {} in -> {}".format(
                                    element.tag, xpath
                                )
                            )
                            # the simple case: replace the complete text of the XML element
                            if not setting and not assoc_elem:
                                logger.info(
                                    "Replace complete text of XML element -> {} from -> {} to -> {}".format(
                                        xpath, element.text, replace_string
                                    )
                                )
                                element.text = replace_string
                                xml_modified = True
                            # In this case we want to set a complete value of a setting (basically replacing a whole line)
                            elif setting and not assoc_elem:
                                logger.info(
                                    "Replace single setting -> {} in XML element -> {} with new value -> {}".format(
                                        setting, xpath, replace_string
                                    )
                                )
                                setting_value = cls.searchSetting(
                                    element.text, setting, is_simple=True
                                )
                                if setting_value:
                                    logger.info(
                                        "Found existing setting value -> {}".format(
                                            setting_value
                                        )
                                    )
                                    #                                    replace_string = "&quot;" + setting + "&quot;:" + replace_string + ","
                                    if (
                                        replace_string == "true"
                                        or replace_string == "false"
                                        or replace_string == "none"
                                        or replace_string.isnumeric()
                                    ):
                                        replace_setting = (
                                            '"' + setting + '":' + replace_string
                                        )
                                    else:
                                        replace_setting = (
                                            '"' + setting + '":"' + replace_string + '"'
                                        )
                                    logger.info(
                                        "Replacement setting -> {}".format(
                                            replace_setting
                                        )
                                    )
                                    element.text = cls.replaceSetting(
                                        element_text=element.text,
                                        setting_key=setting,
                                        new_value=replace_setting,
                                        is_simple=True,
                                    )
                                    xml_modified = True
                                else:
                                    logger.warning(
                                        "Cannot find the value for setting -> {}. Skipping...".format(
                                            setting
                                        )
                                    )
                                    continue
                            # in this case the text is just one assoc (no setting substructure)
                            elif not setting and assoc_elem:
                                logger.info(
                                    "Replace single Assoc value -> {} in XML element -> {} with -> {}".format(
                                        assoc_elem, xpath, replace_string
                                    )
                                )
                                assoc_string: str = Assoc.extractAssocString(
                                    input_string=element.text
                                )
                                logger.debug("Assoc String -> {}".format(assoc_string))
                                assoc_dict = Assoc.stringToDict(
                                    assoc_string=assoc_string
                                )
                                logger.debug("Assoc Dict -> {}".format(assoc_dict))
                                assoc_dict[
                                    assoc_elem
                                ] = replace_string  # escaped_replace_string
                                assoc_string_new: str = Assoc.dictToString(
                                    assoc_dict=assoc_dict
                                )
                                logger.info(
                                    "Replace assoc with -> {}".format(assoc_string_new)
                                )
                                element.text = assoc_string_new
                                element.text = element.text.replace('"', "&quot;")
                                xml_modified = True
                            # In this case we have multiple settings with their own assocs
                            elif setting and assoc_elem:
                                logger.info(
                                    "Replace single Assoc value -> {} in setting -> {} in XML element -> {} with -> {}".format(
                                        assoc_elem, setting, xpath, replace_string
                                    )
                                )
                                setting_value = cls.searchSetting(
                                    element.text, setting, is_simple=False
                                )
                                if setting_value:
                                    logger.info(
                                        "Found setting value -> {}".format(
                                            setting_value
                                        )
                                    )
                                    assoc_string: str = Assoc.extractAssocString(
                                        input_string=setting_value
                                    )
                                    logger.debug(
                                        "Assoc String -> {}".format(assoc_string)
                                    )
                                    assoc_dict = Assoc.stringToDict(
                                        assoc_string=assoc_string
                                    )
                                    logger.debug("Assoc Dict -> {}".format(assoc_dict))
                                    escaped_replace_string = replace_string.replace(
                                        "'", "\\\\\u0027"
                                    )
                                    logger.info(
                                        "Escaped replacement string -> {}".format(
                                            escaped_replace_string
                                        )
                                    )
                                    assoc_dict[
                                        assoc_elem
                                    ] = escaped_replace_string  # escaped_replace_string
                                    assoc_string_new: str = Assoc.dictToString(
                                        assoc_dict=assoc_dict
                                    )
                                    assoc_string_new = assoc_string_new.replace(
                                        "'", "\\u0027"
                                    )
                                    # replace_setting = "&quot;" + setting + "&quot;:&quot;" + assoc_string_new + "&quot;"
                                    replace_setting = (
                                        '"' + setting + '":"' + assoc_string_new + '"'
                                    )
                                    logger.info(
                                        "Replacement setting -> {}".format(
                                            replace_setting
                                        )
                                    )
                                    # here we need to apply a "trick". It is required
                                    # as regexp cannot handle the special unicode escapes \u0027
                                    # we require. We first insert a placeholder "PLACEHOLDER"
                                    # and let regexp find the right place for it. Then further
                                    # down we use a simple search&replace to switch the PLACEHOLDER
                                    # to the real value (replace() does not have the issues with unicode escapes)
                                    element.text = cls.replaceSetting(
                                        element_text=element.text,
                                        setting_key=setting,
                                        #                                        new_value=replace_setting,
                                        new_value="PLACEHOLDER",
                                        is_simple=False,
                                        is_escaped=False,
                                    )
                                    element.text = element.text.replace(
                                        "PLACEHOLDER", replace_setting
                                    )
                                    element.text = element.text.replace('"', "&quot;")
                                    xml_modified = True
                                else:
                                    logger.warning(
                                        "Cannot find the value for setting -> {}. Skipping...".format(
                                            setting
                                        )
                                    )
                                    continue
                        if xml_modified:
                            logger.info(
                                "XML tree has been modified. Write updated file -> {}...".format(
                                    file_path
                                )
                            )

                            new_contents = etree.tostring(
                                tree,
                                pretty_print=True,
                                xml_declaration=True,
                                encoding="UTF-8",
                            )
                            # we need to undo some of the stupid things tostring() did:
                            new_contents = new_contents.replace(
                                b"&amp;quot;", b"&quot;"
                            )
                            new_contents = new_contents.replace(
                                b"&amp;apos;", b"&apos;"
                            )
                            new_contents = new_contents.replace(b"&amp;gt;", b"&gt;")
                            new_contents = new_contents.replace(b"&amp;lt;", b"&lt;")

                            # Replace single quotes inside double quotes strings with "&apos;" (manual escaping)
                            # This is required as we next want to replace all double quotes with single quotes
                            pattern = b'"([^"]*)"'
                            new_contents = re.sub(
                                pattern,
                                lambda m: m.group(0).replace(b"'", b"&apos;"),
                                new_contents,
                            )

                            # Replace single quotes in XML text elements with "&apos;"
                            # and replace double quotes in XML text elements with "&quot;"
                            # This is required as we next want to replace all double quotes with single quotes
                            pattern = b'>([^<>]+?)<'
                            replacement = lambda match: match.group(0).replace(b'"', b"&quot;")
                            new_contents = re.sub(pattern, replacement, new_contents)
                            replacement = lambda match: match.group(0).replace(b"'", b"&apos;")
                            new_contents = re.sub(pattern, replacement, new_contents)

                            # Change double quotes to single quotes across the XML file - Extended ECM has it that way:
                            new_contents = new_contents.replace(b'"', b"'")

                            # Write the updated contents to the file.
                            # We DO NOT want to use tree.write() here
                            # as it would undo the manual XML tweaks we
                            # need for Extended ECM. We also need "wb"
                            # as we have bytes and not str as a data type
                            with open(file_path, "wb") as f:
                                f.write(new_contents)

                            found = True
                    # this is not using xpath - do a simple search and replace
                    else:
                        logger.info("Replacement without xpath...")
                        with open(file_path, "r") as f:
                            contents = f.read()
                        # Replace all occurrences of the search pattern with the replace string
                        new_contents = pattern.sub(replace_string, contents)

                        # Write the updated contents to the file if there were replacements
                        if contents != new_contents:
                            logger.info(
                                "Found search string -> {} in XML file -> {}. Write updated file...".format(
                                    search_pattern, file_path
                                )
                            )
                            # Write the updated contents to the file
                            with open(file_path, "w") as f:
                                f.write(new_contents)
                            found = True

        return found

        # end method definition
