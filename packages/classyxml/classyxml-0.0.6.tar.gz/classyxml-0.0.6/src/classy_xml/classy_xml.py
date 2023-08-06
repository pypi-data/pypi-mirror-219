from __future__ import annotations
import os
import xml.etree.ElementTree as ET
from collections import defaultdict


class ClassyXml:
    def __init__(self, xml_info: str = None, root_xml_element_name: str = "root"):
        """ClassyXml Class
        An xml parser that makes the element text and attributes of an xml
        file or xml string accessible as ClassyXml class attributes.

        Args:
            xml_info (str): xml file or xml string to parse
        """
        self._elements = defaultdict(list)

        if xml_info is not None:
            if os.path.isfile(xml_info):
                self.xml_file = xml_info
                root = ET.parse(xml_info).getroot()
            else:
                root = ET.fromstring(xml_info)
            self.root_xml_element_name = root.tag
            self.parse_xml(root)
        else:
            self.xml_file = None
            self.root_xml_element_name = root_xml_element_name

    def __setattr__(self, name, value):
        if isinstance(value, XmlElement):
            self._elements[name].append(value)
            super().__setattr__(name, self._elements[name])
        else:
            super().__setattr__(name, value)

    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if (
            isinstance(attr, list)
            and isinstance(attr[0], XmlElement)
            and len(attr) == 1
        ):
            return attr[0]
        else:
            return attr

    def parse_xml(self, root: ET.Element, element: XmlElement = None):
        """Parse the xml file and create class attributes for the elements and
        attributes defined in the xml file.
        """
        for attr_name, attr_value in root.attrib.items():
            setattr(element, attr_name, attr_value)
        children = root.findall("*")
        for child in children:
            child_element = self.parse_xml(child, XmlElement())
            if element is None:
                setattr(self, child.tag, child_element)
            else:
                setattr(element, child.tag, child_element)
            child_element.text = child.text

        return element

    def save(self):
        if self.xml_file is None:
            raise ValueError(
                "XML file is not defined. Use the save_as(xml_file) method instead"
            )
        self.save_as(self.xml_file)

    def save_as(self, xml_file):
        self.xml_file = xml_file
        with open(xml_file, "w") as file_handle:
            file_handle.write(f"<{self.root_xml_element_name}>\n")
            for element_name, elements in self._elements.items():
                for element in elements:
                    self._write_xml(file_handle, element, element_name)
            file_handle.write(f"</{self.root_xml_element_name}>\n")

    def _write_xml(self, file_handle, element: XmlElement, element_name: str, level=1):
        file_handle.write(f'{"  "*level}<{element_name}')

        for attribute_name, attribute_value in element._attributes.items():
            file_handle.write(f' {attribute_name}="{attribute_value}"')

        if len(element._elements) == 0:
            needs_end_tag = False
            if element.text:
                file_handle.write(f">{element.text}</{element_name}>\n")
            else:
                file_handle.write("/>\n")
        else:
            needs_end_tag = True
            file_handle.write(">\n")

        for child_name, child_elements in element._elements.items():
            for child_element in child_elements:
                self._write_xml(file_handle, child_element, child_name, level + 1)

        if needs_end_tag:
            file_handle.write(f'{"  "*level}</{element_name}>\n')


class XmlElement:
    def __init__(self, text: str = None, attributes: dict = {}):
        """Helper class with the ClassyXml class

        Args:
            text (str, optional): xml element text field. Defaults to None
            attributes (dict, optional): xml element attributes. Defaults to {}.
        """
        self._elements = defaultdict(list)
        self._attributes = {}
        self._text = text
        self._iterated = False

        for name, value in attributes.items():
            setattr(self, name, value)

    def __setattr__(self, name, value):
        if isinstance(value, XmlElement):
            self._elements[name].append(value)
            super().__setattr__(name, self._elements[name])
        else:
            if name[0] != "_" and name != "text":
                value = str(value)
                self._attributes[name] = value
            super().__setattr__(name, value)

    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if (
            isinstance(attr, list)
            and isinstance(attr[0], XmlElement)
            and len(attr) == 1
        ):
            return attr[0]
        else:
            return attr

    def __iter__(self):
        return self

    def __next__(self):
        if self._iterated:
            self._iterated = False
            raise StopIteration
        else:
            self._iterated = True
            return self

    def __len__(self):
        return 1

    def __getitem__(self, index: int):
        if index == 0 or index == -1:
            return self
        else:
            raise ValueError()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if isinstance(value, str):
            value = value.replace("\n", "").strip()
            if value == "":
                value = None
        elif value == None:
            pass
        else:
            value = str(value)
        self._text = value

    @text.deleter
    def text(self):
        self._text = None
