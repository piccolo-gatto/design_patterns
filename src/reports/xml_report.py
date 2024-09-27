import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from src.abstract_models.abstract_report import AbstractReport
from src.utils.format_reporting import FormatReporting
from src.utils.castom_exceptions import ArgumentTypeException, EmptyException

"""
Ответ формирует набор данных в формате XML
"""


class XMLReport(AbstractReport):

    def __init__(self) -> None:
        super().__init__()
        self.__format = FormatReporting.XML

    def create(self, data: list):
        if not isinstance(data, list):
            raise ArgumentTypeException("data", "list")
        if len(data) == 0:
            raise EmptyException()
        root = ET.Element('report')
        for row in data:
            row_data = ET.SubElement(root, 'row')
            self.serialize(row, row_data)

        xml_string = ET.tostring(root, encoding="unicode")
        self.result = minidom.parseString(xml_string).toprettyxml(indent="  ")

    @staticmethod
    def serialize(data, row):
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(data.__class__, x)), dir(data)))
        for field in fields:
            value = getattr(data, field)
            if hasattr(value, '__dict__'):
                element = ET.SubElement(row, field)
                XMLReport.serialize(value, element)
            elif isinstance(value, list):
                for val in value:
                    element = ET.SubElement(row, field)
                    XMLReport.serialize(val, element)
            else:
                element = ET.SubElement(row, field)
                element.text = str(value)
