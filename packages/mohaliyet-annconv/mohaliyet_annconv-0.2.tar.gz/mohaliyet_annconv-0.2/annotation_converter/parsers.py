# annotation_converter/parsers.py

from abc import ABC, abstractmethod
from PIL import Image
from typing import List

class AnnotationParser(ABC):
    def __init__(self, annotation_file, image_file):
        self.annotation_file = annotation_file
        self.image_file = image_file
        self.image_size = self._get_image_size()

    def _get_image_size(self):
        with Image.open(self.image_file) as img:
            return img.size

    @abstractmethod
    def get_objects(self):
        pass


class YoloParser(AnnotationParser):
    def __init__(self, annotation_file, image_file, class_names_file):
        super().__init__(annotation_file, image_file)
        self.class_names = self._get_class_names(class_names_file)

    def _get_class_names(self, class_names_file) -> List[str]:
        with open(class_names_file, 'r') as file:
            return [line.strip() for line in file]

    def get_objects(self):
        objects = []
        with open(self.annotation_file, 'r') as file:
            for line in file:
                object_class_id, x_center, y_center, width, height = map(float, line.strip().split())
                object_class = self.class_names[int(object_class_id)]
                x_center *= self.image_size[0]
                y_center *= self.image_size[1]
                width *= self.image_size[0]
                height *= self.image_size[1]
                xmin = int(x_center - (width / 2))
                ymin = int(y_center - (height / 2))
                xmax = int(x_center + (width / 2))
                ymax = int(y_center + (height / 2))
                objects.append((object_class, xmin, ymin, xmax, ymax))
        return objects
