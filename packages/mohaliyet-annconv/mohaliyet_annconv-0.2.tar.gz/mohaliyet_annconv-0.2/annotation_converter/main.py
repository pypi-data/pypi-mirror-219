# annotation_converter/main.py

from .parsers import YoloParser
from .writers import create_pascal_voc_annotation
import argparse
import glob
import os

def find_image_file(base_filename):
    for ext in ['.jpg', '.jpeg', '.png', '.tiff', '.bmp']:
        if os.path.isfile(base_filename + ext):
            return base_filename + ext
    return None

def main():
    parser = argparse.ArgumentParser(description='Convert YOLO annotations to Pascal VOC format.')
    parser.add_argument('input_dir', help='Path to the directory containing the YOLO annotations and corresponding images.')
    parser.add_argument('class_names_file', help='Path to the file containing class names for YOLO annotations.')
    parser.add_argument('output_dir', help='Directory to store the resulting Pascal VOC annotations.')
    args = parser.parse_args()

    annotation_files = glob.glob(os.path.join(args.input_dir, '*.txt'))
    
    for annotation_file in annotation_files:
        image_file = find_image_file(os.path.splitext(annotation_file)[0])
        if image_file is None:
            print(f'No image file found for annotation {annotation_file}, skipping.')
            continue

        try:
            parser = YoloParser(annotation_file, image_file, args.class_names_file)
        except IOError:
            print(f'Error reading image or class names file for annotation {annotation_file}, skipping.')
            continue

        voc_annotation = create_pascal_voc_annotation(
            os.path.splitext(os.path.basename(annotation_file))[0] + '.xml', 
            parser.image_size, 
            parser.get_objects()
        )

        output_file = os.path.join(args.output_dir, os.path.splitext(os.path.basename(annotation_file))[0] + '.xml')
        with open(output_file, 'w') as f:
            f.write(voc_annotation)

if __name__ == '__main__':
    main()
