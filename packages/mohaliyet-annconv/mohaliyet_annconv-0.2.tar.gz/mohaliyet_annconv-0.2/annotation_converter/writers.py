# annotation_converter/writers.py

from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

def create_pascal_voc_annotation(filename, size, objects):
    root = Element('annotation')
    SubElement(root, 'filename').text = filename
    size_element = SubElement(root, 'size')
    SubElement(size_element, 'width').text = str(size[0])
    SubElement(size_element, 'height').text = str(size[1])

    for (object_class, xmin, ymin, xmax, ymax) in objects:
        object_element = SubElement(root, 'object')
        SubElement(object_element, 'name').text = str(object_class)
        bbox_element = SubElement(object_element, 'bndbox')
        SubElement(bbox_element, 'xmin').text = str(xmin)
        SubElement(bbox_element, 'ymin').text = str(ymin)
        SubElement(bbox_element, 'xmax').text = str(xmax)
        SubElement(bbox_element, 'ymax').text = str(ymax)

    xml = tostring(root)
    dom = parseString(xml)
    return dom.toprettyxml()
