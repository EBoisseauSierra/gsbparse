from pathlib import Path
from xml.etree.ElementTree import Element

from defusedxml import ElementTree as ET  # noqa: N817

from gsbparse2.exceptions import InvalidGsbFileError, InvalidGsbFileRootError


def read_file(path: Path | str) -> Element:
    with open(path) as gsb_file:
        xml_tree = ET.parse(gsb_file)

    root = xml_tree.getroot()
    if type(root) is not Element:
        raise InvalidGsbFileError()
    if root.tag != "Grisbi":
        raise InvalidGsbFileRootError(root.tag)

    return root
