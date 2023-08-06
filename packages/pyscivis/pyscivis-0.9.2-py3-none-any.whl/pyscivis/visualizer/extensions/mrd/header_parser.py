from typing import List, Dict, Optional
import uuid
from xml.etree.ElementTree import Element

from defusedxml import ElementTree
from ismrmrd.xsd.ismrmrdschema.ismrmrd import ismrmrdHeader as AcquisitionsHeader
from pyscivis.visualizer.plots.components.loading_div import LoadingDiv


class HeaderParser:
    @staticmethod
    def parse(header: AcquisitionsHeader,
              loading_indicator: Optional[LoadingDiv] = None
              ) -> Dict[str, List]:
        xml_tree = ElementTree.fromstring(header.toXML())
        column_dict = dict(name=list(), value=list())
        HeaderParser.create_list(column_dict, xml_tree)
        return column_dict

    @staticmethod
    def create_list(column_dict, node, depth=0):
        elem: Element
        for elem in node:
            name = elem.tag[30:]
            name = f"{depth*'——'} {name}"
            column_dict['name'].append(name)
            if not len(elem):
                column_dict['value'].append(elem.text)
            else:
                column_dict['value'].append("")
                HeaderParser.create_list(column_dict, elem, depth+1)
