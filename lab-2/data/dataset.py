import os
import json
import csv
from PIL import Image


def prepare_validation_images_meta_information(folder_path, json_file, csv_file, class_name):
    filenames = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    json_structure = {str(i): [filename, class_name] for i, filename in enumerate(filenames)}

    with open(json_file, 'w') as file:
        json.dump(json_structure, file, indent=4)

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['filename', 'link'])
        for filename in filenames:
            writer.writerow([filename, f"![Thumbnail of {filename}](./data/input/thumbs/{filename})"])

    for i, filename in enumerate(filenames):
        # Resize and save thumbnail
        img_path = os.path.join(folder_path, filename)
        img = Image.open(img_path)
        img.thumbnail((128, 128))
        img.save(os.path.join(f"{folder_path}/thumbs", filename))


def main():
    folder_path = './input'
    json_file = '../test_images_map.json'
    csv_file = '../test_images.csv'
    prepare_validation_images_meta_information(folder_path, json_file, csv_file, "vase")


if __name__ == "__main__":
    main()