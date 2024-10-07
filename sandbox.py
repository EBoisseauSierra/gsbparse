from gsbparse.account_sections._abstract_section import GsbFileSection

from gsbparse.file import GsbFile


sections: list[GsbFileSection] = []
# with open("Example_3.0-en.gsb") as gsb_file:
#     tree = ET.parse(gsb_file)
#     root = tree.getroot()
#     print(root.tag)
#     print(root.attrib)
#     for child in root:
#         section = ELEMENT_TAG_TO_SECTION.get(child.tag)
#         if section is None:
#             print(f"Unknown section: {child.tag}")
#         sections.append(section.from_xml(child))
#         print(child.tag, child.attrib)

# print(sections)

gsb_file = GsbFile.from_file("Example_3.0-en.gsb")
print(gsb_file)
