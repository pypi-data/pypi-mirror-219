"""
Extended ECM Assoc Module to implement functions to read / write from
so called "Assoc" data structures in Extended ECM. Right now this module
is used to tweak settings in XML-based transport packages that include
Assoc structures inside some of the XML elements.

Class: Assoc
Methods:

stringToDict: convert an Assoc string to an Python dict representing the assoc values
dictToString: converting an Assoc dict to an Assoc string
"""

__author__ = "Dr. Marc Diefenbruch"
__copyright__ = "Copyright 2023, OpenText"
__credits__ = ["Kai-Philip Gatzweiler"]
__maintainer__ = "Dr. Marc Diefenbruch"
__email__ = "mdiefenb@opentext.com"

import re
import html


class Assoc:
    @classmethod
    def isUnicodeEscaped(cls, assoc_string: str) -> bool:
        pattern = r"\\u[0-9a-fA-F]{4}"
        matches = re.findall(pattern, assoc_string)
        return len(matches) > 0


    @classmethod
    def escapeUnicode(cls, assoc_string: str) -> str:
        encoded_string = assoc_string.encode('unicode_escape') # .decode()

        return encoded_string


    @classmethod
    def unescapeUnicode(cls, assoc_string: str) -> str:
        try:
            decoded_string = bytes(assoc_string, "utf-8").decode("unicode_escape")
            return decoded_string
        except UnicodeDecodeError:
            return assoc_string

    @classmethod
    def isHTMLEscaped(cls, assoc_string: str) -> bool:
        decoded_string = html.unescape(assoc_string)
        return assoc_string != decoded_string

    @classmethod
    def unescapeHTML(cls, assoc_string: str) -> str:
        decoded_string = html.unescape(assoc_string)
        return decoded_string

    @classmethod
    def stringToDict(cls, assoc_string: str) -> dict:
        if cls.isHTMLEscaped(assoc_string):
            assoc_string = cls.unescapeHTML(assoc_string)
        if cls.isUnicodeEscaped(assoc_string):
            assoc_string = cls.unescapeUnicode(assoc_string)

        # Split the string using regex pattern
        pieces = re.split(r",(?=(?:[^']*'[^']*')*[^']*$)", assoc_string)

        # Trim any leading/trailing spaces from each piece
        pieces = [piece.strip() for piece in pieces]

        # Split the last pieces from the assoc close tag
        last_piece = pieces[-1].split(">")[0]

        # Remove the first two and last pieces from the list
        # the first two are mostly "1" and "?"
        pieces = pieces[2:-1]

        # Insert the last pieces separately
        pieces.append(last_piece)

        assoc_dict: dict = {}

        for piece in pieces:
            name = piece.split("=")[0]
            if name[0] == "'":
                name = name[1:]
            if name[-1] == "'":
                name = name[:-1]
            value = piece.split("=")[1]
            if value[0] == "'":
                value = value[1:]
            if value[-1] == "'":
                value = value[:-1]
            assoc_dict[name] = value

        return assoc_dict

    @classmethod
    def dictToString(cls, assoc_dict: dict) -> str:
        assoc_string: str = "A&lt;1,?,"

        for item in assoc_dict.items():
            assoc_string += "\u0027" + item[0] + "\u0027"
            assoc_string += "="
            # Extended ECM's XML is a bit special in cases.
            # If the value is empty set (curly braces) it does
            # not put it in quotes. As Extended ECM is also very
            # picky about XML syntax we better produce it exactly like that.
            if item[1] == "{}":
                assoc_string += item[1] + ","
            else:
                assoc_string += "\u0027" + item[1] + "\u0027,"

        if assoc_dict.items():
            assoc_string = assoc_string[:-1]
        assoc_string += "&gt;"
        return assoc_string

    @classmethod
    def extractSubstring(
        cls, input_string: str, start_sequence: str, stop_sequence: str
    ):
        start_index = input_string.find(start_sequence)
        if start_index == -1:
            return None

        end_index = input_string.find(stop_sequence, start_index)
        if end_index == -1:
            return None

        end_index += len(stop_sequence)
        return input_string[start_index:end_index]

    @classmethod
    def extractAssocString(cls, input_string: str, is_escaped: bool = False) -> str:
        if is_escaped:
            assoc_string = cls.extractSubstring(input_string, "A&lt;", "&gt;")
        else:
            assoc_string = cls.extractSubstring(input_string, "A<", ">")
        return assoc_string
